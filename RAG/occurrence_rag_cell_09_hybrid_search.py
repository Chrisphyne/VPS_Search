# Cell 9: Hybrid Search System
"""
Hybrid search that combines:
1. SQL-based queries on relational data (structured queries, analytics, counts)
2. Vector-based semantic search on occurrence content (similarity, meaning)
3. Intelligent routing to determine which method(s) to use
"""

class HybridOccurrenceSearch:
    """Hybrid search system combining SQL and vector search"""
    
    def __init__(self, llm, vector_store: OccurrenceVectorStore, query_builder: JSONBQueryBuilder, schema_manager: FieldSchemaManager):
        self.llm = llm
        self.vector_store = vector_store
        self.query_builder = query_builder
        self.schema_manager = schema_manager
        self.setup_prompts()
    
    def setup_prompts(self):
        """Setup prompts for query classification and SQL generation"""
        
        # Query classification prompt
        self.classifier_prompt = PromptTemplate.from_template("""
Analyze this question about police occurrence data and classify the search approach needed.

Question: {question}

Available search methods:
1. SQL - For counts, statistics, filtering by specific criteria, date ranges, aggregations
2. VECTOR - For finding similar content, semantic search, narrative descriptions
3. HYBRID - For complex questions needing both approaches

Examples:
- "How many vehicle thefts in the last month?" → SQL
- "Show me cases similar to a stolen laptop at university" → VECTOR  
- "What are the trends in cyber crime and show me examples" → HYBRID
- "Find arson cases at schools" → HYBRID
- "Count death cases by cause" → SQL
- "Cases involving stolen electronics" → VECTOR

Classification: Choose ONE: SQL, VECTOR, or HYBRID
Reasoning: Brief explanation of why this approach is best.

Response format:
METHOD: [SQL/VECTOR/HYBRID]
REASONING: [explanation]
""")
        
        # SQL generation prompt
        self.sql_prompt = PromptTemplate.from_template("""
Generate a PostgreSQL query for this question about police occurrence data.

Database Schema:
- sub_module_data: Contains occurrence records with JSONB formData
  * Columns: id, ob_number, submissionDate, sub_moduleId, formData (JSONB), location, urgency, narrative, iprsId
- sub_module: Contains occurrence type definitions
  * Columns: id, name, description, fields (JSONB schema)
- IPRS_Person: Contains person information
  * Columns: id, id_no, first_name, last_name, gender, nationality, email, phone_number

Available JSONB fields in formData (commonly used):
{available_fields}

Important notes:
- Use formData->>'field_name' to extract text values from JSONB
- Use formData->'field_name' for JSON values  
- Join with sub_module to get occurrence type names
- Join with IPRS_Person using iprsId for reporter information
- Always include ob_number in results for reference

Question: {question}

Generate a valid PostgreSQL query:
""")
        
        # Hybrid response prompt
        self.hybrid_prompt = PromptTemplate.from_template("""
You are analyzing police occurrence data. Answer the question using both SQL results and similar occurrence examples.

Question: {question}

SQL Results (structured data):
{sql_results}

Similar Occurrences (semantic matches):
{vector_results}

Available Occurrence Types:
{schema_info}

Instructions:
- Combine insights from both SQL data and similar occurrences
- Mention specific OB numbers when referencing cases
- Provide quantitative insights from SQL and qualitative examples from vector search
- If trends are asked about, analyze patterns in the data
- Be comprehensive but concise

Answer:
""")
    
    def classify_query(self, question: str) -> tuple:
        """Classify the query to determine search approach"""
        try:
            response = self.llm.invoke(self.classifier_prompt.format(question=question))
            content = response.content.strip()
            
            # Extract method and reasoning
            method = "HYBRID"  # Default
            reasoning = "Complex question requiring multiple approaches"
            
            lines = content.split('\n')
            for line in lines:
                if line.startswith('METHOD:'):
                    method = line.split(':', 1)[1].strip()
                elif line.startswith('REASONING:'):
                    reasoning = line.split(':', 1)[1].strip()
            
            return method, reasoning
            
        except Exception as e:
            print(f"Classification error: {e}")
            return "HYBRID", "Error in classification, using hybrid approach"
    
    def generate_sql_query(self, question: str) -> str:
        """Generate SQL query for the question"""
        available_fields = ', '.join(self.schema_manager.get_all_field_names()[:20])
        
        try:
            response = self.llm.invoke(self.sql_prompt.format(
                question=question,
                available_fields=available_fields
            ))
            
            sql_query = response.content.strip()
            
            # Clean up SQL (remove markdown formatting)
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
            
        except Exception as e:
            print(f"SQL generation error: {e}")
            return ""
    
    def execute_sql_search(self, question: str) -> str:
        """Execute SQL-based search"""
        print("🔍 Executing SQL search...")
        
        sql_query = self.generate_sql_query(question)
        if not sql_query:
            return "Could not generate SQL query"
        
        print(f"Generated SQL: {sql_query[:100]}...")
        
        results = self.query_builder.execute_query(sql_query)
        if results:
            return f"SQL Query: {sql_query}\n\nResults: {results}"
        else:
            return "No SQL results found"
    
    def execute_vector_search(self, question: str) -> str:
        """Execute vector-based semantic search"""
        print("🎯 Executing vector search...")
        
        if not self.vector_store.retriever:
            return "Vector store not initialized. Please load occurrences first."
        
        docs = self.vector_store.search_similar_occurrences(question, k=5)
        
        if docs:
            formatted_results = []
            for i, doc in enumerate(docs, 1):
                formatted_results.append(f"Match {i}:")
                formatted_results.append(f"OB: {doc.metadata.get('ob_number', 'N/A')}")
                formatted_results.append(f"Type: {doc.metadata.get('module_name', 'N/A')}")
                formatted_results.append(f"Content: {doc.page_content[:200]}...")
                formatted_results.append("-" * 40)
            
            return "\n".join(formatted_results)
        else:
            return "No similar occurrences found"
    
    def execute_hybrid_search(self, question: str) -> str:
        """Execute hybrid search combining SQL and vector approaches"""
        print("🚀 Executing hybrid search...")
        
        # Get SQL results
        sql_results = self.execute_sql_search(question)
        
        # Get vector results  
        vector_results = self.execute_vector_search(question)
        
        # Get schema info
        schema_info = "\n".join([f"{s['name']}: {s['description']}" for s in self.schema_manager.schemas.values()])
        
        # Generate combined response
        try:
            response = self.llm.invoke(self.hybrid_prompt.format(
                question=question,
                sql_results=sql_results,
                vector_results=vector_results,
                schema_info=schema_info
            ))
            
            return response.content
            
        except Exception as e:
            return f"Error generating hybrid response: {e}\n\nSQL Results:\n{sql_results}\n\nVector Results:\n{vector_results}"
    
    def search(self, question: str) -> str:
        """Main search function that automatically chooses the best approach"""
        print(f"Question: {question}")
        print("=" * 60)
        
        # Classify the query
        method, reasoning = self.classify_query(question)
        print(f"🤖 Analysis: Using {method} approach")
        print(f"💭 Reasoning: {reasoning}")
        print("-" * 60)
        
        # Execute appropriate search
        if method == "SQL":
            return self.execute_sql_search(question)
        elif method == "VECTOR":
            return self.execute_vector_search(question)
        else:  # HYBRID
            return self.execute_hybrid_search(question)

