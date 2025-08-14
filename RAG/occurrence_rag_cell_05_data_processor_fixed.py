# Cell 5: Data Processor and Vector Store (FIXED)
"""
Process occurrence data for LLM consumption and create vector store for semantic search
FIXED: Updated to use correct column name "iprsID"
"""

class OccurrenceDataProcessor:
    """Process occurrence data for LLM consumption"""
    
    def __init__(self, schema_manager: FieldSchemaManager):
        self.schema_manager = schema_manager
    
    def format_occurrence_for_llm(self, occurrence_data: Dict) -> str:
        """Format occurrence data into human-readable text for LLM"""
        formatted = []
        
        # Basic occurrence info
        formatted.append(f"OB Number: {occurrence_data.get('ob_number', 'N/A')}")
        formatted.append(f"Date: {occurrence_data.get('submissionDate', 'N/A')}")
        formatted.append(f"Type: {occurrence_data.get('module_name', 'N/A')}")
        formatted.append(f"Description: {occurrence_data.get('module_description', 'N/A')}")
        
        if occurrence_data.get('location'):
            formatted.append(f"Location: {occurrence_data['location']}")
        
        if occurrence_data.get('urgency'):
            formatted.append(f"Urgency: {occurrence_data['urgency']}")
        
        # Person information
        if occurrence_data.get('first_name'):
            name = f"{occurrence_data.get('first_name', '')} {occurrence_data.get('last_name', '')}".strip()
            formatted.append(f"Reporter: {name}")
        
        if occurrence_data.get('id_no'):
            formatted.append(f"ID Number: {occurrence_data['id_no']}")
        
        # Process JSONB form data
        form_data = occurrence_data.get('formData', {})
        if isinstance(form_data, str):
            try:
                form_data = json.loads(form_data)
            except:
                form_data = {}
        
        if form_data:
            formatted.append("\nOccurrence Details:")
            
            for key, value in form_data.items():
                if value and str(value).strip() and str(value) != 'null':
                    # Clean up the key name
                    clean_key = key.replace('_', ' ').title()
                    formatted.append(f"- {clean_key}: {value}")
        
        if occurrence_data.get('narrative'):
            formatted.append(f"\nNarrative: {occurrence_data['narrative']}")
        
        return "\n".join(formatted)
    
    def create_occurrence_documents(self, occurrences: List[Dict]) -> List[Document]:
        """Create LangChain documents from occurrence data"""
        documents = []
        
        for occurrence in occurrences:
            content = self.format_occurrence_for_llm(occurrence)
            
            metadata = {
                'ob_number': occurrence.get('ob_number', ''),
                'module_name': occurrence.get('module_name', ''),
                'submission_date': str(occurrence.get('submissionDate', '')),
                'urgency': occurrence.get('urgency', ''),
                'location': occurrence.get('location', '')
            }
            
            documents.append(Document(
                page_content=content,
                metadata=metadata
            ))
        
        return documents

def parse_db_result_to_dict(db_result_string: str) -> List[Dict]:
    """Parse database result string into list of dictionaries"""
    import ast
    try:
        # Parse the string representation of tuples
        rows = ast.literal_eval(db_result_string)
        
        # Define column names based on our query
        columns = ['id', 'ob_number', 'submissionDate', 'sub_moduleId', 'module_name', 
                  'module_description', 'formData', 'location', 'urgency', 'narrative',
                  'first_name', 'last_name', 'id_no']
        
        result = []
        for row in rows:
            occurrence_dict = dict(zip(columns, row))
            result.append(occurrence_dict)
        
        return result
    except Exception as e:
        print(f"Error parsing result: {e}")
        return []

class OccurrenceVectorStore:
    """Manage vector store for occurrence data"""
    
    def __init__(self, embeddings, data_processor: OccurrenceDataProcessor, query_builder: JSONBQueryBuilder):
        self.embeddings = embeddings
        self.data_processor = data_processor
        self.query_builder = query_builder
        self.vectorstore = None
        self.retriever = None
    
    def load_occurrences_to_vectorstore(self, limit: int = 50):
        """Load occurrences into vector store"""
        print(f"Loading {limit} recent occurrences into vector store...")
        
        # Get occurrence data
        query = self.query_builder.build_occurrence_query(limit=limit)
        results = self.query_builder.execute_query(query)
        
        if not results:
            print("No occurrence data found")
            return
        
        # Parse results
        occurrences = parse_db_result_to_dict(results)
        print(f"Parsed {len(occurrences)} occurrences")
        
        # Create documents
        documents = self.data_processor.create_occurrence_documents(occurrences)
        print(f"Created {len(documents)} documents")
        
        # Split documents if they're too long
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        split_docs = text_splitter.split_documents(documents)
        print(f"Split into {len(split_docs)} chunks")
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory="./occurrence_vectorstore"
        )
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        print("✅ Vector store created successfully!")
    
    def search_similar_occurrences(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar occurrences"""
        if not self.retriever:
            print("Vector store not initialized. Call load_occurrences_to_vectorstore first.")
            return []
        
        return self.retriever.invoke(query)

# Re-initialize data processor and vector store with fixed query builder
data_processor = OccurrenceDataProcessor(schema_manager)
vector_store = OccurrenceVectorStore(embeddings, data_processor, query_builder)

print("✅ Data Processor and Vector Store (FIXED) initialized!")

# Test data processing with sample occurrences
sample_query = query_builder.build_occurrence_query(limit=2)
sample_results = query_builder.execute_query(sample_query)

if sample_results:
    sample_occurrences = parse_db_result_to_dict(sample_results)
    
    if sample_occurrences:
        print("\nSample processed occurrence:")
        print("=" * 50)
        formatted_sample = data_processor.format_occurrence_for_llm(sample_occurrences[0])
        print(formatted_sample)
    else:
        print("❌ No sample data to process")
else:
    print("❌ No sample data available")