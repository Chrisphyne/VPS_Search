# import streamlit as st
# import meilisearch
# import psycopg2
# import os
# import logging
# import json
# import requests
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import meilisearch.errors

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Streamlit app configuration
# st.set_page_config(page_title="Incident Search DBs", layout="wide", page_icon="🔍")

# # Apply deep blue theme CSS with yellow/gold Search button
# st.markdown("""
#     <style>
#     /* Primary buttons (except Search) */
#     .stButton > button:not([id='search_button']) {
#         background-color: #FFD700;
#         color: white;
#         border-color: #003087;
#         border-radius: 5px;
#         padding: 0.5rem 1rem;
#     }
#     .stButton > button:not([id='search_button']):hover {
#         background-color: #0041b3;
#         border-color: #0041b3;
#         color: white;
#     }
#     /* Search button */
#     .stButton > button[id='search_button'] {
#         background-color: #FFD700;
#         color: black;
#         border-color: #FFD700;
#         border-radius: 5px;
#         padding: 0.5rem 1rem;
#     }
#     .stButton > button[id='search_button']:hover {
#         background-color: #FFC107;
#         border-color: #FFC107;
#         color: black;
#     }
#     /* Checkboxes (Databases) */
#     .stCheckbox > label > div > div {
#         background-color: #454746;
#         border-color: #454746;
#         border-radius: 5px;
#         padding: 0.5rem;
#         color: white;
#     }
#     .stCheckbox > label > div > div:hover {
#         background-color: #454746;
#         border-color: #454746;
#     }
#     /* Expander toggle */
#     .streamlit-expanderHeader {
#         background-color: #003087 !important;
#         color: white !important;
#         border-radius: 5px;
#     }
#     .streamlit-expanderHeader:hover {
#         background-color: #0041b3 !important;
#     }
#     /* Slider */
#     .stSlider > div > div > div {
#         background-color: #454746;
#     }
#     /* Progress bar */
#     .stProgress > div > div {
#         background-color: #454746;
#     }
#     /* Selectbox and multiselect */
#     .stSelectbox > div > div, .stMultiSelect > div > div {
#         border-color: #454746;
#         /* border-color: #454746; */

#     }
#     .stSelectbox > div > div:hover, .stMultiSelect > div > div:hover {
#         border-color: #454746;
#     }
#     /* Remove gold/orange highlights */
#     .stMarkdown a, .stMarkdown a:hover {
#         color: #454746;
#     }
#     /* General text input focus */
#     input:focus {
#         border-color: #003087 !important;
#         box-shadow: 0 0 0 2px rgba(0, 48, 135, 0.3) !important;
#     }
#     /* Settings container */
#     .settings-container {
#         background-color: #f0f2f6;
#         padding: 10px;
#         border-radius: 5px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.2);
#     }
#     /* Center title */
#     .title-container {
#         text-align: center;
#     }
#     /* Center description */
#     .description-container {
#         text-align: center;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Center title with search icon
# st.markdown('<div class="title-container"><h1>Search 🔍</h1></div>', unsafe_allow_html=True)
# st.markdown('<div class="description-container"><p> Search for lost items, vehicles, persons, or incidents using full-text search across all fields. </p></div>', unsafe_allow_html=True)
# # st.markdown("Search for lost items, vehicles, persons, or incidents using full-text search across all fields.")

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
#                 "Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY', 'bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=')}",
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

# # # Settings with toggle
# # col1, col2 = st.columns([3, 1])
# # with col2:
# #     # Initialize session state
# #     if 'show_settings' not in st.session_state:
# #         st.session_state.show_settings = False
# #     # Checkbox for toggling settings
# #     st.checkbox("Show Settings", value=st.session_state.show_settings, key="show_settings")
# #     if st.session_state.show_settings:
# #         with st.container():
# #             st.markdown('<div class="settings-container">', unsafe_allow_html=True)
# #             setting_action = st.selectbox(
# #                 "Settings:",
# #                 ["None", "Create Meilisearch Index", "Index Data", "Debug Suspect Names", "Debug Indexed Documents"],
# #                 key="settings_select"
# #             )
# #             if setting_action != "None" and st.button("Execute"):
# #                 if setting_action == "Create Meilisearch Index":
# #                     try:
# #                         create_meilisearch_index()
# #                         set_index_settings()
# #                         st.success("Meilisearch index created and configured.")
# #                     except Exception as e:
# #                         st.error(f"Error: {str(e)}")
# #                 elif setting_action == "Index Data":
# #                     index_meilisearch_data()
# #                 elif setting_action == "Debug Suspect Names":
# #                     debug_suspect_names()
# #                 elif setting_action == "Debug Indexed Documents":
# #                     debug_indexed_documents()
# #             st.markdown('</div>', unsafe_allow_html=True)





