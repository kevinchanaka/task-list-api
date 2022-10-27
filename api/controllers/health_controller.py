from flask import Blueprint, jsonify

bp = Blueprint("health", __name__, url_prefix="/api/v1/health")


@bp.route("", strict_slashes=False)
def health():  # TODO: Consider improving this route e.g. check DB connection
    return jsonify({"message": "API is running!"})