def quick_search(question: str) -> str:
    """Quick search function for easy use"""
    return hybrid_search.search(question)

# Initialize hybrid search system
hybrid_search = HybridOccurrenceSearch(llm, vector_store, query_builder, schema_manager)
print("✅ Hybrid Search System initialized!")

# Test the hybrid search with different types of questions
test_questions = [
    "How many vehicle thefts were reported in the last month?",  # Should use SQL
    "Show me cases similar to stolen electronics at universities",  # Should use VECTOR
    "What are the trends in cyber crime and give me some examples",  # Should use HYBRID
    "Find all arson cases affecting schools",  # Should use HYBRID
    "Count total occurrences by module type"  # Should use SQL
]

print("\n🧪 Testing Hybrid Search System:")
print("=" * 60)

for i, question in enumerate(test_questions, 1):
    print(f"\n{i}. Testing: {question}")
    print("─" * 50)
    
    try:
        method, reasoning = hybrid_search.classify_query(question)
        print(f"🎯 Classified as: {method}")
        print(f"💡 Reasoning: {reasoning}")
        print()
        
        # For demo, just show classification - uncomment below to run full search
        # result = hybrid_search.search(question)
        # print(result[:300] + "..." if len(result) > 300 else result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)

print("""
🎉 Hybrid Search System Ready!

Usage Examples:
==============

# Simple search (automatically chooses best method)
quick_search("How many death cases in the last week?")

# Detailed search with method explanation  
hybrid_search.search("Find cases similar to laptop theft at university")

# The system will automatically:
# 1. Analyze your question
# 2. Choose SQL, VECTOR, or HYBRID approach
# 3. Execute the appropriate search
# 4. Return comprehensive results

Try asking questions like:
- "How many motor vehicle thefts in July 2025?"
- "Show me cases similar to fire incidents at schools"  
- "What are the patterns in cyber crime and show examples"
- "Find all high urgency cases involving stolen electronics"
""")