import streamlit as st
import meilisearch
import psycopg2
import os
import logging
import json
import requests
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import meilisearch.errors

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to update database selections
def update_database_selections(option):
    if st.session_state[f"cbx_{option}"]:
        if option == "ALL":
            for opt in database_options:
                st.session_state[f"cbx_{opt}"] = True
        else:
            st.session_state[f"cbx_ALL"] = False
    elif option != "ALL" and not any(st.session_state[f"cbx_{opt}"] for opt in database_options if opt != "ALL"):
        st.session_state[f"cbx_ALL"] = True
    for opt in database_options:
        st.session_state.database_selections[opt] = st.session_state[f"cbx_{option}"]

# Streamlit app configuration
st.set_page_config(page_title="Kenya Police Search System", layout="wide", page_icon="🔍")

# Apply custom theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    :root {
        --primary-color: #007BFF;
        --background-color: #F5F6F5; /* Light gray background for main content */
        --text-color: #333333;
        --button-color: #D3D3D3;
        --button-hover: #B0B0B0;
        --border-color: #CCCCCC;
        --shadow-color: rgba(0, 0, 0, 0.1);
        --light-blue: #E7F0FA;
    }

    .main {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        padding: 1rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: flex-start !important;
    }

    .main-content {
        width: 90% !important; /* Responsive width */
        max-width: 800px !important;
        padding: 1rem !important;
        text-align: center !important;
        background-color: var(--background-color) !important;
        margin: 0 auto !important; /* Center the content */
    }

    .stSidebar {
        background-color: var(--background-color) !important;
        padding: 1rem !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: 0 2px 10px var(--shadow-color) !important;
        height: 100vh !important;
        overflow-y: auto !important;
    }

    .stButton > button {
        background-color: var(--button-color) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 400 !important;
        transition: all 0.3s ease !important;
        font-family: 'Roboto', sans-serif !important;
        margin: 0 0.5rem !important;
    }
    .stButton > button:hover {
        background-color: var(--button-hover) !important;
        border-color: var(--button-hover) !important;
        color: var(--text-color) !important;
    }
    .stButton:nth-child(3) > button {
        background-color: var(--primary-color) !important;
        color: #fff !important;
        border: 1px solid var(--primary-color) !important;
    }
    .stButton:nth-child(3) > button:hover {
        background-color: #0056b3 !important;
        border-color: #0056b3 !important;
    }

    .stTextInput > div > div > input, .stDateInput > div > div > input {
        background-color: var(--background-color) !important; /* Uniform background */
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        color: var(--text-color) !important;
        font-family: 'Roboto', sans-serif !important;
        padding: 0.5rem !important;
        text-align: left !important;
        width: 100% !important;
        max-width: 100% !important; /* Full width for inputs */
        box-sizing: border-box !important;
    }
    .stTextInput > div > div > input:focus, .stDateInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.2) !important;
    }

    .databases-container {
        background-color: var(--light-blue) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin-bottom: 1.5rem !important;
        border: none !important;
        outline: none !important;
    }
    .checkbox-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.5rem !important;
    }
    .stCheckbox > label {
        background-color: var(--light-blue) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Roboto', sans-serif !important;
        font-size: 14px !important;
        cursor: pointer !important;
    }
    .stCheckbox > label:hover {
        background-color: rgba(0, 119, 255, 0.2) !important;
    }
    .stCheckbox [type="checkbox"]:checked + span {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
        color: #fff !important;
    }
    .title-container {
        text-align: center !important;
        width: 100% !important;
        margin-bottom: 1.5rem !important;
        padding-top: 0 !important;
    }
    .title-container h1 {
        font-size: 1.75rem !important;
        font-weight: 500 !important;
        color: var(--text-color) !important;
        margin: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
    }
    .title-container h1::before {
        content: "🔍 "; /* Magnifying glass icon */
        margin-right: 0.5rem !important;
    }
    .results-container {
        border: 2px dashed var(--border-color) !important;
        padding: 1rem !important;
        border-radius: 4px !important;
        margin-top: 1rem !important;
        text-align: center !important;
        color: #666 !important;
        width: 100% !important;
        max-width: 600px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        background-color: var(--background-color) !important;
    }
    .stMarkdown h3 {
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    .error-container {
        background-color: #ffebee !important;
        border: 2px solid #ef9a9a !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin-top: 1rem !important;
        color: #c62828 !important;
    }

    /* Add "Filters" text to the blue section */
    .databases-container::before {
        content: "Filters";
        display: block;
        font-size: 1.25rem;
        font-weight: 500;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Meilisearch client
try:
    MEILISEARCH_HOST = os.getenv("MEILISEARCH_HOST", "http://localhost:7700")
    response = requests.get(f"{MEILISEARCH_HOST}/health", timeout=5)
    if response.status_code != 200:
        raise Exception("Meilisearch is not available")
    meili_client = meilisearch.Client(
        url=MEILISEARCH_HOST,
        api_key=os.getenv("MEILISEARCH_API_KEY", "bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=")
    )
    version = meili_client.get_version()
    logger.info(f"Meilisearch server version: {version['pkgVersion']}")
except Exception as e:
    st.error(f"Meilisearch connection failed: {str(e)}")
    logger.error(f"Meilisearch connection failed: {str(e)}")
    st.stop()

# PostgreSQL connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DB", "your_db"),
            user=os.getenv("PG_USER", "your_user"),
            password=os.getenv("PG_PASSWORD", "your_password"),
            host=os.getenv("PG_HOST", "localhost"),
            port=os.getenv("PG_PORT", "5432")
        )
        return conn
    except Exception as e:
        st.error(f"PostgreSQL connection failed: {str(e)}")
        logger.error(f"PostgreSQL connection failed: {str(e)}")
        raise

# Fetch sub-module names
@st.cache_data
def get_sub_module_names():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sub_module ORDER BY name")
        sub_modules = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return sub_modules
    except Exception as e:
        st.error(f"Error fetching sub-modules: {str(e)}")
        logger.error(f"Error fetching sub-modules: {str(e)}")
        return [
            "GBV", "Stolen Lost Item", "Robbery", "Rape", "Motor Vehicle Theft", "Missing Person",
            "Homicide", "Death", "Cyber Crime", "Burglary", "Assault", "Arson"
        ]

# Index-related functions
def index_exists(index_name="incidents"):
    try:
        meili_client.index(index_name).get_stats()
        return True
    except meilisearch.errors.MeilisearchApiError as e:
        if e.code == "index_not_found":
            return False
        raise

def create_meilisearch_index(index_name="incidents"):
    try:
        response = requests.post(
            f"{MEILISEARCH_HOST}/indexes",
            headers={"Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY')}", "Content-Type": "application/json"},
            json={"uid": index_name, "primaryKey": "id"}
        )
        if response.status_code not in [200, 201, 202]:
            raise Exception(f"Failed to create index: {response.text}")
        task = meili_client.get_task(response.json().get("taskUid", response.json().get("uid")))
        task_id = getattr(task, "task_uid", getattr(task, "uid", None))
        if not task_id:
            raise Exception("Task ID not found in response")
        meili_client.wait_for_task(task_id, timeout_in_ms=180000)
        logger.info("Meilisearch index created.")
        return True
    except Exception as e:
        st.error(f"Error creating index: {str(e)}")
        logger.error(f"Error creating index: {str(e)}")
        raise

def set_index_settings(index_name="incidents"):
    try:
        index = meili_client.index(index_name)
        task = index.update_settings({
            "searchableAttributes": ["*"],
            "filterableAttributes": [
                "sub_module_name", "stolen_items", "electronic_type", "document_type",
                "vehicle_registration", "victim_name", "gbv_type", "cause_of_death",
                "mental_condition", "suspect_presence", "submissionDate", "suspect_name",
                "suspect_description"
            ],
            "typoTolerance": {"enabled": True, "minWordSizeForTypos": {"oneTypo": 2, "twoTypos": 4}},
            "rankingRules": ["words", "typo", "proximity", "attribute", "sort", "exactness"]
        })
        task_id = getattr(task, "task_uid", getattr(task, "uid", None))
        if not task_id:
            raise Exception("Task ID not found for index settings")
        meili_client.wait_for_task(task_id, timeout_in_ms=180000)
        logger.info("Index settings updated.")
        return True
    except Exception as e:
        st.error(f"Error setting index settings: {str(e)}")
        logger.error(f"Error setting index settings: {str(e)}")
        raise

def index_meilisearch_data():
    try:
        index_name = "incidents"
        try:
            response = requests.delete(f"{MEILISEARCH_HOST}/indexes/{index_name}", headers={"Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY')}"})
            if response.status_code in [200, 202, 204]:
                task = meili_client.get_task(response.json().get("taskUid", response.json().get("uid")))
                task_id = getattr(task, "task_uid", getattr(task, "uid", None))
                if task_id:
                    meili_client.wait_for_task(task_id, timeout_in_ms=180000)
                logger.info("Existing index deleted.")
        except Exception as e:
            logger.warning(f"Index deletion skipped (may not exist): {str(e)}")

        create_meilisearch_index(index_name)
        set_index_settings(index_name)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT smd."id", smd."sub_moduleId", smd."submissionDate", smd."formData", smd."location", smd."narrative",
                   sm.name as sub_module_name
            FROM sub_module_data smd
            JOIN sub_module sm ON smd."sub_moduleId" = sm.id
            WHERE sm.name IN ('GBV', 'Stolen Lost Item', 'Robbery', 'Rape', 'Motor Vehicle Theft', 'Missing Person',
                             'Homicide', 'Death', 'Cyber Crime', 'Burglary', 'Assault', 'Arson')
        """)
        chunk_size = 1000
        documents = []
        total_records = 0
        progress_bar = st.progress(0)
        status_text = st.empty()

        cur_count = conn.cursor()
        cur_count.execute("""
            SELECT COUNT(*)
            FROM sub_module_data smd
            JOIN sub_module sm ON smd."sub_moduleId" = sm.id
            WHERE sm.name IN ('GBV', 'Stolen Lost Item', 'Robbery', 'Rape', 'Motor Vehicle Theft', 'Missing Person',
                             'Homicide', 'Death', 'Cyber Crime', 'Burglary', 'Assault', 'Arson')
        """)
        total_expected = cur_count.fetchone()[0]
        cur_count.close()

        while True:
            rows = cur.fetchmany(chunk_size)
            if not rows:
                break
            for row in rows:
                form_data = row[3] or {}
                searchable_values = []
                for key, value in form_data.items():
                    if isinstance(value, str):
                        searchable_values.append(value)
                    elif value is not None:
                        searchable_values.append(str(value))
                searchable_values.extend(filter(None, [row[4] or '', row[5] or '', row[6] or '']))
                searchable_text = " ".join(searchable_values)
                submission_date = row[2].isoformat() if row[2] and isinstance(row[2], datetime) else None
                doc = {
                    "id": row[0], "sub_moduleId": row[1], "sub_module_name": row[6],
                    "submissionDate": submission_date, "location": row[4] or form_data.get("location"),
                    "narrative": row[5], "description": form_data.get("Give a brief narrative of what happened") or
                    form_data.get("A brief narrative of what happened") or form_data.get("A brief description of the person") or "N/A",
                    "type_of_property": form_data.get("Type of property") or form_data.get("select type of property broken into"),
                    "victim_name": form_data.get("Name of the casualty") or form_data.get("Name of the victim") or
                    form_data.get("Name of the deceased") or form_data.get("Name"),
                    "vehicle_make": form_data.get("Make"), "vehicle_model": form_data.get("Model"),
                    "vehicle_registration": form_data.get("Registration number"),
                    "stolen_items": form_data.get("What category of items were stolen"),
                    "electronic_type": form_data.get("type of electronic"),
                    "document_type": form_data.get("type of Documents"),
                    "gbv_type": form_data.get("Type of GBV"), "cause_of_death": form_data.get("Cause of death"),
                    "mental_condition": form_data.get("Mental Condition"),
                    "suspect_presence": form_data.get("Do you have a suspect"),
                    "suspect_name": form_data.get("Name of the suspect"),
                    "suspect_description": form_data.get("Description of the suspect") or form_data.get("Give details about the suspect"),
                    "cyber_incident": form_data.get("Select Incident"),
                    "platform_digital_violence": form_data.get("Platform In Digital or Online Violence"),
                    "searchable_text": searchable_text, "formData": form_data
                }
                for key, value in form_data.items():
                    doc[key] = value
                documents.append(doc)
            total_records += len(rows)
            progress = min(total_records / total_expected if total_expected > 0 else 1.0, 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Indexed {total_records} of approximately {total_expected} records...")
        cur.close()
        conn.close()
        if documents:
            index = meili_client.index(index_name)
            task = index.add_documents(documents)
            task_id = getattr(task, "task_uid", getattr(task, "uid", None))
            if not task_id:
                raise Exception("Task ID not found for document indexing")
            meili_client.wait_for_task(task_id, timeout_in_ms=300000)
            progress_bar.progress(1.0)
            status_text.text(f"Indexed {total_records} documents in Meilisearch.")
            st.success(f"Indexed {total_records} documents in Meilisearch.")
        else:
            progress_bar.progress(1.0)
            status_text.text("No documents retrieved from database.")
            st.warning("No documents retrieved from database.")
        return True
    except Exception as e:
        progress_bar.progress(1.0)
        status_text.text(f"Indexing failed: {str(e)}")
        st.error(f"Meilisearch indexing error: {str(e)}")
        logger.error(f"Meilisearch indexing error: {str(e)}")
        return False

def debug_suspect_names(index_name="incidents"):
    try:
        index = meili_client.index(index_name)
        results = index.search("", {
            "filter": "suspect_presence = 'Yes' AND (suspect_name IS NOT NULL OR suspect_description IS NOT NULL)",
            "limit": 10,
            "attributesToRetrieve": ["suspect_name", "suspect_description", "sub_module_name", "id"]
        })
        if results["hits"]:
            st.write("Sample suspect names and descriptions in Meilisearch:")
            for hit in results["hits"]:
                st.write(f"- ID: {hit['id']}, Sub-module: {hit['sub_module_name']}, Suspect: {hit.get('suspect_name', 'N/A')}, Description: {hit.get('suspect_description', 'N/A')}")
        else:
            st.warning("No documents found with suspect names or descriptions in Meilisearch.")
        logger.debug(f"Debug suspect names: {json.dumps(results, indent=2)}")
    except Exception as e:
        st.error(f"Error debugging suspect names: {str(e)}")
        logger.error(f"Error debugging suspect names: {str(e)}")

def debug_indexed_documents(index_name="incidents"):
    try:
        index = meili_client.index(index_name)
        results = index.search("", {"limit": 10, "attributesToRetrieve": ["*"]})
        if results["hits"]:
            st.write("Sample documents in Meilisearch index:")
            for hit in results["hits"]:
                st.write(f"- ID: {hit['id']}, Sub-module: {hit.get('sub_module_name', 'N/A')}")
                st.write(f"  Location: {hit.get('location', 'N/A')}")
                st.write(f"  Submission Date: {hit.get('submissionDate', 'N/A')}")
                st.write(f"  Description: {hit.get('description', 'N/A')}")
                st.write(f"  Suspect Name: {hit.get('suspect_name', 'N/A')}")
                st.write(f"  Suspect Description: {hit.get('suspect_description', 'N/A')}")
                st.write(f"  Searchable Text: {hit.get('searchable_text', 'N/A')[:100]}...")
                st.write(f"  Form Data: {json.dumps(hit.get('formData', {}), indent=2)[:200]}...")
        else:
            st.warning("No documents found in Meilisearch index.")
        logger.debug(f"Debug indexed documents: {json.dumps(results, indent=2)}")
    except Exception as e:
        st.error(f"Error debugging indexed documents: {str(e)}")
        logger.error(f"Error debugging indexed documents: {str(e)}")

# Automatic index creation on startup
if not index_exists("incidents"):
    st.info("Incidents index not found. Creating and indexing data...")
    try:
        index_meilisearch_data()
    except Exception as e:
        st.error(f"Failed to create and index data: {str(e)}")
        logger.error(f"Failed to create and index data: {str(e)}")
        st.stop()

# Main UI
st.markdown('<div class="title-container"><h1> SEARCH </h1></div>', unsafe_allow_html=True)

# Sidebar for Search Filters
with st.sidebar:
    st.markdown('<div class="databases-container">', unsafe_allow_html=True)
    st.markdown("### Databases")
    database_options = [
        "ALL", "WATCHLIST DB", "STOLEN/LOST ITEMS DB", "MISSING PERSONS DB",
        "EVIDENCE DB", "STOLEN VEHICLES DB", "PRISONER PROPERTY DB"
    ]
    if 'database_selections' not in st.session_state:
        st.session_state.database_selections = {option: False for option in database_options}

    st.markdown('<div class="checkbox-grid">', unsafe_allow_html=True)
    for option in database_options:
        st.session_state.database_selections[option] = st.checkbox(option, value=st.session_state.database_selections[option], key=f"cbx_{option}", on_change=update_database_selections, args=(option,))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("More Filters"):
        st.markdown("#### Report/OB")
        sub_module_filter = st.multiselect(
            "Select Sub-modules", get_sub_module_names(), key="sub_module_filter"
        )
        st.markdown("#### Settings")
        setting_action = st.selectbox(
            "Settings Action:",
            ["None", "Create Meilisearch Index", "Index Data", "Debug Suspect Names", "Debug Indexed Documents"],
            key="settings_select"
        )
        if setting_action != "None" and st.button("Execute", key="execute_button"):
            if setting_action == "Create Meilisearch Index":
                try:
                    create_meilisearch_index()
                    set_index_settings()
                    st.success("Meilisearch index created and configured.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            elif setting_action == "Index Data":
                index_meilisearch_data()
            elif setting_action == "Debug Suspect Names":
                debug_suspect_names()
            elif setting_action == "Debug Indexed Documents":
                debug_indexed_documents()

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)
selected_databases = [opt for opt in database_options if st.session_state.database_selections[opt]]

# Keyword Section
st.markdown("### Keywords")
st.text_input(
    "Enter keywords...",
    label_visibility="collapsed",
    key="query_input",
    placeholder="Enter keywords..."
)

# Date Range Section
st.markdown("### Date Range")
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Start Date", value=date(2025, 6, 9), key="start_date")  # Current date: 05:04 PM EAT, June 09, 2025
with col2:
    end_date = st.date_input("End Date", value=date(2025, 7, 9), key="end_date")

# Actions
col3, col4 = st.columns([1, 1])
with col3:
    if st.button("Search", key="main_search_button", help="Perform search with current filters"):
        if st.session_state.query_input:
            if not selected_databases:
                for option in database_options:
                    st.session_state.database_selections[option] = True
                selected_databases = database_options
                st.warning("No databases selected. Defaulting to ALL databases.")
            try:
                index = meili_client.index("incidents")
                filters = []
                if "ALL" not in selected_databases or len(selected_databases) < len(database_options):
                    for db_type in selected_databases:
                        if db_type == "WATCHLIST DB":
                            filters.append("victim_name IS NOT NULL")
                        elif db_type == "STOLEN/LOST ITEMS DB":
                            filters.append("stolen_items IS NOT NULL OR electronic_type IS NOT NULL OR document_type IS NOT NULL")
                        elif db_type == "MISSING PERSONS DB":
                            filters.append("sub_module_name = 'Missing Person'")
                        elif db_type == "EVIDENCE DB":
                            filters.append("narrative IS NOT NULL OR description IS NOT NULL")
                        elif db_type == "STOLEN VEHICLES DB":
                            filters.append("sub_module_name = 'Motor Vehicle Theft' OR vehicle_registration IS NOT NULL")
                        elif db_type == "PRISONER PROPERTY DB":
                            filters.append("stolen_items IS NOT NULL")
                if sub_module_filter:
                    sub_module_list = ', '.join(f'"{sm}"' for sm in sub_module_filter)
                    filters.append(f"sub_module_name IN [{sub_module_list}]")
                if start_date and end_date:
                    start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
                    end_ts = int(datetime.combine(end_date, datetime.max.time()).timestamp())
                    filters.append(f"submissionDate >= {start_ts} AND submissionDate <= {end_ts}")
                filter_str = " AND ".join(filters) if filters else None
                logger.debug(f"Search query: {st.session_state.query_input}")
                logger.debug(f"Search filters: {filter_str}")
                offset = (st.session_state.get('current_page', 1) - 1) * 10
                results = index.search(st.session_state.query_input, {"limit": 10, "offset": offset, "filter": filter_str, "attributesToRetrieve": ["*"]})["hits"]
                total_results = index.search(st.session_state.query_input, {"filter": filter_str, "attributesToRetrieve": ["*"]})["estimatedTotalHits"]
                st.session_state.total_pages = max(1, (total_results + 9) // 10)
                st.info("Search performed using full-text search across all fields.")
                st.write(f"Found {len(results)} results (Page {st.session_state.get('current_page', 1)} of {st.session_state.get('total_pages', 1)})")
                if not results:
                    st.warning("No results found with current query/filters. Trying search without filters...")
                    results = index.search(st.session_state.query_input, {"limit": 10, "offset": offset, "filter": None, "attributesToRetrieve": ["*"]})["hits"]
                    total_results = index.search(st.session_state.query_input, {"filter": None, "attributesToRetrieve": ["*"]})["estimatedTotalHits"]
                    st.session_state.total_pages = max(1, (total_results + 9) // 10)
                    st.write(f"Found {len(results)} results without filters (Page {st.session_state.get('current_page', 1)} of {st.session_state.get('total_pages', 1)})")
                    if not results:
                        st.warning("Still no results. Check 'Debug Indexed Documents' to verify index contents or try a different query.")
                st.session_state.results = results
                for hit in results:
                    with st.expander(f"{hit.get('sub_module_name', 'N/A')} - ID: {hit['id']}"):
                        st.markdown(f"**Location**: {hit.get('location', 'N/A')}")
                        st.markdown(f"**Submission Date**: {hit.get('submissionDate', 'N/A')}")
                        st.markdown(f"**Description**: {hit.get('description', 'N/A')}")
                        if hit.get('suspect_name'):
                            st.markdown(f"**Suspect Name**: {hit['suspect_name']}")
                        if hit.get('suspect_description'):
                            st.markdown(f"**Suspect Description**: {hit['suspect_description']}")
                        st.markdown("**Form Data**:")
                        for key, value in hit.get('formData', {}).items():
                            st.markdown(f"- **{key}**: {value}")
                        st.markdown(f"**Score**: {hit.get('_rankingScore', 1.0):.2f}")
            except TypeError as te:
                st.markdown('<div class="error-container">', unsafe_allow_html=True)
                st.error(f"An error occurred: {str(te)}. Please ensure all inputs are valid.")
                st.markdown('</div>', unsafe_allow_html=True)
                logger.error(f"TypeError during search: {str(te)}")
            except Exception as e:
                st.markdown('<div class="error-container">', unsafe_allow_html=True)
                st.error(f"Search error: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
                logger.error(f"Search error: {str(e)}")
        else:
            st.warning("Please enter a search query.")
with col4:
    if st.button("Reset", key="reset_button"):
        st.session_state.clear()
        st.rerun()

# Results area
st.markdown('<div class="results-container">', unsafe_allow_html=True)
if 'results' not in st.session_state or not st.session_state.get('results'):
    # st.write("No results to display. Perform a search using the filters.")
    st.write(" ")
else:
    for hit in st.session_state.results:
        with st.expander(f"{hit.get('sub_module_name', 'N/A')} - ID: {hit['id']}"):
            st.markdown(f"**Location**: {hit.get('location', 'N/A')}")
            st.markdown(f"**Submission Date**: {hit.get('submissionDate', 'N/A')}")
            st.markdown(f"**Description**: {hit.get('description', 'N/A')}")
            if hit.get('suspect_name'):
                st.markdown(f"**Suspect Name**: {hit['suspect_name']}")
            if hit.get('suspect_description'):
                st.markdown(f"**Suspect Description**: {hit['suspect_description']}")
            st.markdown("**Form Data**:")
            for key, value in hit.get('formData', {}).items():
                st.markdown(f"- **{key}**: {value}")
            st.markdown(f"**Score**: {hit.get('_rankingScore', 1.0):.2f}")
st.markdown('</div>', unsafe_allow_html=True)

# Pagination
def update_page(direction):
    if direction == "previous" and st.session_state.current_page > 1:
        st.session_state.current_page -= 1
    elif direction == "next" and st.session_state.current_page < st.session_state.total_pages:
        st.session_state.current_page += 1
    st.rerun()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'total_pages' not in st.session_state:
    st.session_state.total_pages = 1

col5, col6, col7 = st.columns([1, 1, 1])
with col5:
    st.button("Previous", key="prev_button", disabled=st.session_state.current_page == 1, on_click=lambda: update_page("previous"))
with col6:
    st.write(f"Page {st.session_state.current_page}")
with col7:
    st.button("Next", key="next_button", disabled=st.session_state.current_page >= st.session_state.total_pages, on_click=lambda: update_page("next"))

st.markdown('</div>', unsafe_allow_html=True)  # Close main-content div







# import streamlit as st
# import meilisearch
# import psycopg2
# import os
# import logging
# import json
# import requests
# from datetime import datetime, timedelta, date
# from dotenv import load_dotenv
# import meilisearch.errors

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Streamlit app configuration
# st.set_page_config(page_title="Incident Search DBs", layout="centered", page_icon="🔍")

# # Apply custom theme CSS with white background, deeper grey buttons, vibrant blue accents, and Roboto font
# # Colors align with config.toml: primaryColor=#007BFF, backgroundColor=#F5F6F5, secondaryBackgroundColor=#E7EDE9, textColor=#000000
# st.markdown("""
#     <style>

#     /* Import Roboto from Google Fonts */
#     @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

#     /* Root variables for theme consistency */
#     :root {
#         --primary-color: #007BFF;
#         --background-color: #F5F6F5;
#         --secondary-background: #E7EDE9;
#         --text-color: #000000;
#         --button-color: #4A4A4A;
#         --button-hover: #6B6B6B;
#         --border-color: #D3D3D3;
#         --shadow-color: rgba(0, 0, 0, 0.1);
#         --accent-color: #007BFF;
#         --checkbox-checked: #007BFF;
#         --slider-track: #E7EDE9;
#         --slider-thumb: #007BFF;
#         --light-blue: #E7F0FA; /* Light blue for unselected state */
#     }

#     /* Main container with increased width */
#     .main, .css-1v3fvcr {
#         background-color: var(--background-color);
#         color: var(--text-color);
#         padding: 2rem;
#         max-width: 1200px;
#         margin-left: auto;
#         margin-right: auto;
#     }

#     /* Primary buttons */
#     .stButton > button {
#         background-color: var(--button-color);
#         color: var(--text-color);
#         border: 2px solid var(--border-color);
#         border-radius: 8px;
#         padding: 0.5rem 1rem;
#         font-weight: 500;
#         transition: all 0.3s ease;
#         font-family: 'Roboto', sans-serif !important;
#     }
#     .stButton > button:hover {
#         background-color: var(--button-hover);
#         border-color: var(--button-hover);
#         color: var(--text-color);
#     }

#     /* Expander toggle */
#     .streamlit-expanderHeader {
#         background-color: var(--secondary-background) !important;
#         color: var(--text-color) !important;
#         border-radius: 8px;
#         padding: 0.5rem;
#         transition: all 0.3s ease;
#         font-family: 'Roboto', sans-serif !important;
#     }
#     .streamlit-expanderHeader:hover {
#         background-color: var(--border-color) !important;
#     }

#     /* Slider */
#     .stSlider > div > div > div {
#         background-color: var(--slider-track);
#     }
#     .stSlider > div > div > div > div {
#         background-color: var(--slider-thumb);
#         border: 2px solid var(--text-color);
#     }
#     .stSlider > div > div > div > div > div {
#         color: var(--text-color);
#         font-weight: 500;
#         font-family: 'Roboto', sans-serif !important;
#     }

#     /* Progress bar */
#     .stProgress > div > div {
#         background-color: var(--primary-color);
#     }

#     /* Selectbox and multiselect */
#     .stSelectbox > div > div, .stMultiSelect > div > div {
#         background-color: var(--secondary-background);
#         border: 2px solid var(--border-color);
#         border-radius: 5px;
#         color: var(--text-color);
#         font-family: 'Roboto', sans-serif !important;
#     }
#     .stSelectbox > div > div:hover, .stMultiSelect > div > div:hover {
#         border-color: var(--primary-color);
#     }

#     /* Text input */
#     .stTextInput > div > div > input {
#         background-color: var(--secondary-background);
#         border: 2px solid var(--border-color);
#         border-radius: 5px;
#         color: var(--text-color);
#         font-family: 'Roboto', sans-serif !important;
#     }
#     .stTextInput > div > div > input:focus {
#         border-color: var(--primary-color) !important;
#         box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2) !important;
#     }

#     /* Date input */
#     .stDateInput > div > div > input {
#         background-color: var(--secondary-background);
#         border: 2px solid var(--border-color);
#         border-radius: 5px;
#         color: var(--text-color);
#         font-family: 'Roboto', sans-serif !important;
#     }
#     .stDateInput > div > div > input:focus {
#         border-color: var(--primary-color) !important;
#         box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2) !important;
#     }

#     /* Links */
#     .stMarkdown a, .stMarkdown a:hover {
#         color: var(--primary-color);
#     }

#     /* Settings container */
#     .settings-container {
#         background-color: var(--secondary-background);
#         padding: 15px;
#         border-radius: 8px;
#         box-shadow: 0 2px 5px var(--shadow-color);
#         margin-top: 0 !important;
#         z-index: 1;
#         position: relative;
#     }

#     /* Center title */
#     .title-container {
#         text-align: center;
#         color: var(--text-color);
#     }

#     /* General typography */
#     h1, h2, h3, h4, h5, h6, p, div {
#         color: var(--text-color);
#         font-family: 'Roboto', sans-serif !important;
#     }

#     /* Improve readability for markdown */
#     .stMarkdown {
#         color: var(--text-color);
#     }

#     /* Checkbox wrapper styling to match the screenshot */
#     .databases-container {
#         background-color: var(--light-blue);
#         padding: 10px;
#         border-radius: 8px;
#         margin-bottom: 20px;
#     }
#     .checkbox-wrapper-4 * {
#         box-sizing: border-box;
#     }
#     .checkbox-wrapper-4 .cbx {
#         -webkit-user-select: none;
#         user-select: none;
#         cursor: pointer;
#         padding: 6px 12px;
#         border-radius: 6px;
#         overflow: hidden;
#         transition: all 0.2s ease;
#         display: inline-block;
#         border: 2px solid var(--border-color);
#         background-color: var(--light-blue);
#         color: var(--text-color);
#         font-family: 'Roboto', sans-serif !important;
#         font-size: 14px;
#         white-space: nowrap; /* Prevent text wrapping */
#     }
#     .checkbox-wrapper-4 .cbx:hover {
#         background: rgba(0,119,255,0.2);
#     }
#     .checkbox-wrapper-4 .cbx span {
#         vertical-align: middle;
#         transform: translate3d(0, 0, 0);
#         display: inline-flex;
#         align-items: center;
#     }
#     .checkbox-wrapper-4 .cbx span:first-child {
#         position: relative;
#         width: 18px;
#         height: 18px;
#         border-radius: 4px;
#         transform: scale(1);
#         border: 1px solid #cccfdb;
#         transition: all 0.2s ease;
#         box-shadow: 0 1px 1px rgba(0,16,75,0.05);
#         margin-right: 8px;
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#         background-color: #fff; /* White background for the checkmark box */
#     }
#     .checkbox-wrapper-4 .cbx span:first-child svg {
#         position: absolute;
#         top: 50%;
#         left: 50%;
#         transform: translate(-50%, -50%);
#         width: 12px;
#         height: 10px;
#         fill: none;
#         stroke: #007BFF;
#         stroke-width: 2;
#         stroke-linecap: round;
#         stroke-linejoin: round;
#         stroke-dasharray: 16px;
#         stroke-dashoffset: 16px;
#         transition: all 0.3s ease;
#         transition-delay: 0.1s;
#         visibility: hidden; /* Hidden by default */
#     }
#     .checkbox-wrapper-4 .cbx span:last-child {
#         line-height: 18px;
#     }
#     .checkbox-wrapper-4 .cbx:hover span:first-child {
#         border-color: #07f;
#     }
#     .checkbox-wrapper-4 .inp-cbx {
#         position: absolute;
#         visibility: hidden;
#     }
#     .checkbox-wrapper-4 .inp-cbx:checked + .cbx {
#         background: var(--primary-color);
#         border-color: var(--primary-color);
#         color: #fff;
#     }
#     .checkbox-wrapper-4 .inp-cbx:checked + .cbx span:first-child {
#         background: #fff;
#         border-color: #fff;
#         animation: wave-4 0.4s ease;
#     }
#     .checkbox-wrapper-4 .inp-cbx:checked + .cbx span:first-child svg {
#         stroke-dashoffset: 0;
#         visibility: visible; /* Show checkmark when checked */
#         stroke: #007BFF; /* Blue checkmark */
#     }
#     .checkbox-wrapper-4 .inline-svg {
#         position: absolute;
#         width: 0;
#         height: 0;
#         pointer-events: none;
#         user-select: none;
#     }
#     @media screen and (max-width: 640px) {
#         .checkbox-wrapper-4 .cbx {
#             width: 100%;
#             display: inline-block;
#         }
#     }
#     @-moz-keyframes wave-4 {
#         50% {
#             transform: scale(0.9);
#         }
#     }
#     @-webkit-keyframes wave-4 {
#         50% {
#             transform: scale(0.9);
#         }
#     }
#     @-o-keyframes wave-4 {
#         50% {
#             transform: scale(0.9);
#         }
#     }
#     @keyframes wave-4 {
#         50% {
#             transform: scale(0.9);
#         }
#     }

#     /* Ensure 2-column layout with better spacing */
#     .checkbox-grid {
#         display: flex;
#         flex-wrap: wrap;
#         gap: 15px 10px; /* Vertical and horizontal gap */
#     }
#     .checkbox-wrapper-4 {
#         margin-bottom: 10px;
#     }


#         </style>
# """, unsafe_allow_html=True)

# # Meilisearch client
# try:
#     MEILISEARCH_HOST = os.getenv("MEILISEARCH_HOST", "http://localhost:7700")
#     response = requests.get(f"{MEILISEARCH_HOST}/health", timeout=5)
#     if response.status_code != 200:
#         raise Exception("Meilisearch is not available")
#     meili_client = meilisearch.Client(
#         url=MEILISEARCH_HOST,
#         api_key=os.getenv("MEILISEARCH_API_KEY", "bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=")
#     )
#     version = meili_client.get_version()
#     logger.info(f"Meilisearch server version: {version['pkgVersion']}")
# except Exception as e:
#     st.error(f"Meilisearch connection failed: {str(e)}")
#     logger.error(f"Meilisearch connection failed: {str(e)}")
#     st.stop()

# # PostgreSQL connection
# def get_db_connection():
#     try:
#         conn = psycopg2.connect(
#             dbname=os.getenv("PG_DB", "your_db"),
#             user=os.getenv("PG_USER", "your_user"),
#             password=os.getenv("PG_PASSWORD", "your_password"),
#             host=os.getenv("PG_HOST", "localhost"),
#             port=os.getenv("PG_PORT", "5432")
#         )
#         return conn
#     except Exception as e:
#         st.error(f"PostgreSQL connection failed: {str(e)}")
#         logger.error(f"PostgreSQL connection failed: {str(e)}")
#         raise

# # Fetch sub-module names
# @st.cache_data
# def get_sub_module_names():
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT name FROM sub_module ORDER BY name")
#         sub_modules = [row[0] for row in cur.fetchall()]
#         cur.close()
#         conn.close()
#         return sub_modules
#     except Exception as e:
#         st.error(f"Error fetching sub-modules: {str(e)}")
#         logger.error(f"Error fetching sub-modules: {str(e)}")
#         return [
#             "GBV", "Stolen Lost Item", "Robbery", "Rape", "Motor Vehicle Theft", "Missing Person",
#             "Homicide", "Death", "Cyber Crime", "Burglary", "Assault", "Arson"
#         ]

# # Check if index exists
# def index_exists(index_name="incidents"):
#     try:
#         meili_client.index(index_name).get_stats()
#         return True
#     except meilisearch.errors.MeilisearchApiError as e:
#         if e.code == "index_not_found":
#             return False
#         raise

# # Create Meilisearch index
# def create_meilisearch_index(index_name="incidents"):
#     try:
#         response = requests.post(
#             f"{MEILISEARCH_HOST}/indexes",
#             headers={
#     "Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY', 'bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=')}",
#                 "Content-Type": "application/json"
#             },
#             json={"uid": index_name, "primaryKey": "id"}
#         )
#         if response.status_code not in [200, 201, 202]:
#             raise Exception(f"Failed to create index: {response.text}")
#         task = meili_client.get_task(response.json().get("taskUid", response.json().get("uid")))
#         task_id = getattr(task, "task_uid", getattr(task, "uid", None))
#         if not task_id:
#             raise Exception("Task ID not found in response")
#         meili_client.wait_for_task(task_id, timeout_in_ms=180000)
#         logger.info("Meilisearch index created.")
#         return True
#     except Exception as e:
#         st.error(f"Error creating index: {str(e)}")
#         logger.error(f"Error creating index: {str(e)}")
#         raise

# # Set index settings
# def set_index_settings(index_name="incidents"):
#     try:
#         index = meili_client.index(index_name)
#         task = index.update_settings({
#             "searchableAttributes": ["*"],
#             "filterableAttributes": [
#                 "sub_module_name", "stolen_items", "electronic_type", "document_type",
#                 "vehicle_registration", "victim_name", "gbv_type", "cause_of_death",
#                 "mental_condition", "suspect_presence", "submissionDate", "suspect_name",
#                 "suspect_description"
#             ],
#             "typoTolerance": {
#                 "enabled": True,
#                 "minWordSizeForTypos": {"oneTypo": 2, "twoTypos": 4}
#             },
#             "rankingRules": [
#                 "words",
#                 "typo",
#                 "proximity",
#                 "attribute",
#                 "sort",
#                 "exactness"
#             ]
#         })
#         task_id = getattr(task, "task_uid", getattr(task, "uid", None))
#         if not task_id:
#             raise Exception("Task ID not found for index settings")
#         meili_client.wait_for_task(task_id, timeout_in_ms=180000)
#         logger.info("Index settings updated.")
#         return True
#     except Exception as e:
#         st.error(f"Error setting index settings: {str(e)}")
#         logger.error(f"Error setting index settings: {str(e)}")
#         raise

# # Index Meilisearch data from PostgreSQL
# def index_meilisearch_data():
#     try:
#         index_name = "incidents"
#         # Delete existing index
#         try:
#             response = requests.delete(
#                 f"{MEILISEARCH_HOST}/indexes/{index_name}",
#                 headers={
#                     "Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY', 'bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=')}"
#                 }
#             )
#             if response.status_code not in [200, 202, 204]:
#                 logger.warning(f"Failed to delete index: {response.text}")
#             else:
#                 task = meili_client.get_task(response.json().get("taskUid", response.json().get("uid")))
#                 task_id = getattr(task, "task_uid", getattr(task, "uid", None))
#                 if task_id:
#                     meili_client.wait_for_task(task_id, timeout_in_ms=180000)
#                 logger.info("Existing index deleted.")
#         except Exception as e:
#             logger.warning(f"Index deletion skipped (may not exist): {str(e)}")

#         # Create index and set settings
#         create_meilisearch_index(index_name)
#         set_index_settings(index_name)

#         # Fetch data from PostgreSQL
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT smd."id", smd."sub_moduleId", smd."submissionDate", smd."formData", smd."location", smd."narrative",
#                    sm.name as sub_module_name
#             FROM sub_module_data smd
#             JOIN sub_module sm ON smd."sub_moduleId" = sm.id
#             WHERE sm.name IN ('GBV', 'Stolen Lost Item', 'Robbery', 'Rape', 'Motor Vehicle Theft', 'Missing Person',
#                              'Homicide', 'Death', 'Cyber Crime', 'Burglary', 'Assault', 'Arson')
#         """)
#         chunk_size = 1000
#         documents = []
#         total_records = 0
#         progress_bar = st.progress(0)
#         status_text = st.empty()

#         # Estimate total records
#         cur_count = conn.cursor()
#         cur_count.execute("""
#             SELECT COUNT(*)
#             FROM sub_module_data smd
#             JOIN sub_module sm ON smd."sub_moduleId" = sm.id
#             WHERE sm.name IN ('GBV', 'Stolen Lost Item', 'Robbery', 'Rape', 'Motor Vehicle Theft', 'Missing Person',
#                              'Homicide', 'Death', 'Cyber Crime', 'Burglary', 'Assault', 'Arson')
#         """)
#         total_expected = cur_count.fetchone()[0]
#         cur_count.close()

#         while True:
#             rows = cur.fetchmany(chunk_size)
#             if not rows:
#                 break
#             for row in rows:
#                 form_data = row[3] or {}
#                 logger.debug(f"Raw formData for ID {row[0]}: {json.dumps(form_data, indent=2)}")
#                 searchable_values = []
#                 for key, value in form_data.items():
#                     if isinstance(value, str):
#                         searchable_values.append(value)
#                     elif value is not None:
#                         searchable_values.append(str(value))
#                 searchable_values.extend(filter(None, [
#                     row[4] or '', row[5] or '', row[6] or ''
#                 ]))
#                 searchable_text = " ".join(searchable_values)
#                 submission_date = None
#                 if row[2] and isinstance(row[2], datetime):
#                     submission_date = row[2].isoformat()
#                 else:
#                     logger.warning(f"Invalid or missing submissionDate for ID {row[0]}")
#                 doc = {
#                     "id": row[0],
#                     "sub_moduleId": row[1],
#                     "sub_module_name": row[6],
#                     "submissionDate": submission_date,
#                     "location": row[4] or form_data.get("location"),
#                     "narrative": row[5],
#                     "description": (
#                         form_data.get("Give a brief narrative of what happened") or
#                         form_data.get("A brief narrative of what happened") or
#                         form_data.get("A brief description of the person") or "N/A"
#                     ),
#                     "type_of_property": (
#                         form_data.get("Type of property") or
#                         form_data.get("select type of property broken into")
#                     ),
#                     "victim_name": (
#                         form_data.get("Name of the casualty") or
#                         form_data.get("Name of the victim") or
#                         form_data.get("Name of the deceased") or
#                         form_data.get("Name")
#                     ),
#                     "vehicle_make": form_data.get("Make"),
#                     "vehicle_model": form_data.get("Model"),
#                     "vehicle_registration": form_data.get("Registration number"),
#                     "stolen_items": form_data.get("What category of items were stolen"),
#                     "electronic_type": form_data.get("type of electronic"),
#                     "document_type": form_data.get("type of Documents"),
#                     "gbv_type": form_data.get("Type of GBV"),
#                     "cause_of_death": form_data.get("Cause of death"),
#                     "mental_condition": form_data.get("Mental Condition"),
#                     "suspect_presence": form_data.get("Do you have a suspect"),
#                     "suspect_name": form_data.get("Name of the suspect"),
#                     "suspect_description": (
#                         form_data.get("Description of the suspect") or
#                         form_data.get("Give details about the suspect")
#                     ),
#                     "cyber_incident": form_data.get("Select Incident"),
#                     "platform_digital_violence": form_data.get("Platform In Digital or Online Violence"),
#                     "searchable_text": searchable_text,
#                     "formData": form_data
#                 }
#                 for key, value in form_data.items():
#                     doc[key] = value
#                 documents.append(doc)
#             total_records += len(rows)
#             progress = min(total_records / total_expected if total_expected > 0 else 1.0, 1.0)
#             progress_bar.progress(progress)
#             status_text.text(f"Indexed {total_records} of approximately {total_expected} records...")
#             logger.debug(f"Processed {total_records} records so far")
#         cur.close()
#         conn.close()
#         if documents:
#             index = meili_client.index(index_name)
#             task = index.add_documents(documents)
#             task_id = getattr(task, "task_uid", getattr(task, "uid", None))
#             if not task_id:
#                 raise Exception("Task ID not found for document indexing")
#             meili_client.wait_for_task(task_id, timeout_in_ms=300000)
#             progress_bar.progress(1.0)
#             status_text.text(f"Indexed {total_records} documents in Meilisearch.")
#             st.success(f"Indexed {total_records} documents in Meilisearch.")
#         else:
#             progress_bar.progress(1.0)
#             status_text.text("No documents retrieved from database.")
#             st.warning("No documents retrieved from database.")
#         return True
#     except Exception as e:
#         progress_bar.progress(1.0)
#         status_text.text(f"Indexing failed: {str(e)}")
#         st.error(f"Meilisearch indexing error: {str(e)}")
#         logger.error(f"Meilisearch indexing error: {str(e)}")
#         return False

# # Debug suspect names
# def debug_suspect_names(index_name="incidents"):
#     try:
#         index = meili_client.index(index_name)
#         results = index.search("", {
#             "filter": "suspect_presence = 'Yes' AND (suspect_name IS NOT NULL OR suspect_description IS NOT NULL)",
#             "limit": 10,
#             "attributesToRetrieve": ["suspect_name", "suspect_description", "sub_module_name", "id"]
#         })
#         if results["hits"]:
#             st.write("Sample suspect names and descriptions in Meilisearch:")
#             for hit in results["hits"]:
#                 st.write(f"- ID: {hit['id']}, Sub-module: {hit['sub_module_name']}, Suspect: {hit.get('suspect_name', 'N/A')}, Description: {hit.get('suspect_description', 'N/A')}")
#         else:
#             st.warning("No documents found with suspect names or descriptions in Meilisearch.")
#         logger.debug(f"Debug suspect names: {json.dumps(results, indent=2)}")
#     except Exception as e:
#         st.error(f"Error debugging suspect names: {str(e)}")
#         logger.error(f"Error debugging suspect names: {str(e)}")

# # Debug indexed documents
# def debug_indexed_documents(index_name="incidents"):
#     try:
#         index = meili_client.index(index_name)
#         results = index.search("", {
#             "limit": 10,
#             "attributesToRetrieve": ["*"]
#         })
#         if results["hits"]:
#             st.write("Sample documents in Meilisearch index:")
#             for hit in results["hits"]:
#                 st.write(f"- ID: {hit['id']}, Sub-module: {hit.get('sub_module_name', 'N/A')}")
#                 st.write(f"  Location: {hit.get('location', 'N/A')}")
#                 st.write(f"  Submission Date: {hit.get('submissionDate', 'N/A')}")
#                 st.write(f"  Description: {hit.get('description', 'N/A')}")
#                 st.write(f"  Suspect Name: {hit.get('suspect_name', 'N/A')}")
#                 st.write(f"  Suspect Description: {hit.get('suspect_description', 'N/A')}")
#                 st.write(f"  Searchable Text: {hit.get('searchable_text', 'N/A')[:100]}...")
#                 st.write(f"  Form Data: {json.dumps(hit.get('formData', {}), indent=2)[:200]}...")
#         else:
#             st.warning("No documents found in Meilisearch index.")
#         logger.debug(f"Debug indexed documents: {json.dumps(results, indent=2)}")
#     except Exception as e:
#         st.error(f"Error debugging indexed documents: {str(e)}")
#         logger.error(f"Error debugging indexed documents: {str(e)}")

# # Automatic index creation on startup
# if not index_exists("incidents"):
#     st.info("Incidents index not found. Creating and indexing data...")
#     try:
#         index_meilisearch_data()
#     except Exception as e:
#         st.error(f"Failed to create and index data: {str(e)}")
#         logger.error(f"Failed to create and index data: {str(e)}")
#         st.stop()

# # Main UI, matching the snippet's structure
# st.markdown('<div class="title-container"><h1>🔍 What are you looking for?</h1></div>', unsafe_allow_html=True)

# with st.container():
#     # Categories (formerly Databases)
#     st.markdown("### Databases")
#     database_options = [
#         "ALL",
#         "WATCHLIST DB",
#         "STOLEN/LOST ITEMS DB",
#         "MISSING PERSONS DB",
#         "EVIDENCE DB",
#         "STOLEN VEHICLES DB",
#         "PRISONER PROPERTY DB"
#     ]
#     selected_databases = []

#     # Initialize session state for checkboxes - all unselected by default
#     if 'database_selections' not in st.session_state:
#         st.session_state.database_selections = {option: False for option in database_options}

#     # Create a form to handle state updates
#     with st.form(key="database_form", clear_on_submit=False):
#         # Create a 2-column layout
#         cols = st.columns(2)
#         st.markdown('<div class="checkbox-grid">', unsafe_allow_html=True)
#         for i, option in enumerate(database_options):
#             col_idx = i % 2  # Distribute across 2 columns
#             # Calculate width based on text length (approximate: 10px per character + padding)
#             text_length = len(option)
#             width = max(100, text_length * 10 + 30)  # Adjusted multiplier for better fit

#             with cols[col_idx]:
#                 # Get current state
#                 checked = st.session_state.database_selections[option]

#                 # Custom checkbox HTML
#                 st.markdown(
#                     f'''
#                     <div class="checkbox-wrapper-4">
#                         <input class="inp-cbx" id="cbx_{option}" name="cbx_{option}" type="checkbox" {'checked' if checked else ''}/>
#                         <label class="cbx" for="cbx_{option}" style="width: {width}px;">
#                             <span>
#                                 <svg width="12px" height="10px">
#                                     <use xlink:href="#check-4"></use>
#                                 </svg>
#                             </span>
#                             <span>{option}</span>
#                         </label>
#                         <svg class="inline-svg">
#                             <symbol id="check-4" viewbox="0 0 12 10">
#                                 <polyline points="1.5 6 4.5 9 10.5 1"></polyline>
#                             </symbol>
#                         </svg>
#                     </div>
#                     ''',
#                     unsafe_allow_html=True
#                 )

#         st.markdown('</div>', unsafe_allow_html=True)

#         # Submit button
#         submitted = st.form_submit_button("Update")

#         # Update session state based on form submission
#         if submitted:
#             for option in database_options:
#                 if f"cbx_{option}" in st.session_state:
#                     st.session_state.database_selections[option] = st.session_state[f"cbx_{option}"]
#                 if option == "ALL" and st.session_state.database_selections["ALL"]:
#                     for opt in database_options:
#                         st.session_state.database_selections[opt] = True
#                 elif option != "ALL" and not st.session_state.database_selections["ALL"]:
#                     # Ensure "ALL" is unchecked if any other is unchecked
#                     if not st.session_state.database_selections[option]:
#                         st.session_state.database_selections["ALL"] = False

#     st.markdown('</div>', unsafe_allow_html=True)  # Close databases-container

#     # Keywords with placeholder
#     st.markdown("### Keywords")
#     query = st.text_input(
#         "Enter keywords...",
#         label_visibility="collapsed",
#         key="query_input",
#         placeholder="Enter keywords..."
#     )

#     # Dynamic Date Range (one month apart)
#     st.markdown("### Date Range")
#     today = date(2025, 6, 5)  # Current date based on system time
#     start_date = st.date_input("Start Date", value=today, key="start_date")
#     end_date = st.date_input("End Date", value=today + timedelta(days=30), key="end_date")

#     # Number of Results
#     #st.markdown("### Results to show")
#     #limit = st.slider("Number of results", min_value=1, max_value=50, value=10, key="results_slider")

#     # Collect selected databases
#     selected_databases = [opt for opt in database_options if st.session_state.database_selections[opt]]

# # Optional: Display selected databases for debugging
# #st.write("Selected Databases:", selected_databases)




#     # Number of Results
#     #st.markdown("### #️⃣ Results to show")
#     #limit = st.slider("Number of results", min_value=1, max_value=50, value=10, key="results_slider")

# # More Filters (including Report/OB and Settings)
# with st.expander("More Filters"):
#     # Report/OB (formerly in sidebar)
#     st.markdown("#### Report/OB")
#     sub_module_filter = st.multiselect(
#         "Select Sub-modules",
#         get_sub_module_names(),
#         key="sub_module_filter"
#     )

#     # Additional Filters (similar to snippet)
#     include_watchlist = st.checkbox("Include Watchlist", key="include_watchlist")
#     exact_match = st.checkbox("Exact Match", key="exact_match")
#     show_archived = st.checkbox("Show Archived Records", key="show_archived")

#     # Settings (moved into expander)
#     st.markdown("#### Settings")
#     st.markdown('<div class="settings-container">', unsafe_allow_html=True)
#     setting_action = st.selectbox(
#         "Settings Action:",
#         ["None", "Create Meilisearch Index", "Index Data", "Debug Suspect Names", "Debug Indexed Documents"],
#         key="settings_select"
#     )
#     if setting_action != "None" and st.button("Execute", key="execute_button"):
#         if setting_action == "Create Meilisearch Index":
#             try:
#                 create_meilisearch_index()
#                 set_index_settings()
#                 st.success("Meilisearch index created and configured.")
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")
#         elif setting_action == "Index Data":
#             index_meilisearch_data()
#         elif setting_action == "Debug Suspect Names":
#             debug_suspect_names()
#         elif setting_action == "Debug Indexed Documents":
#             debug_indexed_documents()
#     st.markdown('</div>', unsafe_allow_html=True)

# # Actions
# st.markdown("### Actions")
# col1, col2 = st.columns(2)
# if col1.button("🔍 Search", key="main_search_button"):
#     if query:
#         # Ensure at least one database is selected
#         if not selected_databases:
#             st.session_state.database_selections["ALL"] = True
#             for option in database_options:
#                 st.session_state.database_selections[option] = True
#             selected_databases = database_options
#             st.warning("No databases selected. Defaulting to ALL databases.")
#         try:
#             index = meili_client.index("incidents")
#             filters = []
#             if "ALL" not in selected_databases or len(selected_databases) < len(database_options):
#                 for db_type in selected_databases:
#                     if db_type == "WATCHLIST DB":
#                         filters.append("victim_name IS NOT NULL")
#                     elif db_type == "STOLEN/LOST ITEMS DB":
#                         filters.append("stolen_items IS NOT NULL OR electronic_type IS NOT NULL OR document_type IS NOT NULL")
#                     elif db_type == "MISSING PERSONS DB":
#                         filters.append("sub_module_name = 'Missing Person'")
#                     elif db_type == "EVIDENCE DB":
#                         filters.append("narrative IS NOT NULL OR description IS NOT NULL")
#                     elif db_type == "STOLEN VEHICLES DB":
#                         filters.append("sub_module_name = 'Motor Vehicle Theft' OR vehicle_registration IS NOT NULL")
#                     elif db_type == "PRISONER PROPERTY DB":
#                         filters.append("stolen_items IS NOT NULL")
#             if sub_module_filter:
#                 sub_module_list = ', '.join(f'"{sm}"' for sm in sub_module_filter)
#                 filters.append(f"sub_module_name IN [{sub_module_list}]")
#             if start_date and end_date:
#                 start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
#                 end_ts = int(datetime.combine(end_date, datetime.max.time()).timestamp())
#                 filters.append(f"submissionDate >= {start_ts} AND submissionDate <= {end_ts}")
#             # Apply additional filters
#             if include_watchlist:
#                 filters.append("victim_name IS NOT NULL")  # Example filter for watchlist
#             if exact_match:
#                 # Meilisearch exact match can be approximated with phrase search
#                 query = f'"{query}"'
#             # 'Show Archived' filter not implemented as it requires schema support
#             filter_str = " AND ".join(filters) if filters else None
#             logger.debug(f"Search query: {query}")
#             logger.debug(f"Search filters: {filter_str}")
#             st.write(f"Search query: {query}")
#             st.write(f"Search filters: {filter_str if filter_str else 'None'}")
#             results = index.search(query, {
#                 "limit": limit,
#                 "filter": filter_str,
#                 "attributesToRetrieve": ["*"]
#             })["hits"]
#             st.info("Search performed using full-text search across all fields.")
#             st.write(f"Found {len(results)} results")
#             if not results:
#                 st.warning("No results found with current query/filters. Trying search without filters...")
#                 results = index.search(query, {
#                     "limit": limit,
#                     "filter": None,
#                     "attributesToRetrieve": ["*"]
#                 })["hits"]
#                 st.write(f"Found {len(results)} results without filters")
#                 if not results:
#                     st.warning("Still no results. Check 'Debug Indexed Documents' to verify index contents or try a different query.")
#             for hit in results:
#                 with st.expander(f"{hit.get('sub_module_name', 'N/A')} - ID: {hit['id']}"):
#                     st.markdown(f"**Location**: {hit.get('location', 'N/A')}")
#                     st.markdown(f"**Submission Date**: {hit.get('submissionDate', 'N/A')}")
#                     st.markdown(f"**Description**: {hit.get('description', 'N/A')}")
#                     if hit.get('suspect_name'):
#                         st.markdown(f"**Suspect Name**: {hit['suspect_name']}")
#                     if hit.get('suspect_description'):
#                         st.markdown(f"**Suspect Description**: {hit['suspect_description']}")
#                     st.markdown("**Form Data**:")
#                     for key, value in hit.get('formData', {}).items():
#                         st.markdown(f"- **{key}**: {value}")
#                     st.markdown(f"**Score**: {hit.get('_rankingScore', 1.0):.2f}")
#         except Exception as e:
#             st.error(f"Search error: {str(e)}")
#             logger.error(f"Search error: {str(e)}")
#     else:
#         st.warning("Please enter a search query.")

# if col2.button("↩ Reset", key="reset_button"):
#     # Reset session state and rerun
#     st.session_state.clear()
#     st.experimental_rerun()
