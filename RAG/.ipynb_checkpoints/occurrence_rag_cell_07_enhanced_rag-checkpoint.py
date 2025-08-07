# Cell 7: Enhanced RAG System
"""
Create the complete RAG system that understands field schemas and provides intelligent answers
"""

class EnhancedOccurrenceRAG:
    """Enhanced RAG system for occurrence data with schema awareness"""
    
    def __init__(self, llm, vector_store: OccurrenceVectorStore, schema_manager: FieldSchemaManager, query_builder: JSONBQueryBuilder):
        self.llm = llm
        self.vector_store = vector_store
        self.schema_manager = schema_manager
        self.query_builder = query_builder
        self.setup_prompts()
    
    def setup_prompts(self):
        """Setup prompts for different types of queries"""
        
        # General RAG prompt with schema awareness
        self.rag_prompt = PromptTemplate.from_template("""
You are an intelligent assistant analyzing police occurrence reports. You have access to:
1. Occurrence data with structured fields
2. Field schemas that define what information is available
3. Historical occurrence patterns

Available Occurrence Types and Their Fields:
{schema_info}

Context from similar occurrences:
{context}

Question: {question}

Instructions:
- Provide accurate information based on the occurrence data
- Mention specific OB numbers when referencing occurrences
- Explain what fields are available for different occurrence types
- If asked about trends, analyze patterns in the data
- If information is not available, clearly state this

Answer:
""")
    
    def get_schema_summary(self) -> str:
        """Get summary of all available schemas"""
        summary = []
        for module_id, schema in self.schema_manager.schemas.items():
            summary.append(f"{schema['name']}: {schema['description']}")
        return "\n".join(summary)
    
    def answer_question(self, question: str) -> str:
        """Answer question using RAG approach"""
        # Get relevant documents
        relevant_docs = self.vector_store.search_similar_occurrences(question)
        
        # Format context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Get schema info
        schema_info = self.get_schema_summary()
        
        # Generate answer
        prompt = self.rag_prompt.format(
            schema_info=schema_info,
            context=context,
            question=question
        )
        
        response = self.llm.invoke(prompt)
        return response.content

# Initialize enhanced RAG system
enhanced_rag = EnhancedOccurrenceRAG(llm, vector_store, schema_manager, query_builder)
print("✅ Enhanced Occurrence RAG System initialized!")

# Test the Enhanced RAG System
test_questions = [
    "What types of vehicle theft have been reported recently?",
    "Tell me about arson cases and what property types are affected",
    "What fields are available when reporting a missing person?",
    "How many death cases have been reported?",
    "What are the common locations for theft incidents?"
]

print("\nTesting Enhanced RAG System")
print("=" * 60)

for i, question in enumerate(test_questions, 1):
    print(f"\n{i}. Question: {question}")
    print("-" * 50)
    
    try:
        answer = enhanced_rag.answer_question(question)
        print(f"Answer: {answer[:300]}{'...' if len(answer) > 300 else ''}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60)