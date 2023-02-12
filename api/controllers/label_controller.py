from flask import Blueprint, jsonify, request
from api.services import label_service
from api.helpers import login_required, generate_page_info
from api.schemas import LabelSchema, QueryParamsSchema

bp = Blueprint("labels", __name__, url_prefix="/api/v1/labels")

label_create_schema = LabelSchema(exclude=("created_at", "updated_at", "id"))
label_update_schema = LabelSchema(exclude=("created_at", "updated_at"))
label_get_schema = LabelSchema(exclude=("user_id",))

label_params_schema = QueryParamsSchema()


@bp.route("", strict_slashes=False, methods=["GET"])
@login_required
def list(user_id):
    params = label_params_schema.load_validate(**request.args)
    labels, label_count = label_service.list_labels(user_id, params)
    page_info = generate_page_info(params, label_count)
    return jsonify({"labels": [label_get_schema.dump(x) for x in labels], **page_info})


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    label = label_service.get_label(user_id, id)
    return jsonify({"label": label_get_schema.dump(label)})


@bp.route("", strict_slashes=False, methods=["POST"])
@login_required
def create(user_id):
    payload = request.get_json()
    label = label_create_schema.load_validate(userId=user_id, **payload)
    label_service.create_label(label)
    return jsonify({"label": label_get_schema.dump(label), "message": "Label added"})


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(user_id, id):
    payload = request.get_json()
    label_update_schema.load_validate(userId=user_id, id=id, **payload)
    label = label_service.update_label(user_id, id, payload)
    return jsonify({"label": label_get_schema.dump(label), "message": "Label modified"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    label_service.delete_label(user_id, id)
    return jsonify({"message": "Label deleted"})
