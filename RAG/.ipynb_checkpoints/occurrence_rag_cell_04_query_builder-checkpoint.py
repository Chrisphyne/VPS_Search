# Cell 4: Smart JSONB Query Builder
"""
This class builds intelligent SQL queries that can extract and interpret 
data from your JSONB formData columns.
"""

class JSONBQueryBuilder:
    """Build intelligent SQL queries for JSONB data"""
    
    def __init__(self, db: SQLDatabase, schema_manager: FieldSchemaManager):
        self.db = db
        self.schema_manager = schema_manager
    
    def build_occurrence_query(self, limit: int = 10, module_id: Optional[int] = None) -> str:
        """Build query to get occurrence data with schema information"""
        base_query = """
        SELECT 
            smd.id,
            smd.ob_number,
            smd."submissionDate",
            smd."sub_moduleId",
            sm.name as module_name,
            sm.description as module_description,
            smd."formData",
            smd.location,
            smd.urgency,
            smd.narrative,
            ip.first_name,
            ip.last_name,
            ip.id_no
        FROM sub_module_data smd
        LEFT JOIN sub_module sm ON smd."sub_moduleId" = sm.id
        LEFT JOIN "IPRS_Person" ip ON smd."iprsId" = ip.id
        """
        
        if module_id:
            base_query += f" WHERE smd.\"sub_moduleId\" = {module_id}"
        
        base_query += f" ORDER BY smd.\"submissionDate\" DESC LIMIT {limit}"
        
        return base_query
    
    def search_in_jsonb(self, search_term: str, limit: int = 10) -> str:
        """Build query to search within JSONB formData"""
        return f"""
        SELECT 
            smd.id,
            smd.ob_number,
            smd."submissionDate",
            sm.name as module_name,
            smd."formData",
            smd.location,
            smd.urgency
        FROM sub_module_data smd
        LEFT JOIN sub_module sm ON smd."sub_moduleId" = sm.id
        WHERE smd."formData"::text ILIKE '%{search_term}%'
        OR smd.narrative ILIKE '%{search_term}%'
        ORDER BY smd."submissionDate" DESC
        LIMIT {limit}
        """
    
    def get_statistics_by_module(self) -> str:
        """Get occurrence statistics by module type"""
        return """
        SELECT 
            sm.name as module_name,
            COUNT(*) as total_occurrences,
            COUNT(CASE WHEN smd."submissionDate" >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as last_30_days,
            COUNT(CASE WHEN smd.urgency = 'High' THEN 1 END) as high_urgency
        FROM sub_module_data smd
        LEFT JOIN sub_module sm ON smd."sub_moduleId" = sm.id
        GROUP BY sm.id, sm.name
        ORDER BY total_occurrences DESC
        """
    
    def execute_query(self, query: str) -> Any:
        """Execute query and return results"""
        try:
            return self.db.run(query)
        except Exception as e:
            print(f"Query execution error: {e}")
            return None

# Initialize query builder
query_builder = JSONBQueryBuilder(db, schema_manager)
print("✅ JSONB Query Builder initialized!")

# Test the query builder
print("\nTesting Query Builder:")
print("=" * 40)

# Get recent occurrences
recent_query = query_builder.build_occurrence_query(limit=3)
recent_results = query_builder.execute_query(recent_query)

if recent_results:
    print("✅ Successfully retrieved recent occurrences")
    print(f"Sample result (truncated): {str(recent_results)[:200]}...")
else:
    print("❌ No results returned")

# Search for specific terms
print("\nSearching for 'stolen' in occurrences:")
search_query = query_builder.search_in_jsonb("stolen", limit=2)
search_results = query_builder.execute_query(search_query)

if search_results:
    print("✅ Found occurrences containing 'stolen'")
    print(f"Sample result: {str(search_results)[:200]}...")
else:
    print("❌ No 'stolen' occurrences found")

# Get statistics
print("\nOccurrence Statistics by Module:")
stats_query = query_builder.get_statistics_by_module()
stats_results = query_builder.execute_query(stats_query)
if stats_results:
    print(f"Statistics: {str(stats_results)[:300]}...")
else:
    print("❌ No statistics available")