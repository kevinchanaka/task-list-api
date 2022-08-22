from flask import Blueprint, jsonify, request
from api.services import task_service
from api.helpers import login_required
from api.schemas import task_create_schema, task_update_schema

bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")


@bp.route("", strict_slashes=False, methods=["GET"])
@login_required
def list(user_id):
    return jsonify({"tasks": task_service.list_tasks(user_id)})


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    task = task_service.get_task(user_id, id)
    return jsonify({"task": task})


@bp.route("", strict_slashes=False, methods=["POST"])
@login_required
def create(user_id):
    payload = request.get_json()
    task_obj = task_create_schema.load_validate(user_id=user_id, **payload)
    task = task_service.create_task(task_obj)
    return jsonify({"task": task, "message": "Task added"})


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(user_id, id):
    payload = request.get_json()
    task_obj = task_update_schema.load_validate(user_id=user_id, id=id, **payload)
    task = task_service.update_task(task_obj)
    return jsonify({"task": task, "message": "Task modified"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    task_service.delete_task(user_id, id)
    return jsonify({"message": "Task deleted"})


@bp.route("/<id>/attach", methods=["POST"])
@login_required
def attach(user_id, id):
    payload = request.get_json()
    task_service.attach_label_to_task(user_id, payload["label_id"], id)
    return jsonify({"message": "Attached label to task"})


@bp.route("/<id>/detach", methods=["POST"])
@login_required
def detach(user_id, id):
    payload = request.get_json()
    task_service.detach_label_from_task(user_id, payload["label_id"], id)
    return jsonify({"message": "Detached label from task"})
