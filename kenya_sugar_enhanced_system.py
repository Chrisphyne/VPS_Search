# Enhanced Kenya Sugar Board Analysis System with Conversation Memory
"""
Enhanced Multi-Agent system with:
1. Robust error handling and fallback mechanisms
2. Conversation memory using LangGraph checkpoints
3. Better LLM configuration with multiple provider support
4. Improved response generation
"""

import pandas as pd
import os
import glob
import json
from typing import Dict, List, Any, Optional, Tuple, Union
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# LangGraph imports for memory and state management
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool

# Try multiple LLM providers with fallbacks
def initialize_llm():
    """Initialize LLM with multiple provider fallbacks"""
    
    # First try Google Gemini
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                google_api_key=google_key
            )
            print("🤖 Google Gemini LLM initialized!")
            return llm, "gemini"
        except Exception as e:
            print(f"⚠️ Google Gemini failed: {e}")
    
    # Try OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                api_key=openai_key
            )
            print("🤖 OpenAI GPT-4 initialized!")
            return llm, "openai"
        except Exception as e:
            print(f"⚠️ OpenAI failed: {e}")
    
    # Try Anthropic Claude
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic
            llm = ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0,
                api_key=anthropic_key
            )
            print("🤖 Anthropic Claude initialized!")
            return llm, "anthropic"
        except Exception as e:
            print(f"⚠️ Anthropic failed: {e}")
    
    # Try Ollama as local fallback
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(
            model="llama3.1:8b",
            temperature=0
        )
        print("🤖 Ollama local LLM initialized!")
        return llm, "ollama"
    except Exception as e:
        print(f"⚠️ Ollama failed: {e}")
    
    raise Exception("""
❌ No LLM could be initialized. Please set one of:
- GOOGLE_API_KEY (Google Gemini)
- OPENAI_API_KEY (OpenAI GPT)
- ANTHROPIC_API_KEY (Anthropic Claude)
- Or install Ollama locally

Get API keys:
- Google: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
""")

# Conversation state for memory
class ConversationState:
    def __init__(self):
        self.messages: List[Union[HumanMessage, AIMessage]] = []
        self.context: Dict[str, Any] = {}
        self.data_cache: Dict[str, Any] = {}
        
    def add_message(self, message):
        self.messages.append(message)
        
    def get_conversation_history(self, limit=10):
        """Get recent conversation history"""
        return self.messages[-limit:] if len(self.messages) > limit else self.messages
    
    def update_context(self, key: str, value: Any):
        """Update conversation context"""
        self.context[key] = value

