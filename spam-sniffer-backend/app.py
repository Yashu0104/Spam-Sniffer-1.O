from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Load spam classification model and TF-IDF vectorizer
with open("spam_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.before_request
def log_request_info():
    """Log each request path for debugging."""
    print(f"Accessed Path: {request.path}")

def generate_summary(text, sentence_count=2):
    """Generate summary using TextRank algorithm."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

@app.route("/check_spam", methods=["POST"])
def check_spam():
    data = request.get_json()
    text = data.get("text", "")

    # Vectorize and predict
    vectorized_text = vectorizer.transform([text])
    prediction = model.predict(vectorized_text)[0]
    proba = model.predict_proba(vectorized_text)[0][1]

    # Generate summary
    summary = generate_summary(text)

    # Rule-based override
    description = "Likely spam" if prediction else "Likely safe"
    text_lower = text.lower()
    if "lottery" in text_lower:
        description = "Lottery scam"
        prediction = 1
    elif "free" in text_lower:
        description = "Free offer spam"
        prediction = 1
    elif "urgent" in text_lower:
        description = "Urgent phishing email"
        prediction = 1

    return jsonify({
        "is_spam": bool(prediction),
        "spam_score": round(float(proba), 3),
        "description": description,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
