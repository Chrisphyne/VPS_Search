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


def _build_fallback_message(query: str, analyzer: AdaptiveKenyaSugarAnalyzer) -> str:
    try:
        summary = analyzer.get_data_summary()
    except Exception:
        summary = "Kenya Sugar Board data available."
    return (
        f"I could not generate a detailed response for: '{query}'.\n\n"
        f"Here is an overview of the datasets and sample queries you can try next:\n\n{summary}"
    )


@app.post("/analyze", response_model=AnalyzeResult)
def analyze(req: AnalyzeRequest) -> AnalyzeResult:
    try:
        analyzer = get_analyzer()
        qtype = (req.type or "comprehensive").lower()

        if qtype == "data":
            content = analyzer.quick_data_analysis(req.query)
            if not content or not str(content).strip() or str(content).lower().startswith("error"):
                # Fallback to comprehensive analysis
                result = analyzer.analyze(req.query)
                if isinstance(result, dict):
                    # Prefer synthesis
                    if isinstance(result.get("synthesis"), str) and result["synthesis"].strip():
                        return AnalyzeResult(success=True, response=result["synthesis"], type="comprehensive", status=result.get("status", "ok"))
                    # Try messages
                    messages = result.get("messages")
                    if messages is not None:
                        msg_content = _extract_messages_content(messages)
                        if msg_content and msg_content.strip():
                            return AnalyzeResult(success=True, response=msg_content, type="comprehensive", status=result.get("status", "ok"))
                # Final fallback
                return AnalyzeResult(success=True, response=_build_fallback_message(req.query, analyzer), type="data", status="fallback")
            return AnalyzeResult(success=True, response=str(content), type="data", status="ok")
        elif qtype == "research":
            content = analyzer.quick_research(req.query)
            if not content or not str(content).strip() or str(content).lower().startswith("error"):
                # Fallback to comprehensive analysis
                result = analyzer.analyze(req.query)
                if isinstance(result, dict):
                    if isinstance(result.get("synthesis"), str) and result["synthesis"].strip():
                        return AnalyzeResult(success=True, response=result["synthesis"], type="comprehensive", status=result.get("status", "ok"))
                    messages = result.get("messages")
                    if messages is not None:
                        msg_content = _extract_messages_content(messages)
                        if msg_content and msg_content.strip():
                            return AnalyzeResult(success=True, response=msg_content, type="comprehensive", status=result.get("status", "ok"))
                return AnalyzeResult(success=True, response=_build_fallback_message(req.query, analyzer), type="research", status="fallback")
            return AnalyzeResult(success=True, response=str(content), type="research", status="ok")
        else:
            result = analyzer.analyze(req.query)
            # Prefer 'synthesis' if present
            if isinstance(result, dict):
                if "synthesis" in result and isinstance(result["synthesis"], str) and result["synthesis"].strip():
                    return AnalyzeResult(success=True, response=result["synthesis"], type="comprehensive", status=result.get("status", "ok"), meta={k: v for k, v in result.items() if k not in {"synthesis"}})
                # Else try messages
                messages = result.get("messages")
                if messages is not None:
                    content = _extract_messages_content(messages)
                    if content and content.strip():
                        return AnalyzeResult(success=True, response=content, type="comprehensive", status=result.get("status", "ok"))
                # Else try data_analysis + research
                if "data_analysis" in result or "research" in result:
                    combined = ""
                    if result.get("data_analysis"):
                        combined += f"Data Analysis:\n{result['data_analysis']}\n\n"
                    if result.get("research"):
                        combined += f"Industry Research:\n{result['research']}\n\n"
                    if combined.strip():
                        return AnalyzeResult(success=True, response=combined.strip(), type="comprehensive", status=result.get("status", "ok"))
                # Fallback to summary
                return AnalyzeResult(success=True, response=_build_fallback_message(req.query, analyzer), type="comprehensive", status="fallback")
            else:
                text = str(result or "").strip()
                if not text:
                    return AnalyzeResult(success=True, response=_build_fallback_message(req.query, analyzer), type="comprehensive", status="fallback")
                return AnalyzeResult(success=True, response=text, type="comprehensive", status="ok")

    except Exception as exc:
        # Return a friendly error but keep 200 so frontend can fallback gracefully
        return AnalyzeResult(success=False, response=f"Backend error: {exc}", type=req.type or "comprehensive", status="error")