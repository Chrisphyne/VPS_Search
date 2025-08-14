from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import threading
import json
from datetime import datetime

from kenya_sugar_enhanced_system import EnhancedKenyaSugarAnalyzer, create_enhanced_analyzer

app = FastAPI(
    title="Enhanced Kenya Sugar Board AI Backend", 
    version="2.0.0",
    description="Advanced AI analysis system with conversation memory and multi-LLM support"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance with thread safety
_analyzer: Optional[EnhancedKenyaSugarAnalyzer] = None
_analyzer_lock = threading.Lock()

def get_analyzer() -> EnhancedKenyaSugarAnalyzer:
    """Get or create the enhanced analyzer instance"""
    global _analyzer
    if _analyzer is None:
        with _analyzer_lock:
            if _analyzer is None:
                data_dir = os.getenv("KSB_DATA_DIR", ".")
                _analyzer = create_enhanced_analyzer(data_dir)
    return _analyzer

# Request/Response models
class AnalyzeRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = "default"
    type: Optional[str] = "comprehensive"  # 'data' | 'research' | 'comprehensive'

class AnalyzeResult(BaseModel):
    success: bool
    response: str
    type: str
    status: str
    provider: Optional[str] = None
    conversation_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class ConversationHistoryResult(BaseModel):
    success: bool
    conversation_id: str
    messages: List[Dict[str, Any]]
    count: int

class HealthResult(BaseModel):
    status: str
    version: str
    llm_provider: Optional[str] = None
    features: List[str]
    data_summary: Optional[str] = None

# API Endpoints
@app.get("/health", response_model=HealthResult)
def health() -> HealthResult:
    """Health check with system information"""
    try:
        analyzer = get_analyzer()
        return HealthResult(
            status="healthy",
            version="2.0.0",
            llm_provider=analyzer.llm_provider,
            features=[
                "Conversation Memory",
                "Multi-LLM Support", 
                "Robust Error Handling",
                "Advanced Data Analysis",
                "Kenya Sugar Industry Focus"
            ],
            data_summary=analyzer.get_data_summary()
        )
    except Exception as e:
        return HealthResult(
            status="error",
            version="2.0.0",
            llm_provider=None,
            features=[],
            data_summary=f"Error: {e}"
        )

@app.post("/analyze", response_model=AnalyzeResult)
def analyze(req: AnalyzeRequest) -> AnalyzeResult:
    """Enhanced analysis endpoint with conversation memory"""
    try:
        analyzer = get_analyzer()
        
        # Use the enhanced analyzer
        result = analyzer.analyze(req.query, req.conversation_id or "default")
        
        # Check if we got a valid response
        response_text = result.get("response", "")
        if not response_text or not response_text.strip():
            # Use web research response
            web_response = analyzer.get_web_research_response(req.query, "general")
            return AnalyzeResult(
                success=True,
                response=web_response,
                type=req.type or "comprehensive",
                status="web_research_used",
                provider="tavily_web_research",
                conversation_id=req.conversation_id,
                meta={
                    "query": req.query,
                    "timestamp": datetime.now().isoformat(),
                    "note": "LLM returned empty response, used web research via Tavily"
                }
            )
        
        return AnalyzeResult(
            success=True,
            response=response_text,
            type=req.type or "comprehensive",
            status=result["status"],
            provider=result.get("provider"),
            conversation_id=result.get("conversation_id"),
            meta={
                "query": result["query"],
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as exc:
        # Return friendly error with fallback
        error_msg = f"Analysis error: {exc}"
        
        # Try to provide fallback response
        try:
            analyzer = get_analyzer()
            fallback = analyzer.generate_fallback_response(req.query, "general")
            return AnalyzeResult(
                success=False,
                response=f"{error_msg}\n\n**Fallback Analysis:**\n{fallback}",
                type=req.type or "comprehensive",
                status="error_with_fallback",
                conversation_id=req.conversation_id
            )
        except:
            return AnalyzeResult(
                success=False,
                response=error_msg,
                type=req.type or "comprehensive", 
                status="error",
                conversation_id=req.conversation_id
            )

@app.get("/conversations/{conversation_id}/history", response_model=ConversationHistoryResult)
def get_conversation_history(conversation_id: str) -> ConversationHistoryResult:
    """Get conversation history for a specific conversation ID"""
    try:
        analyzer = get_analyzer()
        messages = analyzer.get_conversation_history(conversation_id)
        
        return ConversationHistoryResult(
            success=True,
            conversation_id=conversation_id,
            messages=messages,
            count=len(messages)
        )
        
    except Exception as e:
        return ConversationHistoryResult(
            success=False,
            conversation_id=conversation_id,
            messages=[],
            count=0
        )

@app.post("/conversations/{conversation_id}/clear")
def clear_conversation(conversation_id: str) -> Dict[str, Any]:
    """Clear conversation history for a specific conversation ID"""
    try:
        analyzer = get_analyzer()
        
        # Clear the conversation state from checkpointer
        config = {"configurable": {"thread_id": conversation_id}}
        
        # Note: MemorySaver doesn't have a direct clear method, 
        # but we can create a new state
        analyzer.app.invoke(
            {"messages": []},
            config=config
        )
        
        return {
            "success": True,
            "message": f"Conversation {conversation_id} cleared",
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error clearing conversation: {e}",
            "conversation_id": conversation_id
        }

@app.get("/data/summary")
def get_data_summary() -> Dict[str, Any]:
    """Get summary of available datasets"""
    try:
        analyzer = get_analyzer()
        summary = analyzer.get_data_summary()
        
        # Also provide structured data info
        datasets_info = {}
        for filename, df in analyzer.datasets.items():
            datasets_info[filename] = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "sample": df.head(2).to_dict('records') if len(df) > 0 else []
            }
        
        return {
            "success": True,
            "summary": summary,
            "datasets": datasets_info,
            "count": len(analyzer.datasets)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "summary": "",
            "datasets": {},
            "count": 0
        }

@app.get("/llm/status")
def get_llm_status() -> Dict[str, Any]:
    """Get LLM provider status and configuration"""
    try:
        analyzer = get_analyzer()
        
        # Check available API keys
        api_keys_status = {
            "google": "✅ Available" if os.getenv("GOOGLE_API_KEY") else "❌ Not set",
            "openai": "✅ Available" if os.getenv("OPENAI_API_KEY") else "❌ Not set", 
            "anthropic": "✅ Available" if os.getenv("ANTHROPIC_API_KEY") else "❌ Not set",
            "ollama": "🔍 Check local installation"
        }
        
        return {
            "success": True,
            "current_provider": analyzer.llm_provider,
            "available_providers": api_keys_status,
            "model_info": {
                "provider": analyzer.llm_provider,
                "model": getattr(analyzer.llm, 'model_name', 'Unknown'),
                "temperature": getattr(analyzer.llm, 'temperature', 0)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "current_provider": None,
            "available_providers": {},
            "model_info": {}
        }

# Quick test endpoints
@app.get("/test/quick")
def quick_test() -> Dict[str, Any]:
    """Quick system test"""
    try:
        analyzer = get_analyzer()
        
        # Simple test query
        test_query = "What data is available for analysis?"
        result = analyzer.analyze(test_query, "test_conversation")
        
        return {
            "success": True,
            "test_query": test_query,
            "response_preview": result["response"][:200] + "..." if len(result["response"]) > 200 else result["response"],
            "status": result["status"],
            "provider": result.get("provider")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "test_query": "What data is available for analysis?",
            "response_preview": "",
            "status": "error",
            "provider": None
        }

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Enhanced Kenya Sugar Board API Server...")
    print("📊 Features: Conversation Memory | Multi-LLM Support | Robust Error Handling")
    print("🌐 Access the API at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )