# Cell 10: Advanced Hybrid Search with LangGraph Agent
"""
Advanced hybrid search system that combines:
1. LangGraph SQL Agent (from rag_sql notebook) for complex database interactions
2. Vector search from occurrence data
3. Multiple database source integration
4. React-style agent that can use tools and reason about queries
"""

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from typing import Dict, List, Any, Optional
from langchain.prompts import PromptTemplate

class AdvancedHybridSearchAgent:
    """Advanced hybrid search with LangGraph agent and multiple sources"""
    
    def __init__(self, llm, db, vector_store, schema_manager):
        self.llm = llm
        self.db = db
        self.vector_store = vector_store
        self.schema_manager = schema_manager
        self.setup_agent()
        self.setup_prompts()
    
    def setup_agent(self):
        """Setup the LangGraph SQL agent with tools"""
        
        # Create SQL toolkit
        self.sql_toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.sql_tools = self.sql_toolkit.get_tools()
        
        # Add custom vector search tool
        self.vector_tool = self.create_vector_search_tool()
        
        # Combine all tools
        self.all_tools = self.sql_tools + [self.vector_tool]
        
        # System message for the agent
        self.system_message = """
You are an intelligent police occurrence data analyst with access to multiple search capabilities.

You have access to these tools:
1. SQL Database Tools - For structured queries, statistics, counts, filtering
   - sql_db_list_tables: List all available tables
   - sql_db_schema: Get table schemas and sample data
   - sql_db_query: Execute SQL queries
   - sql_db_query_checker: Validate SQL queries

2. Vector Search Tool - For semantic similarity and content-based search
   - vector_search_occurrences: Find similar occurrences based on content

Database Schema Overview:
- sub_module_data: Main occurrence records with JSONB formData
- sub_module: Occurrence type definitions and field schemas  
- IPRS_Person: Person/reporter information
- Additional tables may be available (use sql_db_list_tables to explore)

JSONB formData contains dynamic fields based on occurrence type:
- Vehicle theft: Make, Model, Color, Registration number, etc.
- Death cases: Cause of death, Gender, Contact person, etc.
- Arson: Property type, Owner information, etc.
- Cyber crime: Incident type, Suspect details, etc.

Important Guidelines:
1. ALWAYS start by understanding what tables are available if you're unsure
2. For counts and statistics, use SQL queries
3. For finding similar cases or content-based search, use vector search
4. For complex questions, combine both approaches
5. Always include ob_number in results for reference
6. Use formData->>'field_name' to extract JSONB text values
7. Join with IPRS_Person using iprsId for reporter information
8. Be thorough but concise in your analysis

When answering:
- Provide specific OB numbers when referencing cases
- Include quantitative insights when available
- Give concrete examples from the data
- Explain your reasoning and approach
"""
        
        # Create the react agent
        self.agent_executor = create_react_agent(self.llm, self.all_tools, prompt=self.system_message)
        
    def create_vector_search_tool(self):
        """Create a custom vector search tool for the agent"""
        from langchain.tools import BaseTool
        
        class VectorSearchTool(BaseTool):
            name = "vector_search_occurrences"
            description = """
            Search for similar occurrences using semantic similarity.
            Input should be a descriptive query about the type of occurrence you're looking for.
            Examples: 'stolen laptop at university', 'fire at school', 'vehicle theft at shopping center'
            Returns the most similar occurrence records with OB numbers and details.
            """
            
            def __init__(self, vector_store):
                super().__init__()
                self.vector_store = vector_store
            
            def _run(self, query: str) -> str:
                """Execute vector search"""
                try:
                    if not self.vector_store.retriever:
                        return "Vector store not initialized. Please load occurrences first."
                    
                    docs = self.vector_store.search_similar_occurrences(query, k=5)
                    
                    if not docs:
                        return "No similar occurrences found."
                    
                    results = []
                    for i, doc in enumerate(docs, 1):
                        results.append(f"Match {i}:")
                        results.append(f"OB Number: {doc.metadata.get('ob_number', 'N/A')}")
                        results.append(f"Type: {doc.metadata.get('module_name', 'N/A')}")
                        results.append(f"Date: {doc.metadata.get('submission_date', 'N/A')}")
                        results.append(f"Urgency: {doc.metadata.get('urgency', 'N/A')}")
                        results.append(f"Content: {doc.page_content[:300]}...")
                        results.append("-" * 50)
                    
                    return "\n".join(results)
                    
                except Exception as e:
                    return f"Error in vector search: {e}"
            
            def _arun(self, query: str) -> str:
                """Async version"""
                return self._run(query)
        
        return VectorSearchTool(self.vector_store)
    
    def setup_prompts(self):
        """Setup additional prompts for query enhancement"""
        
        self.query_enhancer_prompt = PromptTemplate.from_template("""
Enhance this user question to be more specific for police occurrence data analysis.

Original question: {question}

Available data includes:
- Occurrence records with details like location, urgency, dates
- JSONB form data with specific fields per occurrence type
- Reporter information (names, ID numbers, contact details)
- Occurrence types: Arson, Assault, Burglary, Cyber Crime, Death, Homicide, Motor Vehicle Theft, Missing Person, Rape, Robbery, Stolen Lost Item, GBV

Enhanced question with more context and specificity:
""")
    
    def enhance_query(self, question: str) -> str:
        """Enhance the user query for better processing"""
        try:
            response = self.llm.invoke(self.query_enhancer_prompt.format(question=question))
            enhanced = response.content.strip()
            return enhanced if enhanced else question
        except:
            return question
    
    def search(self, question: str, enhance_query: bool = True) -> str:
        """Main search function using the agent"""
        
        print(f"🔍 Original Question: {question}")
        print("=" * 80)
        
        # Enhance the query if requested
        if enhance_query:
            enhanced_question = self.enhance_query(question)
            if enhanced_question != question:
                print(f"🎯 Enhanced Question: {enhanced_question}")
                print("-" * 80)
                question = enhanced_question
        
        # Execute using the agent
        try:
            print("🤖 Agent is analyzing and searching...")
            
            # Create the human message
            messages = [{"role": "user", "content": question}]
            
            # Stream the agent execution
            response_parts = []
            for step in self.agent_executor.stream(
                {"messages": messages}, 
                stream_mode="values"
            ):
                if step["messages"]:
                    last_message = step["messages"][-1]
                    if hasattr(last_message, 'content'):
                        response_parts.append(last_message.content)
            
            # Get the final response
            if response_parts:
                return response_parts[-1]
            else:
                return "No response generated"
                
        except Exception as e:
            return f"Error executing search: {e}"
    
    def quick_sql_search(self, question: str) -> str:
        """Quick SQL-only search"""
        print("🔍 Executing SQL-focused search...")
        
        sql_question = f"Use SQL queries to answer: {question}"
        return self.search(sql_question, enhance_query=False)
    
    def quick_vector_search(self, question: str) -> str:
        """Quick vector-only search"""
        print("🎯 Executing vector-focused search...")
        
        vector_question = f"Use vector search to find similar occurrences for: {question}"
        return self.search(vector_question, enhance_query=False)
    
    def multi_source_search(self, question: str, sources: List[str] = None) -> str:
        """Search across multiple specified sources"""
        if sources is None:
            sources = ["sql", "vector"]
        
        print(f"🚀 Executing multi-source search across: {', '.join(sources)}")
        
        multi_question = f"""
        Answer this question using multiple data sources: {question}
        
        Available sources: {', '.join(sources)}
        - Use SQL for structured data, counts, statistics
        - Use vector search for similar cases and content-based matching
        - Combine insights from all sources for a comprehensive answer
        """
        
        return self.search(multi_question, enhance_query=True)

