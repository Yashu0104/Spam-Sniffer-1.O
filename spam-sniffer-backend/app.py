
from flask import Flask, request, jsonify

'''from flask import Flask, request, jsonify
from flask_cors import CORS

import pickle
import numpy as np

# Load model and vectorizer
with open("spam_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

app = Flask(__name__)

@app.route("/check_spam", methods=["POST"])
def check_spam():
    data = request.get_json()
    text = data.get("text", "")

    # Vectorize the email content
    vectorized_text = vectorizer.transform([text])

    # Predict using the loaded model
    prediction = model.predict(vectorized_text)[0]
    proba = model.predict_proba(vectorized_text)[0][1]

    # Simple spam type description logic (can be improved)
    if "lottery" in text.lower():
        description = "Lottery scam"
    elif "free" in text.lower():
        description = "Free offer spam"
    elif "urgent" in text.lower():
        description = "Urgent phishing email"
    else:
        description = "General spam"

    return jsonify({
        "is_spam": bool(prediction),
        "spam_score": round(float(proba), 3),
        "description": description
    })

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(host="0.0.0.0", port=5000, debug=True)'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Load model and vectorizer
with open("spam_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

app = Flask(__name__)

# Enable CORS
CORS(app)

@app.before_request
def log_request_info():
    """ Log the accessed path before each request. """
    print(f"Accessed Path: {request.path}")

def generate_summary(text, sentence_count=2):
    """ Generate a short summary using TextRank algorithm """
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summarized_text = " ".join(str(sentence) for sentence in summary)
    return summarized_text

@app.route("/check_spam", methods=["POST"])
def check_spam():
    data = request.get_json()
    text = data.get("text", "")

    # Vectorize the email content
    vectorized_text = vectorizer.transform([text])

    # Predict using the loaded model
    prediction = model.predict(vectorized_text)[0]
    proba = model.predict_proba(vectorized_text)[0][1]

    # Generate a summary of the email
    summary = generate_summary(text)

    description = "Likely spam" if prediction else "Likely safe"

    return jsonify({
        "is_spam": bool(prediction),
        "spam_score": round(float(proba), 3),
        "description": description,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> 85895f0 (Fixed conflict)
