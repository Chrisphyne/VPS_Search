# Kenya Sugar Board Multi-Agent Analysis System
"""
Multi-Agent system for comprehensive Kenya Sugar Board data analysis
implementing context quarantine with specialized agents:
1. Data Retriever Agent - Analyzes local CSV data
2. Web Research Agent - Performs external research
3. Supervisor Agent - Coordinates and synthesizes results
"""

import pandas as pd
import os
from typing import Dict, List, Any
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
# Try different import paths for Tavily
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
except ImportError:
    try:
        from langchain_tavily import TavilySearchResults
    except ImportError:
        try:
            from tavily import TavilyClient
            TavilySearchResults = None  # Will use custom implementation
        except ImportError:
            TavilySearchResults = None

from langgraph.prebuilt import create_react_agent

# Try different import paths for supervisor
try:
    from langgraph_supervisor import create_supervisor
except ImportError:
    # Alternative implementation if langgraph_supervisor is not available
    create_supervisor = None
from IPython.display import Image, display
import warnings
warnings.filterwarnings('ignore')

class KenyaSugarDataAnalyzer:
    """Main class for Kenya Sugar Board data analysis with multi-agent architecture"""
    
    def __init__(self, api_key_gemini: str = None, api_key_tavily: str = None):
        """Initialize the multi-agent system"""
        
        # Initialize LLM - using Google Gemini (adjust as needed)
        if api_key_gemini:
            os.environ["GOOGLE_API_KEY"] = api_key_gemini
        
        if api_key_tavily:
            os.environ["TAVILY_API_KEY"] = api_key_tavily
            
        # Initialize the language model
        try:
            self.llm = init_chat_model("gemini/gemini-2.0-flash-exp", temperature=0)
            print("🤖 Google Gemini LLM initialized!")
        except Exception as e:
            print(f"⚠️ Error initializing Gemini: {e}")
            try:
                # Fallback to a different model if available
                self.llm = init_chat_model("gpt-3.5-turbo", temperature=0)
                print("🤖 OpenAI GPT-3.5 LLM initialized as fallback!")
            except Exception as e2:
                print(f"❌ Error initializing LLM: {e2}")
                print("💡 Please ensure you have a valid API key configured")
                raise
        
        # Load and prepare data
        self.load_data()
        self.setup_agents()
        self.create_supervisor()
        
    def load_data(self):
        """Load and prepare Kenya Sugar Board datasets"""
        print("📊 Loading Kenya Sugar Board datasets...")
        
        # Load the CSV files
        try:
            self.ksb_df_1 = pd.read_csv('ksb_data_1.csv')
            self.ksb_df_2 = pd.read_csv('ksb_data_2.csv')
            print(f"✅ Loaded Dataset 1: {self.ksb_df_1.shape[0]} records")
            print(f"✅ Loaded Dataset 2: {self.ksb_df_2.shape[0]} records")
        except FileNotFoundError:
            print("❌ CSV files not found. Please ensure ksb_data_1.csv and ksb_data_2.csv are in the current directory.")
            return
            
        # Combine datasets for comprehensive analysis
        self.combined_df = pd.merge(
            self.ksb_df_1, 
            self.ksb_df_2, 
            on=['Factory', 'Region', 'Year'], 
            how='inner'
        )
        print(f"✅ Combined Dataset: {self.combined_df.shape[0]} records with {self.combined_df.shape[1]} columns")
        
        # Create data context for agents
        self.create_data_context()
        
    def create_data_context(self):
        """Create data context string for agent prompts"""
        
        # Generate data summaries
        df1_head = self.ksb_df_1.head().to_markdown()
        df2_head = self.ksb_df_2.head().to_markdown()
        combined_head = self.combined_df.head().to_markdown()
        
        # Create comprehensive data context
        self.data_context = f"""
**KENYA SUGAR BOARD DATASETS CONTEXT:**

**Dataset 1 (ksb_df_1) - Production & Quality Metrics:**
```python
ksb_df_1.head().to_markdown()
>>> {df1_head}
```

**Dataset 2 (ksb_df_2) - Operational & Financial Metrics:**
```python
ksb_df_2.head().to_markdown()
>>> {df2_head}
```

**Combined Dataset (combined_df) - Complete Analysis View:**
```python
combined_df.head().to_markdown()
>>> {combined_head}
```

**Available Factories:** {', '.join(self.combined_df['Factory'].unique())}
**Regions:** {', '.join(self.combined_df['Region'].unique())}
**Years Available:** {', '.join(map(str, sorted(self.combined_df['Year'].unique())))}

**Key Metrics Available:**
- Production: Crop Yield (tonnes/ha), Sucrose Content (%), Production Quantity (tonnes)
- Operations: Land Area (hectares), Processing Capacity (tonnes/day), Employment
- Financial: Revenue (KES millions)
- Social: Cane Farmers Registered
"""
        
    def setup_agents(self):
        """Setup specialized agents with context quarantine"""
        
        # 1. DATA RETRIEVER AGENT - Analyzes local CSV data
        self.setup_data_retriever_agent()
        
        # 2. WEB RESEARCH AGENT - Performs external research  
        self.setup_web_research_agent()
        
    def setup_data_retriever_agent(self):
        """Setup the data retriever agent with pandas analysis capabilities"""
        
        # Create Python REPL tool with access to datasets
        self.data_tool = PythonAstREPLTool(
            locals={
                "ksb_df_1": self.ksb_df_1,
                "ksb_df_2": self.ksb_df_2, 
                "combined_df": self.combined_df,
                "pd": pd
            }
        )
        
        # Enhanced data retriever prompt
        data_retriever_prompt = f"""You are a specialized Kenya Sugar Board data analyst with access to comprehensive sugar industry datasets.

{self.data_context}

**Your Responsibilities:**
- Analyze sugar production, quality, and operational data using pandas
- Generate insights on factory performance, regional trends, and temporal patterns
- Calculate statistics, rankings, and comparative analyses
- Focus exclusively on data analysis and quantitative insights
- Use only the provided datasets: ksb_df_1, ksb_df_2, and combined_df

**Analysis Guidelines:**
- Always use Python code to analyze the data
- Provide specific numbers, percentages, and rankings
- Compare factories, regions, and years
- Calculate efficiency metrics and performance indicators
- Show trends and patterns in the data

**Constraints:**
- Do NOT perform web research or external data gathering
- Do NOT speculate beyond what the data shows
- Always verify your calculations with the actual dataset
- Reference specific factories, regions, and metrics in your analysis

**Available Libraries:** pandas (as pd), basic Python functions
"""

        # Create the data retriever agent
        self.data_retriever_agent = create_react_agent(
            model=self.llm,
            tools=[self.data_tool],
            name="data_analyst",
            prompt=data_retriever_prompt
        )
        
    def setup_web_research_agent(self):
        """Setup the web research agent with Tavily search"""
        
        # Initialize Tavily Search Tool
        try:
            if TavilySearchResults is not None:
                self.tavily_tool = TavilySearchResults(
                    max_results=5,
                    include_domains=["wikipedia.org", "britannica.com", "fao.org", "worldbank.org"],
                    exclude_domains=["youtube.com", "tiktok.com"],
                )
                print("✅ Tavily search tool initialized")
            else:
                raise ImportError("TavilySearchResults not available")
        except Exception as e:
            print(f"⚠️ Tavily API not configured: {e}")
            print("🔄 Using mock search tool for demonstration")
            # Create a mock search tool for demo purposes
            self.tavily_tool = self.create_mock_search_tool()
        
        # Enhanced web research prompt with context awareness
        web_research_prompt = f"""You are a specialized agricultural and sugar industry research expert.

**CONTEXT - You are analyzing Kenya Sugar Board data:**
{self.data_context}

**Your Responsibilities:**
- Research global sugar industry trends, best practices, and benchmarks
- Find contextual information about Kenya's sugar industry, policies, and challenges
- Gather information about sugar production technologies and optimization strategies
- Research comparative data from other sugar-producing countries
- Find relevant agricultural and economic factors affecting sugar production

**Research Guidelines:**
- Focus on authoritative sources (FAO, World Bank, agricultural institutions)
- Provide current and historical context for the data being analyzed
- Include relevant statistics and benchmarks for comparison
- Research industry standards and best practices
- Find policy and regulatory information affecting Kenya's sugar sector

**Constraints:**
- Do NOT perform data analysis or calculations
- Do NOT access local datasets - focus on external research
- Always cite your sources and provide URLs when available
- Prioritize recent and credible information sources
- Focus on information that adds context to the Kenya Sugar Board analysis

**Search Strategy:**
- Use specific keywords related to sugar industry, Kenya agriculture, production efficiency
- Search for industry reports, government publications, and academic sources
- Look for comparative benchmarks and best practices
"""

        # Create the web research agent
        self.web_research_agent = create_react_agent(
            model=self.llm,
            tools=[self.tavily_tool],
            name="research_specialist",
            prompt=web_research_prompt
        )
        
    def create_mock_search_tool(self):
        """Create a mock search tool for demo purposes when Tavily is not available"""
        from langchain.tools import BaseTool
        
        class MockSearchTool(BaseTool):
            name = "mock_web_search"
            description = "Mock web search for demonstration purposes"
            
            def _run(self, query: str) -> str:
                mock_results = {
                    "kenya sugar": """
                    Kenya Sugar Industry Overview:
                    - Kenya has 9 major sugar factories with total capacity of ~600,000 tonnes annually
                    - Main regions: Western, Nyanza, Central, and Rift Valley
                    - Challenges include aging infrastructure, low productivity, and competition from imports
                    - Government policy supports local production through import restrictions
                    - Average yield in Kenya: ~60-70 tonnes/ha (below global average of 80-100 tonnes/ha)
                    """,
                    "sugar production efficiency": """
                    Global Sugar Production Benchmarks:
                    - Top producers: Brazil (40+ million tonnes), India (35+ million tonnes)
                    - Optimal sucrose content: 12-16% (Kenya average ~12.5%)
                    - Best practice yields: 100-150 tonnes/ha in advanced regions
                    - Processing efficiency: Modern mills process 8,000-12,000 tonnes/day
                    - Technology focus: Precision agriculture, irrigation optimization
                    """,
                    "sugar industry trends": """
                    Current Sugar Industry Trends:
                    - Sustainability focus: Reducing water usage, carbon footprint
                    - Technology adoption: IoT sensors, AI-driven optimization
                    - Market dynamics: Price volatility, health consciousness affecting demand
                    - Policy trends: Support for local production, biofuel integration
                    - Investment priorities: Mill modernization, cane variety improvement
                    """
                }
                
                # Simple keyword matching for mock results
                for key, result in mock_results.items():
                    if key in query.lower():
                        return f"Mock Search Results for '{query}':\n{result}"
                
                return f"Mock Search Results for '{query}':\nGeneral sugar industry information would be found here in a real implementation."
            
            def _arun(self, query: str) -> str:
                return self._run(query)
        
        return MockSearchTool()
        
    def create_supervisor(self):
        """Create the supervisor agent to coordinate other agents"""
        
        # Enhanced supervisor prompt with clear delegation strategy
        supervisor_prompt = f"""You are an intelligent Kenya Sugar Board analysis supervisor managing two specialized experts:

**CONTEXT - Kenya Sugar Board Multi-Agent Analysis:**
{self.data_context}

**Available Specialists:**
1. **data_analyst** - Analyzes local sugar factory datasets, calculates metrics, generates insights
2. **research_specialist** - Researches external sugar industry information, benchmarks, and context

**Your Role:**
- Coordinate comprehensive analysis combining local data insights with industry context
- Delegate tasks based on the expertise required
- Synthesize results from multiple agents into coherent, actionable reports
- Ensure both quantitative analysis and qualitative context are provided

**Delegation Strategy:**
- For data analysis, calculations, factory performance, trends → use **data_analyst**
- For industry context, benchmarks, best practices, external research → use **research_specialist**  
- For comprehensive reports → coordinate both agents sequentially
- Always start with data analysis, then add research context

**Quality Standards:**
- Ensure specific numbers and metrics are provided (not just generalizations)
- Include both local performance data and industry benchmarks
- Provide actionable insights and recommendations
- Tag sources and methodology clearly
- Focus on Kenya Sugar Board strategic decision-making needs

**Important:** You coordinate and synthesize - delegate the actual work to specialists. Never perform analysis or research directly."""

        # Create supervisor workflow
        try:
            if create_supervisor is not None:
                self.workflow = create_supervisor(
                    [self.data_retriever_agent, self.web_research_agent],
                    model=self.llm,
                    prompt=supervisor_prompt
                )
                # Compile the multi-agent application
                self.app = self.workflow.compile()
                print("✅ Multi-agent supervisor system initialized!")
            else:
                print("⚠️ LangGraph supervisor not available, using direct agent coordination")
                self.app = None
                print("✅ Direct agent coordination initialized!")
        except Exception as e:
            print(f"⚠️ Error creating supervisor: {e}")
            print("🔄 Using direct agent coordination as fallback")
            self.app = None
        
    def analyze(self, query: str) -> Dict[str, Any]:
        """Main analysis function using the multi-agent system"""
        
        print(f"\n🔍 **KENYA SUGAR BOARD ANALYSIS REQUEST:**")
        print(f"**Query:** {query}")
        print("=" * 80)
        
        try:
            if self.app is not None:
                # Execute multi-agent analysis with supervisor
                result = self.app.invoke({"messages": [{"role": "user", "content": query}]})
                
                # Format and return results
                messages = result.get('messages', [])
                
                print("\n📋 **ANALYSIS RESULTS:**")
                print("=" * 80)
                
                for i, message in enumerate(messages):
                    if hasattr(message, 'content') and message.content.strip():
                        role = getattr(message, 'role', 'assistant')
                        if role == 'user':
                            continue
                            
                        print(f"\n**Response {i}:**")
                        print(message.content)
                        print("-" * 60)
                
                return {
                    'query': query,
                    'messages': messages,
                    'status': 'success'
                }
            else:
                # Fallback: coordinate agents manually
                print("🔄 Using direct agent coordination (supervisor not available)")
                
                # Step 1: Data analysis
                print("\n📊 **STEP 1: DATA ANALYSIS**")
                print("-" * 60)
                data_result = self.quick_data_analysis(query)
                
                # Step 2: Research
                print("\n🌐 **STEP 2: INDUSTRY RESEARCH**")
                print("-" * 60)
                research_result = self.quick_research(f"Research industry context for: {query}")
                
                # Step 3: Synthesis
                print("\n🎯 **STEP 3: SYNTHESIS**")
                print("-" * 60)
                synthesis = f"""
**COMPREHENSIVE ANALYSIS SUMMARY:**

**Data Analysis Results:**
{data_result}

**Industry Research Context:**
{research_result}

**Key Insights & Recommendations:**
Based on the local data analysis and industry research, this provides a comprehensive view 
of the Kenya Sugar Board situation with actionable insights for strategic decision-making.
"""
                print(synthesis)
                
                return {
                    'query': query,
                    'data_analysis': data_result,
                    'research': research_result,
                    'synthesis': synthesis,
                    'status': 'success_manual'
                }
            
        except Exception as e:
            error_message = f"Error in multi-agent analysis: {e}"
            print(f"\n❌ **ERROR:** {error_message}")
            return {
                'query': query,
                'error': error_message,
                'status': 'error'
            }
    
    def quick_data_analysis(self, query: str) -> str:
        """Quick data analysis using only the data retriever agent"""
        print(f"\n📊 **QUICK DATA ANALYSIS:**")
        print(f"**Query:** {query}")
        print("-" * 60)
        
        try:
            # Use only data retriever agent
            result = self.data_retriever_agent.invoke({"messages": [{"role": "user", "content": query}]})
            return result['messages'][-1].content
        except Exception as e:
            return f"Error in data analysis: {e}"
    
    def quick_research(self, query: str) -> str:
        """Quick research using only the web research agent"""
        print(f"\n🌐 **QUICK RESEARCH:**")
        print(f"**Query:** {query}")
        print("-" * 60)
        
        try:
            # Use only research agent
            result = self.web_research_agent.invoke({"messages": [{"role": "user", "content": query}]})
            return result['messages'][-1].content
        except Exception as e:
            return f"Error in research: {e}"
    
    def get_data_summary(self):
        """Get a summary of available data"""
        summary = f"""
**KENYA SUGAR BOARD DATA SUMMARY:**

**Datasets Available:**
1. **Production & Quality (ksb_df_1):** {self.ksb_df_1.shape[0]} records
   - Columns: {', '.join(self.ksb_df_1.columns)}

2. **Operations & Finance (ksb_df_2):** {self.ksb_df_2.shape[0]} records  
   - Columns: {', '.join(self.ksb_df_2.columns)}

3. **Combined Analysis:** {self.combined_df.shape[0]} records
   - All metrics integrated for comprehensive analysis

**Coverage:**
- **Factories:** {len(self.combined_df['Factory'].unique())} sugar factories
- **Regions:** {len(self.combined_df['Region'].unique())} regions ({', '.join(self.combined_df['Region'].unique())})
- **Time Period:** {self.combined_df['Year'].min()}-{self.combined_df['Year'].max()}

**Sample Queries You Can Ask:**
- "Which top 5 factories performed best in 2025 in terms of yield and sucrose content?"
- "Compare regional performance across all metrics"
- "What are the efficiency trends from 2023 to 2025?"
- "Research global sugar industry benchmarks and compare with Kenya's performance"
- "Analyze correlation between processing capacity and revenue generation"
"""
        return summary

