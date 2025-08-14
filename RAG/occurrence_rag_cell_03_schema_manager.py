# Cell 3: Field Schema Manager
"""
This class extracts and manages the field schemas from your sub_module table.
It understands what fields are available for each occurrence type (Arson, Theft, Death, etc.).
"""

class FieldSchemaManager:
    """Manages field schemas from sub_module table"""
    
    def __init__(self, db: SQLDatabase):
        self.db = db
        self.schemas = {}
        self.load_schemas()
    
    def load_schemas(self):
        """Load all field schemas from sub_module table"""
        query = "SELECT id, name, description, fields FROM sub_module"
        result = self.db.run(query)
        
        # Parse the result
        import ast
        rows = ast.literal_eval(result)
        
        for row in rows:
            module_id, name, description, fields_json = row
            if fields_json:
                self.schemas[module_id] = {
                    'name': name,
                    'description': description,
                    'fields': fields_json
                }
        
        print(f"Loaded schemas for {len(self.schemas)} modules")
    
    def get_field_info(self, module_id: int) -> Dict:
        """Get field information for a specific module"""
        return self.schemas.get(module_id, {})
    
    def get_all_field_names(self) -> List[str]:
        """Get all unique field names across all modules"""
        all_fields = set()
        for schema in self.schemas.values():
            for field in schema.get('fields', []):
                all_fields.add(field.get('name', ''))
        return list(all_fields)
    
    def create_field_description(self, module_id: int) -> str:
        """Create human-readable field descriptions for LLM"""
        schema = self.get_field_info(module_id)
        if not schema:
            return "No schema information available"
        
        description = f"Module: {schema['name']} - {schema['description']}\n\nFields:\n"
        
        for field in schema.get('fields', []):
            field_name = field.get('name', 'Unknown')
            field_type = field.get('type', 'text')
            required = field.get('required', False)
            options = field.get('options', [])
            
            description += f"- {field_name} ({field_type})"
            if required:
                description += " [REQUIRED]"
            if options:
                description += f" Options: {', '.join(options[:5])}{'...' if len(options) > 5 else ''}"
            description += "\n"
        
        return description

# Initialize the schema manager
schema_manager = FieldSchemaManager(db)
print("✅ Field Schema Manager initialized!")

# Display available modules and their schemas
print("\nAvailable Occurrence Types and Sample Fields:")
print("=" * 60)

for module_id, schema in schema_manager.schemas.items():
    print(f"\n{module_id}. {schema['name']}")
    print(f"   Description: {schema['description']}")
    print(f"   Total fields: {len(schema['fields'])}")
    
    # Show first few fields as example
    print("   Sample fields:")
    for field in schema['fields'][:3]:
        field_name = field.get('name', 'Unknown')
        field_type = field.get('type', 'text')
        print(f"     - {field_name} ({field_type})")
    
    if len(schema['fields']) > 3:
        print(f"     ... and {len(schema['fields']) - 3} more fields")