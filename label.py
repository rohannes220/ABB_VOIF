import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

df = pd.read_csv('voc_fashion_final.csv')

# --- Sentiment (only fill in blanks) ---
def get_sentiment(text):
    if pd.isna(text) or not str(text).strip():
        return ""
    score = analyzer.polarity_scores(str(text))['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

needs_sentiment = df['sentiment'].isna() | (df['sentiment'] == "")
df.loc[needs_sentiment, 'sentiment'] = df.loc[needs_sentiment, 'text'].apply(get_sentiment)

# --- Intent (expanded keyword-based, only fill blanks) ---
INTENT_KEYWORDS = {
    "Complaint": [
        "disappointed", "worst", "bad quality", "refund", "return", "damaged", "poor",
        "waste of money", "never buying", "never again", "rude", "delay", "delayed",
        "issue", "problem", "faulty", "defective", "torn", "ripped", "faded", "shrunk",
        "misleading", "fake", "duplicate", "cheap material", "not worth", "regret",
        "horrible", "terrible", "unacceptable", "pathetic", "cheated", "scam",
        "poor quality", "not happy", "disgusted", "annoyed", "frustrated", "complain",
    ],
    "Recommendation": [
        "recommend", "must buy", "love it", "loved it", "great product", "will buy again",
        "worth it", "amazing", "best purchase", "highly recommend", "value for money",
        "good quality", "excellent", "fantastic", "perfect fit", "happy with", "satisfied",
        "impressed", "superb", "awesome", "nice product", "good experience", "worth every",
        "five stars", "5 stars", "go for it",
    ],
    "Comparison": [
        "better than", "compared to", " vs ", "versus", "instead of", "unlike",
        "similar to", "same as", "rather than", "prefer", "more than other",
    ],
    "Purchase Intent": [
        "planning to buy", "want to buy", "thinking of buying", "going to purchase",
        "will order", "adding to cart", "will definitely buy", "thinking to order",
        "considering buying", "about to buy",
    ],
    "Query": [
        "does it", "is this", "can someone", "how do i", "what size", "anyone know",
        "can anyone", "please tell", "any idea", "which size", "how to", "where can i",
        "does anyone", "?",
    ],
}

def get_intent(text):
    if pd.isna(text) or not str(text).strip():
        return ""
    text_lower = str(text).lower()
    matches = {intent: sum(1 for kw in kws if kw in text_lower)
               for intent, kws in INTENT_KEYWORDS.items()}
    best_intent = max(matches, key=matches.get)
    if matches[best_intent] > 0:
        return best_intent
    return "General Feedback"

needs_intent = df['intent'].isna() | (df['intent'] == "")
df.loc[needs_intent, 'intent'] = df.loc[needs_intent, 'text'].apply(get_intent)

# --- Type / driver (re-classify ALL rows by keyword, ignore the scraper's
# hardcoded "Store Experience" default so real content wins) ---
TYPE_KEYWORDS = {
    "Product Quality": [
        "quality", "fabric", "material", "stitching", "durable", "torn", "faded",
        "cotton", "texture", "print", "color fade", "wear and tear", "long lasting",
        "sturdy", "flimsy", "premium feel", "cheap feel",
    ],
    "Fit & Sizing": [
        "size", "fit", "fitting", "tight", "loose", "small", "large", "xl", "medium",
        "true to size", "size chart", "runs small", "runs large", "true fit",
        "slim fit", "regular fit", "oversized",
    ],
    "Pricing": [
        "price", "expensive", "cheap", "value for money", "overpriced", "discount",
        "affordable", "costly", "worth the price", "price tag", "on sale", "offer",
    ],
    "Delivery & Returns": [
        "delivery", "shipping", "return", "refund", "exchange", "late", "courier",
        "delayed delivery", "on time", "packaging", "package", "tracking", "shipped",
    ],
    "Customer Service": [
        "service", "support", "helpful", "rude", "customer care", "response",
        "assist", "helpline", "call center", "representative", "resolved",
    ],
    "Store Experience": [
        "staff", "ambience", "outlet", "mall", "salesperson",
        "trial room", "billing", "queue", "in-store", "showroom", "store layout",
        "store visit", "walked in", "displayed",
    ],
}

def get_type(text, platform):
    if pd.isna(text) or not str(text).strip():
        return ""
    text_lower = str(text).lower()
    matches = {t: sum(1 for kw in kws if kw in text_lower)
               for t, kws in TYPE_KEYWORDS.items()}
    best_type = max(matches, key=matches.get)
    if matches[best_type] > 0:
        return best_type
    return "Store Experience" if platform == "Google" else "General Feedback"

# Re-classify every row (not just blanks) so the scraper's hardcoded
# "Store Experience" default gets replaced with real keyword-based labels.
df['type'] = df.apply(lambda row: get_type(row['text'], row['platform']), axis=1)

df.to_csv('voc_fashion_labeled.csv', index=False)
print(f"Labeled {len(df)} total rows")
print()
print("Sentiment breakdown:")
print(df['sentiment'].value_counts())
print()
print("Intent breakdown:")
print(df['intent'].value_counts())
print()
print("Type breakdown:")
print(df['type'].value_counts())