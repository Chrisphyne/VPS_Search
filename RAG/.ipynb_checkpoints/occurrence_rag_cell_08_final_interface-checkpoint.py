# Cell 8: Final Interface and Usage Examples
"""
Create a simple interface for querying your occurrence data and demonstrate usage
"""

def query_occurrences(question: str):
    """
    Simple function to query your occurrence data
    
    Examples:
    - query_occurrences("What vehicle thefts happened at Sarit Center?")
    - query_occurrences("Show me recent fire incidents")
    - query_occurrences("What fields are available for death reports?")
    """
    try:
        answer = enhanced_rag.answer_question(question)
        return answer
    except Exception as e:
        return f"Error processing question: {e}"

def get_field_info(module_name: str):
    """
    Get detailed field information for a specific occurrence type
    
    Examples:
    - get_field_info("Motor Vehicle Theft")
    - get_field_info("Arson")
    - get_field_info("Missing Person")
    """
    for module_id, schema in schema_manager.schemas.items():
        if schema['name'].lower() == module_name.lower():
            return schema_manager.create_field_description(module_id)
    
    return f"Module '{module_name}' not found. Available modules: {', '.join([s['name'] for s in schema_manager.schemas.values()])}"

# Test field-specific schema queries
schema_questions = [
    "What information is collected for Motor Vehicle Theft cases?",
    "What fields are required when reporting an Arson incident?", 
    "Show me the available options for Cyber Crime incidents"
]

print("Testing Field Schema Understanding:")
print("=" * 50)

for question in schema_questions:
    print(f"\nQ: {question}")
    print("-" * 30)
    answer = query_occurrences(question)
    print(f"A: {answer[:250]}{'...' if len(answer) > 250 else ''}")

# Example usage
print("\n\nExample Queries:")
print("=" * 30)

example_questions = [
    "What vehicle thefts happened recently?",
    "Show me death cases from accidents"
]

for q in example_questions:
    print(f"\nQ: {q}")
    print(f"A: {query_occurrences(q)[:200]}...")

# Direct schema exploration
print("\n\nDirect Schema Exploration:")
print("=" * 40)

# Show detailed schema for Motor Vehicle Theft (ID 8)
motor_vehicle_schema = get_field_info("Motor Vehicle Theft")
print("Motor Vehicle Theft Fields:")
print(motor_vehicle_schema[:500] + "..." if len(motor_vehicle_schema) > 500 else motor_vehicle_schema)

print("\n" + "="*80)
print("🎉 ENHANCED RAG SYSTEM FOR JSONB OCCURRENCE DATA IS READY!")
print("="*80)
print("""
✅ What We've Built:

1. **Field Schema Manager** - Automatically extracts and understands your dynamic field schemas
2. **Smart JSONB Query Builder** - Creates intelligent SQL queries for JSONB data
3. **Data Processor** - Formats occurrence data for LLM consumption
4. **Vector Store** - Enables semantic search on occurrence content
5. **Enhanced RAG System** - Provides intelligent, schema-aware responses

🚀 Usage Examples:

# Query for specific incidents
query_occurrences("What vehicle thefts happened at Sarit Center?")

# Ask about field schemas  
query_occurrences("What information is required for reporting arson?")

# Search for patterns
query_occurrences("Show me all death cases caused by accidents")

# Get field information directly
get_field_info("Missing Person")

📈 Performance Optimizations:

For production use, consider:
- Creating GIN indexes on JSONB columns: CREATE INDEX idx_formdata_gin ON sub_module_data USING GIN ("formData");
- Implementing caching for frequent queries
- Using connection pooling for database connections
- Batch processing for large vector store updates

Your JSONB occurrence data is now intelligently available to your LLM! 🎉
""")

print("\nFunctions ready for use:")
print("- query_occurrences(question)")
print("- get_field_info(module_name)")
print("- enhanced_rag.answer_question(question)")
print("- vector_store.search_similar_occurrences(query)")