def advanced_search(question: str) -> str:
    """Quick function for advanced hybrid search"""
    return advanced_agent.search(question)

def sql_search(question: str) -> str:
    """Quick function for SQL-focused search"""
    return advanced_agent.quick_sql_search(question)

def vector_search(question: str) -> str:
    """Quick function for vector-focused search"""
    return advanced_agent.quick_vector_search(question)

def multi_search(question: str, sources: List[str] = None) -> str:
    """Quick function for multi-source search"""
    return advanced_agent.multi_source_search(question, sources)

# Initialize the advanced hybrid search agent
print("🚀 Initializing Advanced Hybrid Search Agent...")
advanced_agent = AdvancedHybridSearchAgent(llm, db, vector_store, schema_manager)
print("✅ Advanced Hybrid Search Agent initialized!")

# Test the agent capabilities
print("\n🧪 Testing Agent Capabilities:")
print("=" * 60)

# Test different types of searches
test_scenarios = [
    {
        "name": "SQL Analytics Test",
        "question": "How many occurrences were reported in the last 30 days by type?",
        "method": "sql_search"
    },
    {
        "name": "Vector Similarity Test", 
        "question": "Find cases similar to stolen electronics",
        "method": "vector_search"
    },
    {
        "name": "Multi-Source Analysis Test",
        "question": "What are the patterns in vehicle theft and show me examples",
        "method": "multi_search"
    }
]

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\n{i}. {scenario['name']}")
    print("─" * 50)
    print(f"Question: {scenario['question']}")
    print(f"Method: {scenario['method']}")
    
    # For demo, just show the setup - uncomment to run actual tests
    # try:
    #     if scenario['method'] == 'sql_search':
    #         result = sql_search(scenario['question'])
    #     elif scenario['method'] == 'vector_search':
    #         result = vector_search(scenario['question'])
    #     else:
    #         result = multi_search(scenario['question'])
    #     
    #     print(f"Result: {result[:200]}...")
    # except Exception as e:
    #     print(f"Error: {e}")
    
    print("\n" + "=" * 60)

print("""
🎉 Advanced Hybrid Search Agent Ready!

Available Functions:
==================

1. advanced_search(question) - Full agent with reasoning and tool selection
2. sql_search(question) - SQL-focused analysis  
3. vector_search(question) - Vector similarity search
4. multi_search(question, sources) - Multi-source comprehensive search

Examples:
=========

# Full agent reasoning
advanced_search("What are the trends in cyber crime?")

# SQL analytics
sql_search("How many vehicle thefts in July 2025?")

# Vector similarity  
vector_search("Find cases like stolen laptop at university")

# Multi-source analysis
multi_search("Analyze arson patterns with examples", ["sql", "vector"])

Features:
=========
✅ Intelligent tool selection and reasoning
✅ SQL database exploration and querying
✅ Vector semantic search integration
✅ Multi-step analysis capabilities
✅ Error handling and validation
✅ Comprehensive result synthesis

The agent can:
- Explore database schema autonomously
- Generate and validate SQL queries
- Perform vector similarity searches
- Combine multiple data sources
- Reason about complex questions
- Provide detailed explanations
""")

# Show available tools
print("\nAvailable Tools:")
print("=" * 30)
for tool in advanced_agent.all_tools:
    print(f"- {tool.name}: {tool.description[:60]}...")

print(f"\nTotal tools available: {len(advanced_agent.all_tools)}")
print("Ready for advanced occurrence data analysis! 🚀")