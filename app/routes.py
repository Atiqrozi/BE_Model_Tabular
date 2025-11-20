from flask import Blueprint, request, jsonify
from .services import preprocess_and_predict

bp = Blueprint("api", __name__)


@bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        result = preprocess_and_predict(data)
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