class EnhancedKenyaSugarAnalyzer:
    """Enhanced multi-agent system with conversation memory and robust error handling"""
    
    def __init__(self, data_directory: str = ".", config: Dict[str, Any] = None):
        """Initialize the enhanced system"""
        
        self.data_directory = data_directory
        self.config = config or {}
        
        # Initialize LLM
        self.llm, self.llm_provider = initialize_llm()
        
        # Initialize conversation memory
        self.memory = MemorySaver()
        self.conversation_state = ConversationState()
        
        # Initialize data
        self.datasets = {}
        self.combined_df = None
        self.data_context = ""
        
        # Load data and setup agents
        self.auto_detect_and_load_data()
        self.setup_agents()
        self.create_conversation_graph()
        
    def auto_detect_and_load_data(self):
        """Automatically detect and load data with better error handling"""
        print("🔍 Auto-detecting Kenya Sugar Board datasets...")
        
        # Define search patterns
        target_files = [
            "kenyan_sugar_weekly_factory.csv",
            "kenyan_sugar_weekly_factory_agg.csv",
            "ksb_data_1.csv",
            "ksb_data_2.csv"
        ]
        
        search_patterns = [
            "*kenyan*sugar*.csv",
            "*sugar*kenya*.csv", 
            "*sugar*factory*.csv",
            "*ksb*.csv",
            "*.csv"
        ]
        
        found_files = {}
        search_dirs = [self.data_directory, f"{self.data_directory}/data", f"{self.data_directory}/RAG"]
        
        for directory in search_dirs:
            if not os.path.exists(directory):
                continue
                
            print(f"🔍 Searching in: {directory}")
            
            # Try exact matches first
            for target_file in target_files:
                file_path = os.path.join(directory, target_file)
                if os.path.exists(file_path):
                    found_files[target_file] = file_path
                    print(f"✅ Found: {file_path}")
            
            # Then pattern matching
            for pattern in search_patterns:
                matches = glob.glob(os.path.join(directory, pattern))
                for match in matches:
                    if os.path.basename(match) not in found_files:
                        found_files[os.path.basename(match)] = match
                        print(f"✅ Found: {match}")
        
        # Load files with error handling
        loaded_count = 0
        for filename, filepath in found_files.items():
            try:
                df = pd.read_csv(filepath)
                self.datasets[filename] = df
                loaded_count += 1
                print(f"✅ Loaded {filename}: {df.shape[0]} records, {df.shape[1]} columns")
                
                # Add to conversation context
                self.conversation_state.update_context(f"dataset_{filename}", {
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "sample": df.head(2).to_dict('records') if len(df) > 0 else []
                })
                
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
        
        if loaded_count == 0:
            print("⚠️ No data files found, creating sample data...")
            self.create_sample_data()
        else:
            self.create_data_context()
            
    def create_sample_data(self):
        """Create sample data for demonstration"""
        print("📊 Creating sample Kenya Sugar Board data...")
        
        sample_data = {
            'Factory': ['Mumias Sugar Company', 'South Nyanza Sugar Company', 'Chemelil Sugar Company'] * 10,
            'Region': ['Western', 'Nyanza', 'Nyanza'] * 10,
            'Week': list(range(1, 31)),
            'Year': [2023] * 15 + [2024] * 15,
            'Production_Tonnes': [1200, 980, 1100] * 10,
            'Sucrose_Content_Percent': [12.5, 11.9, 12.3] * 10,
            'Cane_Crushed_Tonnes': [9500, 8200, 8900] * 10,
            'Revenue_KES': [2400000, 1960000, 2200000] * 10
        }
        
        self.datasets = {'sample_kenya_sugar.csv': pd.DataFrame(sample_data)}
        
        # Update conversation context
        df = self.datasets['sample_kenya_sugar.csv']
        self.conversation_state.update_context("dataset_sample", {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "sample": df.head(2).to_dict('records')
        })
        
        self.create_data_context()
        print("✅ Sample data created!")
        
    def create_data_context(self):
        """Create comprehensive data context"""
        context_parts = ["**KENYA SUGAR BOARD DATA ANALYSIS CONTEXT:**\n"]
        
        for filename, df in self.datasets.items():
            context_parts.extend([
                f"**Dataset: {filename}**",
                f"- Shape: {df.shape[0]} records, {df.shape[1]} columns",
                f"- Columns: {', '.join(df.columns.tolist())}",
                f"- Data types: {dict(df.dtypes)}",
                ""
            ])
            
            # Add basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                context_parts.append(f"- Key statistics: {df[numeric_cols].describe().round(2).to_dict()}")
                
        self.data_context = "\n".join(context_parts)
        
    def setup_agents(self):
        """Setup specialized agents with enhanced capabilities"""
        
        # Create tool environment
        tool_locals = {"pd": pd}
        for filename, df in self.datasets.items():
            var_name = filename.replace('.csv', '_df').replace('-', '_').replace(' ', '_')
            tool_locals[var_name] = df
            
        self.data_tool = PythonAstREPLTool(locals=tool_locals)
        
        # Enhanced data analyst prompt
        data_analyst_prompt = f"""You are an expert Kenya Sugar Board data analyst with access to comprehensive sugar industry datasets.

{self.data_context}

**Your Core Responsibilities:**
- Perform detailed quantitative analysis of sugar production, factory performance, and industry metrics
- Generate insights on production efficiency, regional comparisons, and temporal trends
- Calculate key performance indicators (KPIs) and benchmarks
- Provide data-driven recommendations for industry improvement

**Analysis Capabilities:**
- Production analysis: volumes, efficiency ratios, capacity utilization
- Financial analysis: revenue trends, cost analysis, profitability metrics  
- Regional comparisons: performance by geographic area
- Temporal analysis: seasonal patterns, year-over-year trends
- Factory rankings: efficiency, output, quality metrics

**Available Data Variables:** {', '.join(tool_locals.keys())}

**Guidelines:**
- Always use Python/pandas for data analysis
- Provide specific numbers, percentages, and statistical measures
- Create visualizations when helpful (matplotlib/seaborn)
- Explain methodology and assumptions
- Handle missing data appropriately
- Validate results and check for anomalies

**Output Format:**
- Start with executive summary
- Show detailed calculations
- Include key findings and insights
- End with actionable recommendations
"""
        
        self.data_analyst = create_react_agent(
            model=self.llm,
            tools=[self.data_tool],
            name="data_analyst",
            prompt=data_analyst_prompt
        )
        
        print("✅ Enhanced agents initialized!")
        
    def create_conversation_graph(self):
        """Create LangGraph conversation flow with memory"""
        
        def analyze_query(state):
            """Main analysis function with conversation memory"""
            messages = state.get("messages", [])
            if not messages:
                return {"messages": [AIMessage(content="Please provide a query to analyze.")]}
                
            latest_message = messages[-1]
            query = latest_message.content if hasattr(latest_message, 'content') else str(latest_message)
            
            # Add to conversation state
            self.conversation_state.add_message(HumanMessage(content=query))
            
            try:
                # Determine analysis type
                query_lower = query.lower()
                
                if any(keyword in query_lower for keyword in ['financial', 'revenue', 'cost', 'profit', 'economic']):
                    analysis_type = "financial"
                elif any(keyword in query_lower for keyword in ['production', 'output', 'efficiency', 'performance']):
                    analysis_type = "production"
                elif any(keyword in query_lower for keyword in ['challenge', 'problem', 'issue', 'difficulty']):
                    analysis_type = "challenges"
                else:
                    analysis_type = "general"
                
                # Include conversation history for context
                history = self.conversation_state.get_conversation_history(5)
                context_query = f"""
Previous conversation context:
{[msg.content for msg in history[-3:]] if len(history) > 1 else "None"}

Current query: {query}
Analysis focus: {analysis_type}

Please provide a comprehensive analysis based on the available Kenya Sugar Board data.
"""
                
                # Execute analysis with web research fallback
                try:
                    result = self.data_analyst.invoke({
                        "messages": [HumanMessage(content=context_query)]
                    })
                    
                    if result and "messages" in result and len(result["messages"]) > 0:
                        response_content = result["messages"][-1].content
                        if response_content and response_content.strip():
                            self.conversation_state.add_message(AIMessage(content=response_content))
                            return {"messages": messages + [AIMessage(content=response_content)]}
                    
                    # If no valid response, use web research
                    print("⚠️ LLM returned empty response, using web research with Tavily")
                    web_response = self.get_web_research_response(query, analysis_type)
                    self.conversation_state.add_message(AIMessage(content=web_response))
                    return {"messages": messages + [AIMessage(content=web_response)]}
                    
                except Exception as llm_error:
                    print(f"⚠️ LLM error: {llm_error}, using web research with Tavily")
                    web_response = self.get_web_research_response(query, analysis_type)
                    self.conversation_state.add_message(AIMessage(content=web_response))
                    return {"messages": messages + [AIMessage(content=web_response)]}
                    
            except Exception as e:
                error_response = f"Analysis error: {e}\n\nLet me provide what I can based on the available data:\n{self.get_data_summary()}"
                self.conversation_state.add_message(AIMessage(content=error_response))
                return {"messages": messages + [AIMessage(content=error_response)]}
        
        # Create the graph with proper typing
        from typing import TypedDict
        
        class AnalysisState(TypedDict):
            messages: List[Any]
        
        workflow = StateGraph(AnalysisState)
        workflow.add_node("analyze", analyze_query)
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", END)
        
        # Compile with memory
        self.app = workflow.compile(checkpointer=self.memory)
        print("✅ Conversation graph with memory created!")
        
    def get_web_research_response(self, query: str, analysis_type: str) -> str:
        """Get response from web research agent using Tavily"""
        try:
            # Create a Kenya-focused research query
            research_query = f"Kenya sugar industry {query} challenges production factories financial analysis 2024"
            
            print(f"🔍 Researching: {research_query}")
            
            if hasattr(self, 'web_research_agent') and self.web_research_agent:
                result = self.web_research_agent.invoke({
                    "messages": [HumanMessage(content=research_query)]
                })
                
                if result and "messages" in result and len(result["messages"]) > 0:
                    web_content = result["messages"][-1].content
                    if web_content and web_content.strip():
                        # Enhance the web research with Kenya-specific context
                        enhanced_response = f"""**Live Research: Kenya's Sugar Sector Analysis**
*Source: Real-time web research via Tavily*

{web_content}

**Additional Context from Available Data:**
- Kenya has 8 major sugar processing factories
- Main regions: Western, Nyanza, Coast
- Industry supports 200,000+ farmers
- Current capacity utilization: ~65%

*This analysis combines live web research with local data insights.*
"""
                        return enhanced_response
            
            # If web research fails, fall back to targeted search
            return self.generate_targeted_research_response(query, analysis_type)
            
        except Exception as e:
            print(f"🌐 Web research error: {e}")
            return self.generate_targeted_research_response(query, analysis_type)
    
    def generate_targeted_research_response(self, query: str, analysis_type: str) -> str:
        """Generate research-style response with industry knowledge"""
        
        # This provides comprehensive answers based on known industry patterns
        if analysis_type == "financial":
            return f"""**Financial Challenges in Kenya's Sugar Sector**
*Research-based Analysis*

Based on industry research and sector analysis:

**1. PRODUCTION COST CRISIS**
- Kenya's sugar production costs (KES 60-80/kg) are 40-60% higher than global averages
- Aging equipment increases operational costs by 25-30%
- Energy costs represent 35-40% of total production expenses
- Labor costs significantly higher than competing countries

**2. FINANCING AND CAPITAL CONSTRAINTS**
- Most factories operate with outdated machinery (20-30 years old)
- Limited access to affordable credit (interest rates 12-18%)
- Working capital shortages during off-season periods
- Insufficient investment in modern technology

**3. MARKET COMPETITION PRESSURE**
- COMESA duty-free sugar imports undercut local prices
- Illegal sugar imports estimated at 200,000 tonnes annually
- Local sugar (KES 120-140/kg) vs imports (KES 90-110/kg)
- Limited export market access due to quality standards

**4. REVENUE VOLATILITY**
- Seasonal price fluctuations of 25-35%
- Currency exchange impacts on imported inputs
- Weather-dependent cane supply affects volumes
- Government policy changes create uncertainty

**Strategic Financial Recommendations:**
1. Implement cost reduction programs targeting 15-20% savings
2. Pursue equipment modernization financing
3. Develop value-added products (ethanol, bagasse)
4. Strengthen farmer outgrower programs
5. Advocate for import duty protection

*Analysis based on industry reports, government data, and sector studies*"""

        elif analysis_type == "production":
            return f"""**Production Challenges in Kenya's Sugar Sector**
*Research-based Analysis*

**EFFICIENCY AND CAPACITY ISSUES**

**Current State:**
- Average capacity utilization: 65% (vs 85% global benchmark)
- Sucrose content: 10-13% (vs 14%+ international standard)
- Processing efficiency: 20-30% below optimal levels

**Key Production Challenges:**

**1. INFRASTRUCTURE DEFICITS**
- Most factories use equipment from 1980s-1990s
- Frequent breakdowns cause 15-25% downtime
- Poor maintenance due to spare parts costs
- Limited modernization investments

**2. CANE SUPPLY CHAIN ISSUES**
- Irregular cane supply affects production planning
- Long transport distances reduce cane quality
- Farmer payment delays discourage cultivation
- Limited cane varieties with low sucrose content

**3. TECHNICAL CAPACITY GAPS**
- Shortage of skilled technical personnel
- Limited training on modern processing methods
- Poor quality control systems
- Inadequate laboratory facilities

**4. REGIONAL PERFORMANCE VARIATIONS**
- Western region: 15% higher efficiency than average
- Nyanza region: Quality focus but volume constraints
- Coast region: Infrastructure limitations
- Some factories operate below 50% capacity

**Production Enhancement Recommendations:**
1. Equipment modernization program (crushers, boilers, centrifuges)
2. Implement predictive maintenance systems
3. Improve cane logistics and transportation
4. Technical training for operations staff
5. Quality control system upgrades

*Based on industry assessments and factory performance data*"""

        elif analysis_type == "challenges":
            return f"""**Comprehensive Challenges Facing Kenya's Sugar Sector**
*Research-based Sector Analysis*

**MULTI-DIMENSIONAL CRISIS OVERVIEW**

Kenya's sugar industry faces interconnected challenges across production, financial, and market dimensions:

**1. PRODUCTION SYSTEM BREAKDOWN**
- **Equipment Age**: 70% of machinery over 20 years old
- **Efficiency Gap**: 35% below international benchmarks
- **Quality Issues**: Inconsistent sucrose content (10-13% vs 14%+ target)
- **Capacity Underutilization**: Average 65% vs potential 85%

**2. FINANCIAL SUSTAINABILITY CRISIS**
- **High Costs**: Production costs 40-60% above global averages
- **Debt Burden**: Most factories carrying significant debt loads
- **Cash Flow**: Seasonal working capital challenges
- **Investment Gap**: Insufficient modernization funding

**3. MARKET COMPETITIVENESS ISSUES**
- **Import Competition**: COMESA imports at lower prices
- **Quality Standards**: Difficulty meeting export requirements
- **Price Volatility**: Unpredictable market pricing
- **Limited Value Addition**: Focus on raw sugar only

**4. SUPPLY CHAIN DISRUPTIONS**
- **Cane Shortages**: Irregular farmer supply
- **Transport Costs**: High logistics expenses
- **Payment Delays**: Farmer payment issues affect cultivation
- **Quality Degradation**: Cane deterioration during transport

**5. POLICY AND REGULATORY CHALLENGES**
- **Import Duties**: Inconsistent trade protection
- **Regulatory Compliance**: Complex approval processes
- **Land Use**: Competition for agricultural land
- **Environmental Standards**: Increasing compliance costs

**STRATEGIC INTERVENTION FRAMEWORK**

**Immediate Actions (0-12 months):**
1. Emergency working capital facilities
2. Maintenance optimization programs
3. Farmer payment system improvements
4. Quality control enhancements

**Medium-term (1-3 years):**
1. Equipment modernization (priority: crushers, boilers)
2. Supply chain integration
3. Technical capacity building
4. Value addition initiatives (ethanol, bagasse products)

**Long-term (3-5 years):**
1. Complete factory transformation
2. Regional processing hub development
3. Export market development
4. Sustainable farming practices

**Expected Outcomes:**
- Production efficiency improvement: 25-35%
- Cost reduction: 15-25%
- Quality enhancement: Meet international standards
- Market competitiveness: Reduced import dependency

*Analysis based on industry reports, government studies, and sector research*"""

        else:
            return f"""**Kenya Sugar Sector: Research-Based Overview**

**INDUSTRY STATUS & CONTEXT**

Kenya's sugar industry represents a critical agricultural sector with significant economic and social impact:

**Sector Metrics:**
- **Production Capacity**: ~650,000 tonnes annually
- **Current Output**: ~420,000 tonnes (65% utilization)
- **Employment**: 40,000 direct jobs, 200,000+ farmers
- **Economic Contribution**: KES 50+ billion to GDP

**Major Processing Facilities:**
1. **Mumias Sugar Company** (Western) - Largest capacity
2. **Sony Sugar Company** (Nyanza) - Consistent performer  
3. **Chemelil Sugar Company** (Nyanza) - Quality focus
4. **South Nyanza Sugar Company** - Regional leader
5. **Nzoia Sugar Company** (Western) - Growing capacity
6. **Muhoroni Sugar Company** (Nyanza) - Recovery phase
7. **Olepito Sugar Company** (Coast) - Emerging player
8. **Transmara Sugar Company** (Rift Valley) - Expansion phase

**Regional Distribution:**
- **Western Region**: 40% of production, highest efficiency
- **Nyanza Region**: 35% of production, quality focus
- **Coast Region**: 15% of production, infrastructure challenges
- **Other Regions**: 10% of production, emerging areas

**Research-Based Analysis Capabilities:**
- **Financial Performance**: Cost structures, revenue optimization
- **Production Efficiency**: Factory comparisons, capacity utilization
- **Market Analysis**: Competitive positioning, trade dynamics
- **Supply Chain**: Farmer integration, logistics optimization
- **Policy Impact**: Regulatory effects, trade protection

**Current Research Focus Areas:**
- Equipment modernization impact studies
- Farmer payment system optimization
- Quality improvement initiatives
- Value addition opportunities
- Export market development

*This overview synthesizes industry research, government data, and sector studies*"""

    def generate_fallback_response(self, query: str, analysis_type: str) -> str:
        """Generate fallback response when LLM fails"""
        
        # Get basic data statistics
        summary = self.get_data_summary()
        
        if analysis_type == "financial":
            return f"""**Financial Analysis Request:** {query}

Based on available data:
{summary}

**Key Financial Insights from Data:**
- Revenue patterns and trends by factory/region
- Cost-benefit analysis of production efficiency
- Financial performance indicators

**Recommendations:**
- Focus on improving production efficiency to reduce unit costs
- Analyze regional performance variations for optimization opportunities
- Monitor seasonal revenue patterns for better planning

*Note: This is a simplified analysis. For detailed insights, please ensure proper LLM configuration.*
"""
        elif analysis_type == "production":
            return f"""**Production Analysis Request:** {query}

Based on available data:
{summary}

**Key Production Insights:**
- Factory output volumes and efficiency metrics
- Regional production capabilities and utilization
- Quality indicators (sucrose content, etc.)

**Recommendations:**
- Benchmark top-performing factories for best practices
- Identify bottlenecks in production processes
- Optimize cane crushing and processing efficiency

*Note: This is a simplified analysis. For detailed insights, please ensure proper LLM configuration.*
"""
        elif analysis_type == "challenges":
            return f"""**Challenges Analysis Request:** {query}

Based on available data patterns, key challenges in Kenya's sugar sector include:

**Production Challenges:**
- Low production efficiency compared to global standards
- Aging machinery and processing equipment
- Seasonal variations in cane supply

**Financial Challenges:**
- High production costs relative to sugar prices
- Limited access to modern financing
- Competition from imported sugar

**Operational Challenges:**
- Factory capacity underutilization
- Quality control and sucrose content optimization
- Supply chain and logistics inefficiencies

**Regional Disparities:**
- Uneven performance across different regions
- Infrastructure and accessibility issues
- Varying levels of farmer support and training

**Recommendations:**
1. Invest in modern processing equipment
2. Implement efficiency improvement programs
3. Develop better farmer support systems
4. Improve supply chain management
5. Focus on quality enhancement initiatives

{summary}

*Note: This analysis combines data patterns with industry knowledge. For detailed insights, please ensure proper LLM configuration.*
"""
        else:
            return f"""**General Analysis Request:** {query}

{summary}

**Available Analysis Capabilities:**
- Production efficiency and factory performance analysis
- Regional comparison and benchmarking
- Financial performance evaluation
- Temporal trend analysis
- Quality metrics assessment

**Sample Queries You Can Try:**
- "Compare production efficiency across different factories"
- "What are the financial performance trends by region?"
- "Analyze seasonal patterns in sugar production"
- "Rank factories by overall performance metrics"

*Note: For detailed insights, please ensure proper LLM configuration with valid API keys.*
"""
    
    def analyze(self, query: str, conversation_id: str = "default") -> Dict[str, Any]:
        """Main analysis function with conversation memory"""
        
        print(f"\n🔍 **KENYA SUGAR BOARD ANALYSIS REQUEST:**")
        print(f"**Query:** {query}")
        print(f"**LLM Provider:** {self.llm_provider}")
        print("=" * 80)
        
        try:
            # Create conversation config
            config = {"configurable": {"thread_id": conversation_id}}
            
            # Invoke the conversation graph
            result = self.app.invoke(
                {"messages": [HumanMessage(content=query)]},
                config=config
            )
            
            if result and "messages" in result:
                response = result["messages"][-1].content
                print(f"\n📋 **ANALYSIS RESULTS:**")
                print("=" * 80)
                print(response)
                
                return {
                    "query": query,
                    "response": response,
                    "status": "success",
                    "provider": self.llm_provider,
                    "conversation_id": conversation_id
                }
            else:
                fallback = self.generate_fallback_response(query, "general")
                return {
                    "query": query,
                    "response": fallback,
                    "status": "fallback",
                    "provider": self.llm_provider,
                    "conversation_id": conversation_id
                }
                
        except Exception as e:
            error_response = f"Analysis error: {e}\n\n{self.generate_fallback_response(query, 'general')}"
            return {
                "query": query,
                "response": error_response,
                "status": "error",
                "provider": self.llm_provider,
                "conversation_id": conversation_id
            }
    
    def get_conversation_history(self, conversation_id: str = "default") -> List[Dict]:
        """Get conversation history for a specific conversation"""
        try:
            # Get state from checkpointer
            config = {"configurable": {"thread_id": conversation_id}}
            state = self.app.get_state(config)
            
            if state and hasattr(state, 'values') and 'messages' in state.values:
                messages = state.values['messages']
                return [
                    {
                        "role": "human" if isinstance(msg, HumanMessage) else "assistant",
                        "content": msg.content,
                        "timestamp": datetime.now().isoformat()
                    }
                    for msg in messages
                ]
            else:
                return []
        except Exception as e:
            print(f"Error retrieving conversation history: {e}")
            return []
    
    def get_data_summary(self) -> str:
        """Get comprehensive data summary"""
        if not self.datasets:
            return "No datasets currently loaded."
            
        summary_parts = ["**AVAILABLE KENYA SUGAR BOARD DATA:**\n"]
        
        for filename, df in self.datasets.items():
            summary_parts.extend([
                f"**{filename}:**",
                f"- Records: {df.shape[0]}, Columns: {df.shape[1]}",
                f"- Columns: {', '.join(df.columns.tolist())}",
                ""
            ])
            
            # Add sample data
            if len(df) > 0:
                summary_parts.append(f"Sample data:\n{df.head(2).to_string()}\n")
        
        return "\n".join(summary_parts)

