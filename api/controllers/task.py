from flask import Blueprint, jsonify, request
from api.services import task_service
from api.decorators import validator, login_required
from api.config import NAME_LENGTH, DEFAULT_LENGTH

bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")

task_schema = {
    "name": {"type": "string", "required": True, "maxlength": NAME_LENGTH},
    "description": {"type": "string", "required": True, "maxlength": DEFAULT_LENGTH},
}


@bp.route("/", methods=["GET"])
@login_required
def list(user_id):
    return jsonify(task_service.list_tasks(user_id))


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    task = task_service.get_task(user_id, id)
    return jsonify(task)


@bp.route("/", methods=["POST"])
@login_required
@validator(task_schema)
def create(user_id):
    data = request.get_json()
    task = task_service.create_task(user_id, data)
    return jsonify(task)


@bp.route("/<id>", methods=["PUT"])
@login_required
@validator(task_schema)
def update(user_id, id):
    data = request.get_json()
    task = task_service.update_task(user_id, id, data)
    return jsonify(task)


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    ret = task_service.delete_task(user_id, id)
    return jsonify(ret)
