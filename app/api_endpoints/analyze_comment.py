from flask import Blueprint, request, jsonify

from app.configs.model_config import model, vectorizer
from app.utils.clean_text import clean_text

analyzeComment = Blueprint('analyze-comment', __name__)


@analyzeComment.route('/analyze-comment', methods=['POST'])
def analyze_comment():
    try:
        data = request.get_json(force=True)
        comment = data.get('comment')
        learning = data.get('learning', False)

        if comment is None:
            return jsonify({"error": "Missing 'comment' parameter."}), 400

        cleaned_comment = clean_text(comment)
        comment_vector = vectorizer.transform([cleaned_comment])

        prediction = model.predict(comment_vector)
        proba = model.predict_proba(comment_vector)

        if learning:
            model.partial_fit(comment_vector, [prediction[0]])

        return jsonify({
            'prediction': int(prediction[0]),
            'probability': proba.tolist()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
