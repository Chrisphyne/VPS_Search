import os
from dotenv import load_dotenv
import meilisearch
import requests
import psycopg2
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check environment variables
required_env_vars = ["MEILI_HTTP_ADDR", "MEILI_API_KEY", "PG_DB", "PG_USER", "PG_PASSWORD", "PG_HOST", "PG_PORT", "OLLAMA_HOST"]
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

# Meilisearch client
client = meilisearch.Client(
    url=os.environ.get("MEILI_HTTP_ADDR", "http://localhost:7700"),
    api_key=os.environ.get("MEILI_API_KEY", "bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=")
)

# PostgreSQL connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.environ["PG_DB"],
            user=os.environ["PG_USER"],
            password=os.environ["PG_PASSWORD"],
            host=os.environ["PG_HOST"],
            port=os.environ["PG_PORT"]
        )
        return conn
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {str(e)}")
        raise

# Configure Ollama embedder
def configure_ollama_embedder(index_name="incidents"):
    try:
        embedder_config = {
            "suspect-ollama": {
                "source": "rest",
                "url": f"{os.environ.get('OLLAMA_HOST', 'http://localhost:11434')}/api/embeddings",
                "request": {
                    "model": "mxbai-embed-large",
                    "prompt": "{{text}}"
                },
                "response": {
                    "embedding": "{{embedding}}"
                },
                "documentTemplate": "Suspect named {{doc.suspect_name}} described as {{doc.suspect_description}}"
            }
        }
        task = client.index(index_name).update_settings({"embedders": embedder_config})
        client.wait_for_task(task.task_uid, timeout_in_ms=60000)
        logger.info("Ollama embedder configured.")
    except Exception as e:
        logger.error(f"Error configuring Ollama embedder: {str(e)}")
        raise

# Fetch suspect data
def fetch_suspect_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT smd."id", smd."formData"->>'Name of the suspect' AS suspect_name,
                   smd."formData"->>'Description of the suspect' AS suspect_description,
                   smd."formData"->>'Do you have a suspect' AS has_suspect,
                   sm.name AS sub_module_name
            FROM sub_module_data smd
            JOIN sub_module sm ON smd."sub_moduleId" = sm.id
            WHERE sm.name IN ('GBV', 'Robbery', 'Rape', 'Cyber Crime', 'Assault')
              AND smd."formData"->>'Do you have a suspect' = 'Yes'
              AND smd."formData"->>'Name of the suspect' IS NOT NULL
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        documents = [
            {
                "id": row[0],
                "suspect_name": row[1],
                "suspect_description": row[2] or "",
                "sub_module_name": row[4],
                "suspect_presence": row[3],
                "searchable_text": f"{row[1]} {row[2] or ''}".strip()
            }
            for row in rows
        ]
        return documents
    except Exception as e:
        logger.error(f"Error fetching suspect data: {str(e)}")
        raise

# Index data to Meilisearch
def index_data(index_name="incidents"):
    try:
        # Create index if not exists
        try:
            client.create_index(index_name, primary_key="id")
        except:
            pass
        # Set searchable and filterable attributes
        index = client.index(index_name)
        task = index.update_settings({
            "searchableAttributes": ["suspect_name", "suspect_description", "searchable_text", "sub_module_name"],
            "filterableAttributes": ["sub_module_name", "suspect_presence"]
        })
        client.wait_for_task(task.task_uid, timeout_in_ms=60000)
        # Configure Ollama embedder
        configure_ollama_embedder(index_name)
        # Index documents
        documents = fetch_suspect_data()
        task = index.add_documents(documents)
        client.wait_for_task(task.task_uid, timeout_in_ms=300000)
        logger.info(f"Indexed {len(documents)} documents.")
    except Exception as e:
        logger.error(f"Indexing error: {str(e)}")
        raise

# Perform hybrid search
def hybrid_search(query, index_name="incidents", k=3, semantic_ratio=0.5):
    try:
        index = client.index(index_name)
        results = index.search(query, {
            "limit": k,
            "hybrid": {
                "embedder": "suspect-ollama",
                "semanticRatio": semantic_ratio
            },
            "filter": "suspect_presence = 'Yes'",
            "attributesToRetrieve": ["id", "suspect_name", "suspect_description", "sub_module_name"]
        })
        return [
            {
                "id": hit["id"],
                "content": f"{hit['suspect_name']} {hit.get('suspect_description', '')}".strip(),
                "metadata": {
                    "suspect_name": hit["suspect_name"],
                    "suspect_description": hit.get("suspect_description", ""),
                    "sub_module_name": hit["sub_module_name"]
                },
                "score": hit.get("_rankingScore", 1.0)
            }
            for hit in results["hits"]
        ]
    except Exception as e:
        logger.error(f"Hybrid search failed: {str(e)}")
        raise

# Main execution
if __name__ == "__main__":
    index_data()
    query = "John Doe"
    results = hybrid_search(query=query, k=3)
    for result in results:
        print(f"Content: {result['content']}")
        print(f"Metadata: {result['metadata']}")
        print(f"Score: {result['score']}")
        print("-" * 50)
