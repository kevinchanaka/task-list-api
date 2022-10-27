from flask import Blueprint, jsonify, request
from api.services import task_service
from api.helpers import login_required
from api.schemas import TaskSchema

bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")

task_create_schema = TaskSchema(exclude=("completed", "created_at", "updated_at", "id"))
task_update_schema = TaskSchema(exclude=("created_at", "updated_at"))
task_get_schema = TaskSchema(exclude=("user_id",))
task_list_schema = TaskSchema(exclude=("user_id", "created_at", "updated_at"))


@bp.route("", strict_slashes=False, methods=["GET"])
@login_required
def list(user_id):
    tasks = task_service.list_tasks(user_id)
    return jsonify({"tasks": [task_get_schema.dump(x) for x in tasks]})


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    task = task_service.get_task(user_id, id)
    return jsonify({"task": task_get_schema.dump(task)})


@bp.route("", strict_slashes=False, methods=["POST"])
@login_required
def create(user_id):
    payload = request.get_json()
    task = task_create_schema.load_validate(userId=user_id, **payload)
    task_service.create_task(task)
    return jsonify({"task": task_get_schema.dump(task), "message": "Task added"})


@bp.route("/<id>", methods=["PUT"])
@login_required
def update(user_id, id):
    payload = request.get_json()
    task_obj = task_update_schema.load_validate(userId=user_id, id=id, **payload)
    task = task_service.update_task(task_obj.user_id, task_obj.id, payload)
    return jsonify({"task": task_get_schema.dump(task), "message": "Task modified"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    task_service.delete_task(user_id, id)
    return jsonify({"message": "Task deleted"})


@bp.route("/<id>/attach", methods=["POST"])
@login_required
def attach(user_id, id):
    payload = request.get_json()
    task_service.attach_label_to_task(user_id, payload["labelId"], id)
    return jsonify({"message": "Attached label to task"})


@bp.route("/<id>/detach", methods=["POST"])
@login_required
def detach(user_id, id):
    payload = request.get_json()
    task_service.detach_label_from_task(user_id, payload["labelId"], id)
    return jsonify({"message": "Detached label from task"})
