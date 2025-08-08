# Cell 1: Setup and Imports
"""
Enhanced RAG System for JSONB Occurrence Data
=============================================

This system demonstrates how to make your JSONB occurrence data intelligently 
available to your LLM with field schema understanding.

Key Features:
- Dynamic field schema loading from sub_module table
- Smart JSONB querying with field-aware SQL generation  
- Vector search on occurrence content for semantic similarity
- Field-aware LLM responses that understand your data structure
"""

import os
import json
import pandas as pd
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# LangChain and AI imports
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

print("✅ All libraries imported successfully!")