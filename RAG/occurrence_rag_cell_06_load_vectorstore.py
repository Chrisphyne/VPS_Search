# Cell 6: Load Vector Store and Test Semantic Search
"""
Load occurrence data into vector store and test semantic search capabilities
"""

# Load occurrences into vector store (this may take a few moments)
print("Loading occurrences into vector store...")
vector_store.load_occurrences_to_vectorstore(limit=30)  # Start with 30 for testing

# Test semantic search capabilities
test_queries = [
    "vehicle theft at sarit center",
    "death due to accident", 
    "stolen laptop",
    "fire incidents",
    "missing person child"
]

print("\nTesting Semantic Search:")
print("=" * 50)

for query in test_queries:
    print(f"\nSearching for: '{query}'")
    print("-" * 30)
    
    results = vector_store.search_similar_occurrences(query, k=2)
    
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"OB Number: {doc.metadata.get('ob_number', 'N/A')}")
        print(f"Type: {doc.metadata.get('module_name', 'N/A')}")
        print(f"Content: {doc.page_content[:150]}...")
        print("-" * 25)

print("\n✅ Vector store loaded and semantic search tested!")