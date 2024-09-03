from textblob import TextBlob


class SentimentAnalyzer:
    def analyze_sentiment(self, review_body):
        """
        Analizza il sentiment di una recensione.

        Args:
        - review_body (str): Il corpo della recensione.

        Returns:
        - sentiment (str): Il sentiment della recensione (positive, negative, neutral).
        """
        blob = TextBlob(review_body)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            return "positive"
        elif polarity < 0:
            return "negative"
        else:
            return "neutral"
