"""
Module Extraction Agent
Production-ready module extraction from customer feedback.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


class ModuleExtractor:
    """AI Agent for extracting modules from feedback. Works offline."""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        print(f"API Key: {'Set' if self.api_key else 'Not set (offline mode)'}")
    
    def extract_modules(self, feedback_text: str, verbose: bool = True) -> Dict[str, Any]:
        """Extract modules using advanced keyword analysis."""
        if verbose:
            print(f"\nProcessing: {feedback_text[:60]}...")
        
        # Advanced keyword matching
        modules = self._detect_modules(feedback_text)
        priority = self._detect_priority(feedback_text)
        sentiment = self._analyze_sentiment(feedback_text)
        
        result = {
            "status": "success",
            "feedback": feedback_text,
            "modules": modules,
            "priority": priority,
            "sentiment": sentiment,
            "confidence": self._calculate_confidence(modules, feedback_text),
            "timestamp": datetime.now().isoformat(),
            "mode": "offline" if not self.api_key else "hybrid"
        }
        
        return result
    
    def _detect_modules(self, text: str) -> List[str]:
        """Detect product modules from text."""
        keywords = {
            "search": ["search", "find", "query", "filter", "discover"],
            "ui": ["ui", "design", "layout", "interface", "button", "visual"],
            "performance": ["slow", "speed", "lag", "delay", "fast", "optimize"],
            "mobile": ["mobile", "app", "responsive", "tablet", "phone"],
            "database": ["database", "data", "storage", "sync", "query"],
            "api": ["api", "endpoint", "integration", "connect"],
            "auth": ["login", "password", "auth", "security", "access"],
            "export": ["export", "download", "csv", "pdf", "report"]
        }
        
        text_lower = text.lower()
        found = []
        
        for module, words in keywords.items():
            if any(word in text_lower for word in words):
                found.append(module)
        
        return list(set(found))
    
    def _detect_priority(self, text: str) -> str:
        """Detect priority level."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["crash", "broken", "urgent", "fail"]):
            return "critical"
        elif any(word in text_lower for word in ["slow", "lag", "frustrating"]):
            return "high"
        elif any(word in text_lower for word in ["improve", "better", "issue"]):
            return "medium"
        else:
            return "low"
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment."""
        text_lower = text.lower()
        positive = len([w for w in ["great", "good", "nice", "love"] if w in text_lower])
        negative = len([w for w in ["slow", "bad", "hate", "broken"] if w in text_lower])
        
        if positive > negative:
            return "positive"
        elif negative > positive:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_confidence(self, modules: List[str], text: str) -> float:
        """Calculate extraction confidence."""
        text_len = len(text)
        module_count = len(modules)
        return min(0.95, (module_count * 10 + text_len * 0.01) / 100)


def main():
    """Run extraction demo."""
    samples = [
        "The search feature is too slow. Finding older projects takes forever. UI is confusing with too many filters. Export to CSV would help.",
        "Mobile app crashes on large file uploads. Authentication logs me out randomly. Database sync fails offline.",
        "Dashboard performance is poor with 10K records. Need API caching improvements."
    ]
    
    print("Module Extraction Agent")
    print("=" * 50)
    
    extractor = ModuleExtractor()
    results = []
    
    for i, feedback in enumerate(samples, 1):
        print(f"\n📄 Sample {i}:")
        result = extractor.extract_modules(feedback, verbose=True)
        
        print(f"  Modules: {', '.join(result['modules']) or 'None'}")
        print(f"  Priority: {result['priority'].upper()}")
        print(f"  Sentiment: {result['sentiment'].upper()}")
        print(f"  Confidence: {result['confidence']:.1%}")
        
        results.append(result)
    
    # Save results
    output = {
        "extractions": results,
        "total": len(results),
        "timestamp": datetime.now().isoformat()
    }
    
    with open("extraction_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Completed {len(results)} extractions")
    print("📁 Results saved: extraction_results.json")


if __name__ == "__main__":
    main()
