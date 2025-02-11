from flask import Blueprint, jsonify
from api.services import label_service
from api.helpers import (
    login_required,
    parse_request_params,
    parse_request_body,
    get_page_info,
)
from api.schemas import LabelSchema, PageInfoSchema

bp = Blueprint("labels", __name__, url_prefix="/api/v1/labels")

label_create_schema = LabelSchema(exclude=("user_id", "created_at", "updated_at", "id"))
label_update_schema = LabelSchema(exclude=("user_id", "id", "created_at", "updated_at"))
label_get_schema = LabelSchema(exclude=("user_id",))

label_params_schema = PageInfoSchema()


@bp.route("", strict_slashes=False, methods=["GET"])
@login_required
@parse_request_params(label_params_schema)
def list(user_id, params):
    labels, label_count = label_service.list_labels(user_id, params)
    return jsonify(
        {
            "labels": [label_get_schema.dump(x) for x in labels],
            "pageInfo": get_page_info(params, label_count),
        }
    )


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    label = label_service.get_label(user_id, id)
    return jsonify({"label": label_get_schema.dump(label)})


@bp.route("", strict_slashes=False, methods=["POST"])
@login_required
@parse_request_body(label_create_schema)
def create(user_id, data):
    label_service.create_label(user_id, data)
    return jsonify({"label": label_get_schema.dump(data), "message": "Label added"})


@bp.route("/<id>", methods=["PUT"])
@login_required
@parse_request_body(label_update_schema)
def update(user_id, id, data):
    label = label_service.update_label(user_id, id, data)
    return jsonify({"label": label_get_schema.dump(label), "message": "Label modified"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    label_service.delete_label(user_id, id)
    return jsonify({"message": "Label deleted"})
