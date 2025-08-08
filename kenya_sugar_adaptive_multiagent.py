# Kenya Sugar Board Adaptive Multi-Agent Analysis System
"""
Adaptive Multi-Agent system that automatically detects and works with your CSV files.
Supports:
- kenyan_sugar_weekly_factory.csv
- kenyan_sugar_weekly_factory_agg.csv
- Any other CSV files with sugar/factory data

This system implements context quarantine with specialized agents:
1. Data Retriever Agent - Analyzes local CSV data
2. Web Research Agent - Performs external research  
3. Supervisor Agent - Coordinates and synthesizes results
"""

import pandas as pd
import os
import glob
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Try different import paths for dependencies
try:
    from langchain.chat_models import init_chat_model
except ImportError:
    from langchain_community.chat_models import init_chat_model

from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool

# Try different import paths for Tavily
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
except ImportError:
    try:
        from langchain_tavily import TavilySearchResults
    except ImportError:
        TavilySearchResults = None

from langgraph.prebuilt import create_react_agent

# Try different import paths for supervisor
try:
    from langgraph_supervisor import create_supervisor
except ImportError:
    create_supervisor = None

class AdaptiveKenyaSugarAnalyzer:
    """Adaptive multi-agent system for Kenya Sugar Board data analysis"""
    
    def __init__(self, data_directory: str = ".", api_key_gemini: str = None, api_key_tavily: str = None):
        """Initialize the adaptive multi-agent system"""
        
        # Store directory to search for CSV files
        self.data_directory = data_directory
        
        # Initialize LLM
        if api_key_gemini:
            os.environ["GOOGLE_API_KEY"] = api_key_gemini
        if api_key_tavily:
            os.environ["TAVILY_API_KEY"] = api_key_tavily
            
        # Initialize Google Gemini language model (using direct API, not Vertex AI)
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                temperature=0,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            print("🤖 Google Gemini LLM initialized!")
        except Exception as e:
            print(f"❌ Error initializing Google Gemini: {e}")
            print("💡 Please ensure you have set GOOGLE_API_KEY environment variable")
            print("💡 Get your API key from: https://aistudio.google.com/app/apikey")
            print("💡 You may need to install: pip install langchain-google-genai")
            raise
                
        # Auto-detect and load data
        self.auto_detect_and_load_data()
        self.setup_agents()
        self.create_supervisor()
        
    def auto_detect_and_load_data(self):
        """Automatically detect and load Kenyan sugar CSV files"""
        print("🔍 Auto-detecting Kenya Sugar Board datasets...")
        
        # Define possible file patterns
        target_files = [
            "kenyan_sugar_weekly_factory.csv",
            "kenyan_sugar_weekly_factory_agg.csv"
        ]
        
        # Search patterns (case insensitive)
        search_patterns = [
            "*kenyan*sugar*.csv",
            "*sugar*kenya*.csv", 
            "*sugar*factory*.csv",
            "*factory*sugar*.csv",
            "*.csv"  # Fallback: all CSV files
        ]
        
        found_files = {}
        
        # Search in current directory and subdirectories
        search_dirs = [self.data_directory, f"{self.data_directory}/RAG", f"{self.data_directory}/data"]
        
        for directory in search_dirs:
            if not os.path.exists(directory):
                continue
                
            print(f"🔍 Searching in: {directory}")
            
            # First, try to find exact target files
            for target_file in target_files:
                file_path = os.path.join(directory, target_file)
                if os.path.exists(file_path):
                    found_files[target_file] = file_path
                    print(f"✅ Found target file: {file_path}")
            
            # Then try pattern matching
            if len(found_files) < 2:  # If we don't have both files
                for pattern in search_patterns:
                    matches = glob.glob(os.path.join(directory, pattern))
                    for match in matches:
                        filename = os.path.basename(match).lower()
                        if any(keyword in filename for keyword in ['sugar', 'factory', 'kenya']):
                            found_files[os.path.basename(match)] = match
                            print(f"✅ Found potential file: {match}")
        
        # Load the files
        self.datasets = {}
        self.data_context = ""
        
        if found_files:
            print(f"\n📊 Loading {len(found_files)} dataset(s)...")
            
            for filename, filepath in found_files.items():
                try:
                    df = pd.read_csv(filepath)
                    self.datasets[filename] = df
                    print(f"✅ Loaded {filename}: {df.shape[0]} records, {df.shape[1]} columns")
                    
                    # Show a preview
                    print(f"📋 Columns in {filename}: {', '.join(df.columns.tolist()[:10])}{'...' if len(df.columns) > 10 else ''}")
                    
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
            
            if self.datasets:
                self.create_adaptive_data_context()
                return
        
        # Fallback: create sample data if no files found
        print("⚠️ No Kenya Sugar Board CSV files found.")
        print("💡 Creating sample data for demonstration...")
        self.create_sample_data()
        
    def create_sample_data(self):
        """Create sample data when real files aren't available"""
        print("📊 Creating sample Kenya Sugar Board data...")
        
        # Sample data matching expected structure
        sample_data_1 = {
            'Factory': ['Mumias Sugar Company', 'South Nyanza Sugar Company', 'Chemelil Sugar Company'] * 10,
            'Region': ['Western', 'Nyanza', 'Nyanza'] * 10,
            'Week': list(range(1, 31)),
            'Year': [2023] * 15 + [2024] * 15,
            'Weekly_Production_Tonnes': [1200, 980, 1100] * 10,
            'Sucrose_Content_Percent': [12.5, 11.9, 12.3] * 10,
            'Cane_Crushed_Tonnes': [9500, 8200, 8900] * 10
        }
        
        sample_data_2 = {
            'Factory': ['Mumias Sugar Company', 'South Nyanza Sugar Company', 'Chemelil Sugar Company'] * 10,
            'Region': ['Western', 'Nyanza', 'Nyanza'] * 10,
            'Week': list(range(1, 31)),
            'Year': [2023] * 15 + [2024] * 15,
            'Weekly_Revenue_KES': [2400000, 1960000, 2200000] * 10,
            'Employment_Count': [3200, 2800, 3000] * 10,
            'Processing_Capacity_Utilization': [0.85, 0.78, 0.82] * 10
        }
        
        self.datasets = {
            'kenyan_sugar_weekly_factory.csv': pd.DataFrame(sample_data_1),
            'kenyan_sugar_weekly_factory_agg.csv': pd.DataFrame(sample_data_2)
        }
        
        print("✅ Sample data created!")
        for name, df in self.datasets.items():
            print(f"📊 {name}: {df.shape[0]} records, {df.shape[1]} columns")
        
        self.create_adaptive_data_context()
        
    def create_adaptive_data_context(self):
        """Create data context from available datasets"""
        
        context_parts = ["**KENYA SUGAR BOARD DATASETS CONTEXT:**\n"]
        
        # Add information about each dataset
        for i, (filename, df) in enumerate(self.datasets.items(), 1):
            context_parts.append(f"**Dataset {i} ({filename}):**")
            context_parts.append(f"```python")
            context_parts.append(f"{filename.replace('.csv', '_df')}.head().to_markdown()")
            context_parts.append(f">>> {df.head().to_markdown()}")
            context_parts.append(f"```\n")
            
            # Add column information
            context_parts.append(f"**Columns:** {', '.join(df.columns.tolist())}")
            context_parts.append(f"**Records:** {df.shape[0]} rows")
            
            # Add unique values for key columns
            if 'Factory' in df.columns:
                context_parts.append(f"**Factories:** {', '.join(df['Factory'].unique())}")
            if 'Region' in df.columns:
                context_parts.append(f"**Regions:** {', '.join(df['Region'].unique())}")
            if 'Year' in df.columns:
                years = sorted(df['Year'].unique()) if df['Year'].dtype in ['int64', 'float64'] else df['Year'].unique()
                context_parts.append(f"**Years:** {', '.join(map(str, years))}")
            
            context_parts.append("")
        
        # Try to combine datasets if they share common columns
        self.combined_df = None
        if len(self.datasets) >= 2:
            try:
                dfs = list(self.datasets.values())
                common_cols = set(dfs[0].columns)
                for df in dfs[1:]:
                    common_cols = common_cols.intersection(set(df.columns))
                
                if len(common_cols) >= 2:  # Need at least 2 columns to merge
                    merge_cols = list(common_cols)[:3]  # Use up to 3 columns for merging
                    self.combined_df = dfs[0]
                    for df in dfs[1:]:
                        self.combined_df = pd.merge(self.combined_df, df, on=merge_cols, how='inner')
                    
                    context_parts.append("**Combined Dataset:**")
                    context_parts.append(f"```python")
                    context_parts.append(f"combined_df.head().to_markdown()")
                    context_parts.append(f">>> {self.combined_df.head().to_markdown()}")
                    context_parts.append(f"```")
                    context_parts.append(f"**Combined Records:** {self.combined_df.shape[0]} rows, {self.combined_df.shape[1]} columns")
                    
            except Exception as e:
                print(f"⚠️ Could not combine datasets: {e}")
        
        self.data_context = "\n".join(context_parts)
        print("✅ Adaptive data context created!")
        
    def setup_agents(self):
        """Setup specialized agents with adaptive context"""
        
        # 1. DATA RETRIEVER AGENT
        self.setup_data_retriever_agent()
        
        # 2. WEB RESEARCH AGENT
        self.setup_web_research_agent()
        
    def setup_data_retriever_agent(self):
        """Setup the data retriever agent with adaptive datasets"""
        
        # Create locals dict with all available datasets
        tool_locals = {"pd": pd}
        
        # Add each dataset to the tool environment
        for filename, df in self.datasets.items():
            var_name = filename.replace('.csv', '_df').replace('-', '_').replace(' ', '_')
            tool_locals[var_name] = df
            
        # Add combined dataset if available
        if self.combined_df is not None:
            tool_locals['combined_df'] = self.combined_df
        
        # Create Python REPL tool
        self.data_tool = PythonAstREPLTool(locals=tool_locals)
        
        # Enhanced data retriever prompt
        available_vars = ", ".join(tool_locals.keys())
        data_retriever_prompt = f"""You are a specialized Kenya Sugar Board data analyst with access to sugar industry datasets.

{self.data_context}

**Your Responsibilities:**
- Analyze sugar production, operational, and financial data using pandas
- Generate insights on factory performance, regional trends, and temporal patterns  
- Calculate statistics, rankings, and comparative analyses
- Focus exclusively on data analysis and quantitative insights
- Use the provided datasets: {available_vars}

**Analysis Guidelines:**
- Always use Python code to analyze the data
- Provide specific numbers, percentages, and rankings
- Compare factories, regions, and time periods when available
- Calculate efficiency metrics and performance indicators
- Show trends and patterns in the data
- Handle both weekly and aggregated data appropriately

**Constraints:**
- Do NOT perform web research or external data gathering
- Do NOT speculate beyond what the data shows
- Always verify your calculations with the actual dataset
- Reference specific factories, regions, and metrics in your analysis

**Available Variables:** {available_vars}
**Available Libraries:** pandas (as pd), basic Python functions
"""

        # Create the data retriever agent
        self.data_retriever_agent = create_react_agent(
            model=self.llm,
            tools=[self.data_tool],
            name="data_analyst",
            prompt=data_retriever_prompt
        )
        
        print("✅ Adaptive Data Retriever Agent initialized!")
        
    def setup_web_research_agent(self):
        """Setup the web research agent with Kenya sugar industry focus"""
        
        # Initialize search tool with fallback
        try:
            if TavilySearchResults is not None:
                self.tavily_tool = TavilySearchResults(
                    max_results=5,
                    include_domains=["wikipedia.org", "britannica.com", "fao.org", "worldbank.org", "business.co.ke"],
                    exclude_domains=["youtube.com", "tiktok.com"],
                )
                print("✅ Tavily search tool initialized")
            else:
                raise ImportError("TavilySearchResults not available")
        except Exception as e:
            print(f"⚠️ Tavily API not configured: {e}")
            print("🔄 Using enhanced mock search for Kenya sugar industry")
            self.tavily_tool = self.create_enhanced_mock_search_tool()

        # Enhanced web research prompt
        web_research_prompt = f"""You are a specialized agricultural and sugar industry research expert focusing on Kenya.

**CONTEXT - You are analyzing Kenya Sugar Board data:**
{self.data_context}

**Your Responsibilities:**
- Research Kenya's sugar industry trends, policies, and challenges
- Find global sugar industry best practices and benchmarks
- Gather information about sugar production technologies and optimization
- Research comparative data from other sugar-producing countries  
- Find relevant agricultural and economic factors affecting Kenya's sugar sector

**Research Guidelines:**
- Focus on authoritative sources (government, FAO, World Bank, industry reports)
- Provide current context for Kenya's sugar industry specifically
- Include relevant statistics and benchmarks for comparison
- Research industry standards and best practices applicable to Kenya
- Find policy and regulatory information affecting Kenya's sugar sector

**Constraints:**
- Do NOT perform data analysis or calculations
- Do NOT access local datasets - focus on external research
- Always cite your sources when available
- Prioritize recent and credible information sources
- Focus on information that adds context to the Kenya Sugar Board analysis

**Search Strategy:**
- Use keywords: Kenya sugar industry, sugar production efficiency, East Africa sugar
- Search for government reports, industry publications, academic sources
- Look for comparative benchmarks and regional best practices
"""

        # Create the web research agent
        self.web_research_agent = create_react_agent(
            model=self.llm,
            tools=[self.tavily_tool],
            name="research_specialist", 
            prompt=web_research_prompt
        )
        
        print("✅ Kenya-focused Web Research Agent initialized!")
        
    def create_enhanced_mock_search_tool(self):
        """Create enhanced mock search tool with Kenya sugar industry focus"""
        from langchain.tools import BaseTool
        
        class EnhancedMockSearchTool(BaseTool):
            name = "kenya_sugar_search"
            description = "Enhanced mock search for Kenya sugar industry information"
            
            def _run(self, query: str) -> str:
                kenya_sugar_results = {
                    "kenya sugar industry": """
                    Kenya Sugar Industry Overview (2024):
                    - Kenya has 10 operational sugar factories with combined capacity of ~650,000 tonnes annually
                    - Main sugar zones: Western Kenya (60%), Nyanza (25%), Central (10%), Coast (5%)
                    - Key challenges: aging infrastructure, low cane yields (~50-60 tonnes/ha vs global 80-100)
                    - Government initiatives: Sugar Task Force recommendations, import duty protection
                    - Major factories: Mumias (largest), Chemelil, South Nyanza, West Kenya, Nzoia
                    - Employment: ~250,000 direct and indirect jobs in sugar value chain
                    """,
                    
                    "sugar production efficiency": """
                    Global Sugar Production Benchmarks vs Kenya:
                    - World average cane yield: 80-100 tonnes/ha (Kenya: 50-60 tonnes/ha)
                    - Optimal sucrose content: 12-16% (Kenya average: 10-13%)
                    - Modern mill processing: 8,000-15,000 tonnes/day (Kenya mills: 2,000-6,000)
                    - Recovery rate benchmark: 10-12% (Kenya: 8-10%)
                    - Best practice countries: Brazil (150+ tonnes/ha), Australia (100+ tonnes/ha)
                    - Technology gaps: Irrigation, mechanization, variety improvement needed
                    """,
                    
                    "sugar industry trends": """
                    Current Sugar Industry Trends Affecting Kenya:
                    - Regional integration: COMESA sugar trade protocols
                    - Technology adoption: Precision agriculture, drip irrigation systems
                    - Sustainability focus: Bagasse co-generation, waste management
                    - Market dynamics: Competition from COMESA imports, local consumption growth
                    - Investment trends: Private sector partnerships, mill modernization
                    - Climate resilience: Drought-resistant varieties, water management
                    """,
                    
                    "kenya agriculture policy": """
                    Kenya Sugar Sector Policy Framework:
                    - Sugar Act 2001 and regulations (under review)
                    - Kenya Sugar Board: Regulatory oversight and industry development
                    - National Sugar Policy: Focus on productivity and competitiveness
                    - Big Four Agenda: Food security and manufacturing sector growth
                    - County government role: Agriculture extension services, farmer support
                    - Research institutions: KALRO sugar research programs
                    """
                }
                
                # Enhanced keyword matching
                query_lower = query.lower()
                for key, result in kenya_sugar_results.items():
                    if any(word in query_lower for word in key.split()):
                        return f"Kenya Sugar Industry Research Results for '{query}':\n{result}"
                
                # General fallback
                return f"""Kenya Sugar Industry Research for '{query}':
                
                General Context: Kenya's sugar industry faces both challenges and opportunities. 
                The sector supports hundreds of thousands of livelihoods but struggles with 
                productivity issues compared to global standards. Government policy focuses on 
                revitalization through technology adoption, infrastructure improvement, and 
                enhanced competitiveness against regional imports.
                
                Key Areas for Improvement:
                - Cane productivity (currently 50-60 tonnes/ha vs global 80-100+)
                - Mill efficiency and processing capacity
                - Irrigation and mechanization adoption
                - Value chain integration and farmer support
                - Policy framework modernization
                """
            
            def _arun(self, query: str) -> str:
                return self._run(query)
        
        return EnhancedMockSearchTool()
        
    def create_supervisor(self):
        """Create the supervisor agent to coordinate other agents"""
        
        supervisor_prompt = f"""You are an intelligent Kenya Sugar Board analysis supervisor managing two specialized experts:

**CONTEXT - Kenya Sugar Board Multi-Agent Analysis:**
{self.data_context}

**Available Specialists:**
1. **data_analyst** - Analyzes local sugar factory datasets, calculates metrics, generates insights
2. **research_specialist** - Researches Kenya sugar industry information, benchmarks, and context

**Your Role:**
- Coordinate comprehensive analysis combining local data insights with industry context
- Delegate tasks based on the expertise required
- Synthesize results from multiple agents into coherent, actionable reports
- Ensure both quantitative analysis and qualitative context are provided

**Delegation Strategy:**
- For data analysis, calculations, factory performance, trends → use **data_analyst**
- For industry context, benchmarks, best practices, policy research → use **research_specialist**
- For comprehensive reports → coordinate both agents sequentially
- Always start with data analysis, then add research context

**Quality Standards:**
- Ensure specific numbers and metrics are provided (not just generalizations)
- Include both local performance data and Kenya industry context
- Provide actionable insights and recommendations
- Tag sources and methodology clearly
- Focus on Kenya Sugar Board strategic decision-making needs

**Important:** You coordinate and synthesize - delegate the actual work to specialists."""

        # Create supervisor workflow with fallback
        try:
            if create_supervisor is not None:
                self.workflow = create_supervisor(
                    [self.data_retriever_agent, self.web_research_agent],
                    model=self.llm,
                    prompt=supervisor_prompt
                )
                self.app = self.workflow.compile()
                print("✅ Multi-agent supervisor system initialized!")
            else:
                print("⚠️ LangGraph supervisor not available, using direct coordination")
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
                
                return {'query': query, 'messages': messages, 'status': 'success'}
            else:
                # Fallback: coordinate agents manually
                print("🔄 Using direct agent coordination")
                
                # Step 1: Data analysis
                print("\n📊 **STEP 1: DATA ANALYSIS**")
                print("-" * 60)
                data_result = self.quick_data_analysis(query)
                
                # Step 2: Research
                print("\n🌐 **STEP 2: KENYA SUGAR INDUSTRY RESEARCH**")
                print("-" * 60)
                research_result = self.quick_research(f"Research Kenya sugar industry context for: {query}")
                
                # Step 3: Synthesis
                print("\n🎯 **STEP 3: COMPREHENSIVE SYNTHESIS**")
                print("-" * 60)
                synthesis = f"""
**COMPREHENSIVE KENYA SUGAR BOARD ANALYSIS:**

**Local Data Analysis:**
{data_result}

**Industry Context & Benchmarks:**
{research_result}

**Strategic Insights & Recommendations:**
Based on the data analysis and industry research, this provides actionable insights 
for Kenya Sugar Board strategic decision-making, combining local performance data 
with industry context and global best practices.
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
            return {'query': query, 'error': error_message, 'status': 'error'}
    
    def quick_data_analysis(self, query: str) -> str:
        """Quick data analysis using only the data retriever agent"""
        try:
            result = self.data_retriever_agent.invoke({"messages": [{"role": "user", "content": query}]})
            content = result['messages'][-1].content
            print(content)
            return content
        except Exception as e:
            error_msg = f"Error in data analysis: {e}"
            print(error_msg)
            return error_msg

    def quick_research(self, query: str) -> str:
        """Quick research using only the web research agent"""
        try:
            result = self.web_research_agent.invoke({"messages": [{"role": "user", "content": query}]})
            content = result['messages'][-1].content
            print(content)
            return content
        except Exception as e:
            error_msg = f"Error in research: {e}"
            print(error_msg)
            return error_msg
    
    def get_data_summary(self):
        """Get a summary of available data"""
        summary_parts = [
            "**ADAPTIVE KENYA SUGAR BOARD DATA SUMMARY:**",
            ""
        ]
        
        for i, (filename, df) in enumerate(self.datasets.items(), 1):
            summary_parts.extend([
                f"**Dataset {i} ({filename}):** {df.shape[0]} records, {df.shape[1]} columns",
                f"   - Columns: {', '.join(df.columns.tolist())}",
                ""
            ])
        
        if self.combined_df is not None:
            summary_parts.extend([
                f"**Combined Analysis:** {self.combined_df.shape[0]} records, {self.combined_df.shape[1]} columns",
                f"   - Integrated metrics for comprehensive analysis",
                ""
            ])
        
        summary_parts.extend([
            "**Sample Queries You Can Ask:**",
            "- 'Analyze weekly production trends by factory'",
            "- 'Compare regional performance and efficiency metrics'", 
            "- 'Research Kenya sugar industry competitiveness vs global standards'",
            "- 'Which factories show the best improvement trends?'",
            "- 'What are the key challenges facing Kenya's sugar sector?'"
        ])
        
        return "\n".join(summary_parts)

# Convenience functions
def create_analyzer(data_dir: str = ".", search_subdirs: bool = True) -> AdaptiveKenyaSugarAnalyzer:
    """Create an adaptive analyzer that searches for CSV files"""
    print("🇰🇪 ADAPTIVE KENYA SUGAR BOARD MULTI-AGENT ANALYSIS SYSTEM")
    print("=" * 70)
    
    if search_subdirs:
        print("🔍 Searching for Kenya Sugar Board CSV files...")
        
    return AdaptiveKenyaSugarAnalyzer(data_directory=data_dir)

# Demo function
def demo_adaptive_analysis():
    """Demonstrate the adaptive multi-agent analysis system"""
    
    analyzer = create_analyzer()
    
    # Show data summary
    print(analyzer.get_data_summary())
    
    # Example analysis
    print("\n" + "=" * 70)
    print("📊 EXAMPLE COMPREHENSIVE ANALYSIS")
    print("=" * 70)
    
    example_query = """
    Analyze the performance of Kenya's sugar factories based on available data:
    1. Production efficiency and trends
    2. Regional performance comparison
    3. How Kenya compares to global sugar industry standards
    
    Provide specific recommendations for improvement.
    """
    
    result = analyzer.analyze(example_query)
    return analyzer

if __name__ == "__main__":
    demo_adaptive_analysis()