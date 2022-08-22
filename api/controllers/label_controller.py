from flask import Blueprint, jsonify, request
from api.services import label_service
from api.helpers import login_required
from api.schemas import label_create_schema, label_update_schema

bp = Blueprint("labels", __name__, url_prefix="/api/v1/labels")


@bp.route("", strict_slashes=False, methods=["GET"])
@login_required
def list(user_id):
    return jsonify({"labels": label_service.list_labels(user_id)})


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    label = label_service.get_label(user_id, id)
    return jsonify({"label": label})


@bp.route("", strict_slashes=False, methods=["POST"])
@login_required
def create(user_id):
    payload = request.get_json()
    label_obj = label_create_schema.load_validate(user_id=user_id, **payload)
    label = label_service.create_label(label_obj)
    return jsonify({"label": label, "message": "Label added"})


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(user_id, id):
    payload = request.get_json()
    label_obj = label_update_schema.load_validate(user_id=user_id, id=id, **payload)
    label = label_service.update_label(label_obj)
    return jsonify({"label": label, "message": "Label modified"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    label_service.delete_label(user_id, id)
    return jsonify({"message": "Label deleted"})