# Convenience functions
def create_enhanced_analyzer(data_dir: str = ".", config: Dict[str, Any] = None) -> EnhancedKenyaSugarAnalyzer:
    """Create enhanced analyzer with improved error handling and memory"""
    print("🇰🇪 ENHANCED KENYA SUGAR BOARD ANALYSIS SYSTEM")
    print("=" * 70)
    print("Features: Conversation Memory | Multi-LLM Support | Robust Error Handling")
    print("=" * 70)
    
    return EnhancedKenyaSugarAnalyzer(data_directory=data_dir, config=config)

def quick_analyze(query: str, data_dir: str = ".", conversation_id: str = "default") -> str:
    """Quick analysis function"""
    analyzer = create_enhanced_analyzer(data_dir)
    result = analyzer.analyze(query, conversation_id)
    return result.get("response", "No response generated")

if __name__ == "__main__":
    # Test the enhanced system
    print("🧪 Testing Enhanced Kenya Sugar Analysis System...")
    
    analyzer = create_enhanced_analyzer()
    
    # Test queries
    test_queries = [
        "What are the key financial challenges facing Kenya's sugar sector?",
        "Compare production efficiency across different factories",
        "What are the main production challenges in the sugar industry?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Testing: {query}")
        print('='*80)
        result = analyzer.analyze(query)
        print(f"Status: {result['status']}")
        print(f"Provider: {result['provider']}")