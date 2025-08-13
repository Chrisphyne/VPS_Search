from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import threading

from kenya_sugar_adaptive_multiagent import AdaptiveKenyaSugarAnalyzer

app = FastAPI(title="Kenya Sugar Board AI Backend", version="1.0.0")

# Allow local dev UIs to call this server directly if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance with a lock to avoid double init in multi-thread
_analyzer: Optional[AdaptiveKenyaSugarAnalyzer] = None
_analyzer_lock = threading.Lock()


def get_analyzer() -> AdaptiveKenyaSugarAnalyzer:
    global _analyzer
    if _analyzer is None:
        with _analyzer_lock:
            if _analyzer is None:
                data_dir = os.getenv("KSB_DATA_DIR", ".")
                _analyzer = AdaptiveKenyaSugarAnalyzer(data_directory=data_dir)
    return _analyzer


class AnalyzeRequest(BaseModel):
    query: str
    type: Optional[str] = "comprehensive"  # 'data' | 'research' | 'comprehensive'


class AnalyzeResult(BaseModel):
    success: bool
    response: str
    type: str
    status: str
    meta: Optional[Dict[str, Any]] = None


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/summary")
def summary() -> Dict[str, Any]:
    try:
        analyzer = get_analyzer()
        return {"success": True, "summary": analyzer.get_data_summary()}
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc))


def _extract_messages_content(messages: Any) -> str:
    try:
        collected: List[str] = []
        for msg in messages or []:
            content = getattr(msg, "content", None)
            role = getattr(msg, "role", None)
            if content and (role is None or role != "user"):
                collected.append(str(content))
        if not collected and messages:
            # Fallback: best effort str()
            return "\n\n".join(map(str, messages))
        return "\n\n".join(collected) if collected else "No content returned from analyzer."
    except Exception:
        return "No content returned from analyzer."


@app.post("/analyze", response_model=AnalyzeResult)
def analyze(req: AnalyzeRequest) -> AnalyzeResult:
    try:
        analyzer = get_analyzer()
        qtype = (req.type or "comprehensive").lower()

        if qtype == "data":
            content = analyzer.quick_data_analysis(req.query)
            return AnalyzeResult(success=True, response=content, type="data", status="ok")
        elif qtype == "research":
            content = analyzer.quick_research(req.query)
            return AnalyzeResult(success=True, response=content, type="research", status="ok")
        else:
            result = analyzer.analyze(req.query)
            # Prefer 'synthesis' if present
            if isinstance(result, dict):
                if "synthesis" in result and isinstance(result["synthesis"], str):
                    return AnalyzeResult(success=True, response=result["synthesis"], type="comprehensive", status=result.get("status", "ok"), meta={k: v for k, v in result.items() if k not in {"synthesis"}})
                # Else try messages
                messages = result.get("messages")
                if messages is not None:
                    content = _extract_messages_content(messages)
                    return AnalyzeResult(success=True, response=content, type="comprehensive", status=result.get("status", "ok"))
                # Else try data_analysis + research
                if "data_analysis" in result or "research" in result:
                    combined = ""
                    if result.get("data_analysis"):
                        combined += f"Data Analysis:\n{result['data_analysis']}\n\n"
                    if result.get("research"):
                        combined += f"Industry Research:\n{result['research']}\n\n"
                    return AnalyzeResult(success=True, response=combined.strip(), type="comprehensive", status=result.get("status", "ok"))
                # Fallback to string repr
                return AnalyzeResult(success=True, response=str(result), type="comprehensive", status="ok")
            else:
                return AnalyzeResult(success=True, response=str(result), type="comprehensive", status="ok")

    except Exception as exc:
        # Return a friendly error but keep 200 so frontend can fallback gracefully
        return AnalyzeResult(success=False, response=f"Backend error: {exc}", type=req.type or "comprehensive", status="error")