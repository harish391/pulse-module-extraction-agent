"""
FastAPI server for module extraction.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime
import uvicorn

from module_extraction_agent import ModuleExtractor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Module Extraction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

extractor = ModuleExtractor()


class FeedbackRequest(BaseModel):
    text: str
    verbose: bool = False


class FeedbackResponse(BaseModel):
    status: str
    feedback: str
    modules: List[str]
    priority: str
    sentiment: str
    confidence: float
    timestamp: str


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/extract", response_model=FeedbackResponse)
async def extract(request: FeedbackRequest):
    """Extract modules from feedback."""
    try:
        text = request.text.strip()
        if len(text) < 10:
            raise HTTPException(status_code=400, detail="Text too short")
        
        result = extractor.extract_modules(text, verbose=False)
        
        return FeedbackResponse(
            status=result["status"],
            feedback=result["feedback"],
            modules=result["modules"],
            priority=result["priority"],
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            timestamp=result["timestamp"]
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")


@app.get("/examples")
async def examples():
    return {
        "examples": [
            "Search is too slow. UI needs improvement.",
            "Mobile app crashes. Database sync broken.",
            "Performance poor with large datasets."
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