# # # Settings at top right
# col1, col2 = st.columns([3, 1])
# with col2:
#     setting_action = st.selectbox(
#         "Settings:",
#         ["None", "Create Meilisearch Index", "Index Data", "Debug Suspect Names", "Debug Indexed Documents"],
#         key="settings_select"
#     )
#     if setting_action != "None" and st.button("Execute"):
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








# # Automatic index creation on startup
# if not index_exists("incidents"):
#     st.info("Incidents index not found. Creating and indexing data...")
#     try:
#         index_meilisearch_data()
#     except Exception as e:
#         st.error(f"Failed to create and index data: {str(e)}")
#         logger.error(f"Failed to create and index data: {str(e)}")
#         st.stop()

# # Sidebar: Databases and Report/OB Menu
# with st.sidebar:
#     st.header("Filters")
#     st.subheader("Databases")
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

#     # Initialize session state for checkboxes
#     if 'database_selections' not in st.session_state:
#         st.session_state.database_selections = {option: True for option in database_options}

#     # Handle checkbox selections
#     all_checked = st.checkbox("ALL", value=st.session_state.database_selections["ALL"], key="db_ALL")
#     if all_checked != st.session_state.database_selections["ALL"]:
#         for option in database_options:
#             st.session_state.database_selections[option] = all_checked
#     else:
#         for option in database_options[1:]:
#             checked = st.checkbox(option, value=st.session_state.database_selections[option], key=f"db_{option}")
#             st.session_state.database_selections[option] = checked
#         # If any non-ALL option is unchecked, uncheck ALL
#         if not all(st.session_state.database_selections[opt] for opt in database_options[1:]):
#             st.session_state.database_selections["ALL"] = False
#         # If all non-ALL options are checked, check ALL
#         elif all(st.session_state.database_selections[opt] for opt in database_options[1:]):
#             st.session_state.database_selections["ALL"] = True

#     # Collect selected databases
#     selected_databases = [opt for opt in database_options if st.session_state.database_selections[opt]]
#     if not selected_databases:
#         st.session_state.database_selections["ALL"] = True
#         for option in database_options:
#             st.session_state.database_selections[option] = True
#         selected_databases = database_options

#     st.subheader("Report/OB")
#     sub_module_filter = st.multiselect(" ", get_sub_module_names())

# # Search interface
# col1, col2 = st.columns(2)
# with col1:
#     query = st.text_input("SEARCH QUERY:", placeholder="e.g., karanja, lost laptop, Johncoursedoe")
#     # Place Start Date and End Date on the same row
#     date_col1, date_col2 = st.columns(2)
#     with date_col1:
#         default_start = datetime.now().date() - timedelta(days=30)
#         start_date = st.date_input("START DATE:", default_start, key="start_date")
#     with date_col2:
#         default_end = datetime.now().date()
#         end_date = st.date_input("END DATE:", default_end, key="end_date")
# with col2:
#     limit = st.slider("Number of results:", 1, 50, 10)

# if st.button("Search", key="search_button"):
#     if query:
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
#                         filters.append("narrative IS NOT NULL OR description IS NOT NULL")  # Placeholder
#                     elif db_type == "STOLEN VEHICLES DB":
#                         filters.append("sub_module_name = 'Motor Vehicle Theft' OR vehicle_registration IS NOT NULL")
#                     elif db_type == "PRISONER PROPERTY DB":
#                         filters.append("stolen_items IS NOT NULL")  # Placeholder
#             if sub_module_filter:
#                 sub_module_list = ', '.join(f'"{sm}"' for sm in sub_module_filter)
#                 filters.append(f"sub_module_name IN [{sub_module_list}]")
#             if start_date and end_date:
#                 start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
#                 end_ts = int(datetime.combine(end_date, datetime.max.time()).timestamp())
#                 filters.append(f"submissionDate >= {start_ts} AND submissionDate <= {end_ts}")
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





# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Streamlit app configuration
# st.set_page_config(page_title="Incident Search", layout="wide", page_icon="🔍")

import streamlit as st
import meilisearch
import psycopg2
import os
import logging
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import meilisearch.errors

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Streamlit app configuration
st.set_page_config(page_title="Incident Search DBs", layout="wide", page_icon="🔍")

