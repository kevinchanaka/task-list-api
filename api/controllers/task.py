from flask import Blueprint, jsonify, request
from api.services import task_service
from api.helpers import login_required
from api.models import task_create_schema, task_update_schema

bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")


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
def create(user_id):
    payload = request.get_json()
    task_obj = task_create_schema.load_validate(user_id=user_id, **payload)
    task = task_service.create_task(task_obj)
    return jsonify(task)


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(user_id, id):
    payload = request.get_json()
    task_obj = task_update_schema.load_validate(user_id=user_id, id=id, **payload)
    task = task_service.update_task(task_obj)
    return jsonify(task)


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    ret = task_service.delete_task(user_id, id)
    return jsonify(ret)
