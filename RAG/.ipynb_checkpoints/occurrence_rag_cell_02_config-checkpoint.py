# Cell 2: Environment Configuration
"""
Configure environment variables and initialize database/AI connections
"""

# Set up environment variables
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDsJJu5oN0BQrEKvnotU6uYEl5Mxw9fiug'
os.environ['LANGSMITH_API_KEY'] = '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'
os.environ['LANGSMITH_TRACING'] = 'true'

# Database connection settings
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'obmain'
os.environ['DB_USER'] = 'myuser'
os.environ['DB_PASSWORD'] = 'Welcome123'

# Initialize database connection
db_uri = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

try:
    db = SQLDatabase.from_uri(db_uri)
    print("✅ Database connected successfully!")
    print(f"Available tables: {db.get_usable_table_names()}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

# Initialize LLM and embeddings
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

print("✅ LLM and embeddings initialized!")
print("✅ Environment setup complete!")