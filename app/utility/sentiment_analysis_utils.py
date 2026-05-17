"""
AI-based sentiment analysis utility using TextBlob
Provides functions to analyze sentiment of text, news articles, 
and summarize multiple texts (e.g. comments, article paragraphs).
"""

from textblob import TextBlob
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """AI-based sentiment analysis service"""

    def __init__(self):
        try:
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {e}")

    # ---------------------------------------------------------
    # 1. Analyze a single text
    # ---------------------------------------------------------
    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return self._empty_result()

        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            #Balanced threshold for news article sentiment detection
            if polarity > 0.05:
                sentiment = "positive"
            elif polarity < -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            confidence = min(abs(polarity) * 2, 1.0)

            return {
                "text": text,
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "sentiment": sentiment,
                "confidence": round(confidence, 3)
            }

        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return self._empty_result(error=str(e))

    # ---------------------------------------------------------
    # 2. Analyze a news article (title + content)
    # ---------------------------------------------------------
    def analyze_news_article(self, title: str, content: str = "") -> Dict[str, Any]:
        combined = f"{title} {content}".strip()

        return {
            "overall": self.analyze_text(combined),
            "title": self.analyze_text(title),
            "content": self.analyze_text(content) if content else None
        }

    # ---------------------------------------------------------
    # 3. Summary for multiple texts (comments, paragraphs, etc.)
    # ---------------------------------------------------------
    def get_sentiment_summary(self, texts: List[str]) -> Dict[str, Any]:
        if not texts:
            return self._empty_summary()

        results = [self.analyze_text(t) for t in texts]

        positive = sum(1 for r in results if r["sentiment"] == "positive")
        negative = sum(1 for r in results if r["sentiment"] == "negative")
        neutral  = sum(1 for r in results if r["sentiment"] == "neutral")
        total    = len(texts)

        return {
            "total": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_pct": round(positive / total * 100, 1),
            "negative_pct": round(negative / total * 100, 1),
            "neutral_pct":  round(neutral  / total * 100, 1),
            "chart_labels": ["Positive", "Negative", "Neutral"],
            "chart_values": [positive, negative, neutral],
            "details": results
        }

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _empty_result(self, error: str = None):
        return {
            "polarity": 0.0,
            "subjectivity": 0.0,
            "sentiment": "neutral",
            "confidence": 0.0,
            "error": error
        }

    def _empty_summary(self):
        return {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "positive_pct": 0,
            "negative_pct": 0,
            "neutral_pct": 0,
            "chart_labels": ["Positive", "Negative", "Neutral"],
            "chart_values": [0, 0, 0],
            "details": []
        }


# Global instance
sentiment_analyzer = SentimentAnalyzer()

def analyze_sentiment(text: str):
    return sentiment_analyzer.analyze_text(text)

def analyze_news_sentiment(title: str, content: str = ""):
    return sentiment_analyzer.analyze_news_article(title, content)

def get_sentiment_summary(texts: List[str]):
    return sentiment_analyzer.get_sentiment_summary(texts)