# Example usage and demonstration
def demo_kenya_sugar_analysis():
    """Demonstrate the Kenya Sugar Board multi-agent analysis system"""
    
    print("🇰🇪 KENYA SUGAR BOARD MULTI-AGENT ANALYSIS SYSTEM")
    print("=" * 70)
    
    # Initialize the analyzer (you'll need to provide API keys)
    try:
        analyzer = KenyaSugarDataAnalyzer()
        
        # Show data summary
        print(analyzer.get_data_summary())
        
        # Example comprehensive analysis
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE ANALYSIS EXAMPLE")
        print("=" * 70)
        
        comprehensive_query = """
        Analyze the top 5 performing sugar factories in 2025 based on:
        1. Crop yield and sucrose content
        2. Revenue efficiency 
        3. Processing capacity utilization
        
        Then research how these performance levels compare to global sugar industry standards
        and provide recommendations for improvement.
        """
        
        result = analyzer.analyze(comprehensive_query)
        
        # Example quick analyses
        print("\n" + "=" * 70)
        print("⚡ QUICK ANALYSIS EXAMPLES")
        print("=" * 70)
        
        # Quick data analysis
        data_query = "Calculate the average yield improvement from 2023 to 2025 by region"
        analyzer.quick_data_analysis(data_query)
        
        # Quick research
        research_query = "Find global best practices for sugar mill efficiency and technology"
        analyzer.quick_research(research_query)
        
        return analyzer
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        print("\n💡 **SETUP INSTRUCTIONS:**")
        print("1. Set environment variables:")
        print("   - GOOGLE_API_KEY for Gemini")
        print("   - TAVILY_API_KEY for web search")
        print("2. Ensure CSV files are in current directory:")
        print("   - ksb_data_1.csv")
        print("   - ksb_data_2.csv")
        return None

if __name__ == "__main__":
    demo_kenya_sugar_analysis()