# Apply custom theme CSS with white background, deeper grey buttons, vibrant blue accents, and Roboto font
# Colors align with config.toml: primaryColor=#007BFF, backgroundColor=#F5F6F5, secondaryBackgroundColor=#E7EDE9, textColor=#000000
st.markdown("""
    <style>
    /* Import Roboto from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* Root variables for theme consistency */
    :root {
        --primary-color: #007BFF; /* Vibrant Blue from config.toml */
        --background-color: #F5F6F5; /* Soft White from config.toml */
        --secondary-background: #E7EDE9; /* Light Grey-Green from config.toml */
        --text-color: #000000; /* Black from config.toml */
        --button-color: #4A4A4A; /* Deep Grey for buttons */
        --button-hover: #6B6B6B; /* Lighter Deep Grey for button hover */
        --border-color: #D3D3D3; /* Light Grey for borders */
        --shadow-color: rgba(0, 0, 0, 0.1);
        --accent-color: #007BFF; /* Vibrant Blue for accents and focus */
        --checkbox-checked: #007BFF; /* Blue for checked checkboxes */
        --slider-track: #E7EDE9; /* Light Grey-Green for slider track */
        --slider-thumb: #007BFF; /* Blue for slider thumb */
    }

    /* Main container and sidebar */
    .main, .css-1v3fvcr {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--secondary-background);
        color: var(--text-color);
        padding: 1rem;
    }

    /* Primary buttons */
    .stButton > button {
        background-color: var(--button-color);
        color: var(--text-color);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'Roboto', sans-serif !important;
    }
    .stButton > button:hover {
        background-color: var(--button-hover);
        color: var(--text-color);
        border-color: var(--button-hover);
    }

    /* Checkboxes */
    .stCheckbox > label > div > div {
        background-color: var(--secondary-background);
        border: 2px solid var(--border-color);
        border-radius: 4px;
        padding: 0.3rem;
        color: var(--text-color);
        transition: all 0.3s ease;
        font-family: 'Roboto', sans-serif !important;
    }
    .stCheckbox > label > div:hover > div {
        background-color: var(--border-color);
        border-color: var(--border-color);
    }
    .stCheckbox > label > input:checked + div > div {
        background-color: var(--checkbox-checked);
        border-color: var(--checkbox-checked);
    }

    /* Expander toggle */
    .streamlit-expanderHeader {
        background-color: var(--secondary-background) !important;
        color: var(--text-color) !important;
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
        font-family: 'Roboto', sans-serif !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: var(--border-color) !important;
    }

    /* Slider */
    .stSlider > div > div {
        background-color: var(--slider-track);
    }
    .stSlider > div > div > div {
        background-color: var(--slider-thumb);
        border: 2px solid var(--text-color);
    }
    .stSlider > div > div > div > div {
        color: var(--text-color);
        font-weight: 500;
        font-family: 'Roboto', sans-serif !important;
    }

    /* Progress bar */
    .stProgress .stProgress-bar {
        background-color: var(--primary-color);
    }

    /* Selectbox and multiselect */
    .stSelectbox > div > div, .stMultiSelect > div {
        background-color: var(--secondary-background);
        border: 2px solid var(--border-color);
        border-radius: 4px;
        color: var(--text-color);
        font-family: 'Roboto', sans-serif !important;
    }
    .stSelectbox > div:hover > div, .stMultiSelect > div:hover {
        border-color: var(--primary-color);
    }

    /* Text input */
    .stTextInput > div > div > input {
        background-color: var(--secondary-background);
        border: 2px solid var(--border-color);
        border-radius: 4px;
        color: var(--text-color);
        font-family: 'Roboto', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2) !important;
    }

    /* Date input */
    .stDateInput > div > div > input {
        background-color: var(--secondary-background);
        border: 2px solid var(--border-color);
        border-radius: 4px;
        color: var(--text-color);
        font-family: 'Roboto', sans-serif !important;
    }
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2) !important;
    }

    /* Links */
    .stMarkdown a, .stMarkdown a:hover {
        color: var(--primary-color);
    }

    /* Settings container */
    .settings-container {
        background-color: var(--secondary-background);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px var(--shadow-color);
        margin-top: 0 !important;
        z-index: 1;
        position: relative;
    }

    /* Center title and description */
    .title-container, .description-container {
        text-align: center;
        color: var(--text-color);
    }

    /* General typography */
    h1, h2, h3, h4, h5, h6, p, div, button, input, select, label {
        color: var(--text-color);
        font-family: 'Roboto', sans-serif !important;
    }

    /* Improve readability for markdown */
    .stMarkdown {
        color: var(--text-color);
    }

    /* Fix settings section overlap */
    .css-1kyxreq {
        margin-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Center title with search icon
st.markdown('<div class="title-container"><h1>Search 🔍</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="description-container"><p>Search for lost items, vehicles, persons, or incidents using full-text search across all fields.</p></div>', unsafe_allow_html=True)

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

# Check if index exists
def index_exists(index_name="incidents"):
    try:
        meili_client.index(index_name).get_stats()
        return True
    except meilisearch.errors.MeilisearchApiError as e:
        if e.code == "index_not_found":
            return False
        raise

# Create Meilisearch index
def create_meilisearch_index(index_name="incidents"):
    try:
        response = requests.post(
            f"{MEILISEARCH_HOST}/indexes",
            headers={
                "Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY', 'bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=')}",
                "Content-Type": "application/json"
            },
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

# Set index settings
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
            "typoTolerance": {
                "enabled": True,
                "minWordSizeForTypos": {"oneTypo": 2, "twoTypos": 4}
            },
            "rankingRules": [
                "words",
                "typo",
                "proximity",
                "attribute",
                "sort",
                "exactness"
            ]
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

# Index Meilisearch data from PostgreSQL
def index_meilisearch_data():
    try:
        index_name = "incidents"
        # Delete existing index
        try:
            response = requests.delete(
                f"{MEILISEARCH_HOST}/indexes/{index_name}",
                headers={
                    "Authorization": f"Bearer {os.getenv('MEILISEARCH_API_KEY', 'bMMgZDJq0JtbHieMIdAfuDYmUe1z3nU4bVQ/+9IQPck=')}"
                }
            )
            if response.status_code not in [200, 202, 204]:
                logger.warning(f"Failed to delete index: {response.text}")
            else:
                task = meili_client.get_task(response.json().get("taskUid", response.json().get("uid")))
                task_id = getattr(task, "task_uid", getattr(task, "uid", None))
                if task_id:
                    meili_client.wait_for_task(task_id, timeout_in_ms=180000)
                logger.info("Existing index deleted.")
        except Exception as e:
            logger.warning(f"Index deletion skipped (may not exist): {str(e)}")

        # Create index and set settings
        create_meilisearch_index(index_name)
        set_index_settings(index_name)

        # Fetch data from PostgreSQL
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

        # Estimate total records
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
                logger.debug(f"Raw formData for ID {row[0]}: {json.dumps(form_data, indent=2)}")
                searchable_values = []
                for key, value in form_data.items():
                    if isinstance(value, str):
                        searchable_values.append(value)
                    elif value is not None:
                        searchable_values.append(str(value))
                searchable_values.extend(filter(None, [
                    row[4] or '', row[5] or '', row[6] or ''
                ]))
                searchable_text = " ".join(searchable_values)
                submission_date = None
                if row[2] and isinstance(row[2], datetime):
                    submission_date = row[2].isoformat()
                else:
                    logger.warning(f"Invalid or missing submissionDate for ID {row[0]}")
                doc = {
                    "id": row[0],
                    "sub_moduleId": row[1],
                    "sub_module_name": row[6],
                    "submissionDate": submission_date,
                    "location": row[4] or form_data.get("location"),
                    "narrative": row[5],
                    "description": (
                        form_data.get("Give a brief narrative of what happened") or
                        form_data.get("A brief narrative of what happened") or
                        form_data.get("A brief description of the person") or "N/A"
                    ),
                    "type_of_property": (
                        form_data.get("Type of property") or
                        form_data.get("select type of property broken into")
                    ),
                    "victim_name": (
                        form_data.get("Name of the casualty") or
                        form_data.get("Name of the victim") or
                        form_data.get("Name of the deceased") or
                        form_data.get("Name")
                    ),
                    "vehicle_make": form_data.get("Make"),
                    "vehicle_model": form_data.get("Model"),
                    "vehicle_registration": form_data.get("Registration number"),
                    "stolen_items": form_data.get("What category of items were stolen"),
                    "electronic_type": form_data.get("type of electronic"),
                    "document_type": form_data.get("type of Documents"),
                    "gbv_type": form_data.get("Type of GBV"),
                    "cause_of_death": form_data.get("Cause of death"),
                    "mental_condition": form_data.get("Mental Condition"),
                    "suspect_presence": form_data.get("Do you have a suspect"),
                    "suspect_name": form_data.get("Name of the suspect"),
                    "suspect_description": (
                        form_data.get("Description of the suspect") or
                        form_data.get("Give details about the suspect")
                    ),
                    "cyber_incident": form_data.get("Select Incident"),
                    "platform_digital_violence": form_data.get("Platform In Digital or Online Violence"),
                    "searchable_text": searchable_text,
                    "formData": form_data
                }
                for key, value in form_data.items():
                    doc[key] = value
                documents.append(doc)
            total_records += len(rows)
            progress = min(total_records / total_expected if total_expected > 0 else 1.0, 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Indexed {total_records} of approximately {total_expected} records...")
            logger.debug(f"Processed {total_records} records so far")
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

# Debug suspect names
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

# Debug indexed documents
def debug_indexed_documents(index_name="incidents"):
    try:
        index = meili_client.index(index_name)
        results = index.search("", {
            "limit": 10,
            "attributesToRetrieve": ["*"]
        })
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

# Settings at top right
col1, col2 = st.columns([3, 1])
with col2:
    st.markdown('<div class="settings-container">', unsafe_allow_html=True)
    setting_action = st.selectbox(
        "Settings:",
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
    st.markdown('</div>', unsafe_allow_html=True)

# Automatic index creation on startup
if not index_exists("incidents"):
    st.info("Incidents index not found. Creating and indexing data...")
    try:
        index_meilisearch_data()
    except Exception as e:
        st.error(f"Failed to create and index data: {str(e)}")
        logger.error(f"Failed to create and index data: {str(e)}")
        st.stop()

# Sidebar: Databases and Report/OB Menu
with st.sidebar:
    st.header("Filters")
    st.subheader("Databases")
    database_options = [
        "ALL",
        "WATCHLIST DB",
        "STOLEN/LOST ITEMS DB",
        "MISSING PERSONS DB",
        "EVIDENCE DB",
        "STOLEN VEHICLES DB",
        "PRISONER PROPERTY DB"
    ]
    selected_databases = []

    # Initialize session state for checkboxes - all unselected by default
    if 'database_selections' not in st.session_state:
        st.session_state.database_selections = {option: False for option in database_options}

    # Handle checkbox selections
    all_checked = st.checkbox("ALL", value=st.session_state.database_selections["ALL"], key="db_ALL")
    if all_checked != st.session_state.database_selections["ALL"]:
        for option in database_options:
            st.session_state.database_selections[option] = all_checked
    else:
        for option in database_options[1:]:
            checked = st.checkbox(option, value=st.session_state.database_selections[option], key=f"db_{option}")
            st.session_state.database_selections[option] = checked
        # If any non-ALL option is unchecked, uncheck ALL
        if not all(st.session_state.database_selections[opt] for opt in database_options[1:]):
            st.session_state.database_selections["ALL"] = False
        # If all non-ALL options are checked, check ALL
        elif all(st.session_state.database_selections[opt] for opt in database_options[1:]):
            st.session_state.database_selections["ALL"] = True

    # Collect selected databases
    selected_databases = [opt for opt in database_options if st.session_state.database_selections[opt]]

    st.subheader("Report/OB")
    sub_module_filter = st.multiselect(" ", get_sub_module_names())

# Search interface
col1, col2 = st.columns(2)
with col1:
    query = st.text_input("SEARCH QUERY:", placeholder="e.g., karanja, lost laptop, Johncoursedoe")
    # Place Start Date and End Date on the same row
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        default_start = datetime.now().date() - timedelta(days=30)
        start_date = st.date_input("START DATE:", default_start, key="start_date")
    with date_col2:
        default_end = datetime.now().date()
        end_date = st.date_input("END DATE:", default_end, key="end_date")
with col2:
    limit = st.slider("Number of results:", min_value=1, max_value=50, value=10, key="results_slider")

if st.button("Search", key="main_search_button"):
    if query:
        # Ensure at least one database is selected
        if not selected_databases:
            st.session_state.database_selections["ALL"] = True
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
            logger.debug(f"Search query: {query}")
            logger.debug(f"Search filters: {filter_str}")
            st.write(f"Search query: {query}")
            st.write(f"Search filters: {filter_str if filter_str else 'None'}")
            results = index.search(query, {
                "limit": limit,
                "filter": filter_str,
                "attributesToRetrieve": ["*"]
            })["hits"]
            st.info("Search performed using full-text search across all fields.")
            st.write(f"Found {len(results)} results")
            if not results:
                st.warning("No results found with current query/filters. Trying search without filters...")
                results = index.search(query, {
                    "limit": limit,
                    "filter": None,
                    "attributesToRetrieve": ["*"]
                })["hits"]
                st.write(f"Found {len(results)} results without filters")
                if not results:
                    st.warning("Still no results. Check 'Debug Indexed Documents' to verify index contents or try a different query.")
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
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            logger.error(f"Search error: {str(e)}")
    else:
        st.warning("Please enter a search query.")
