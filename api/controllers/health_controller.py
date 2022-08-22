from flask import Blueprint, jsonify

bp = Blueprint("health", __name__, url_prefix="/api/v1/health")


@bp.route("", strict_slashes=False)
def health():
    return jsonify({"message": "API is running!"})
