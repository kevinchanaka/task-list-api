from flask import Blueprint, jsonify
from api.services import task_service
from api.helpers import (
    login_required,
    parse_request_body,
    parse_request_params,
    get_page_info,
)
from api.schemas import TaskSchema, TaskLabelSchema, TaskQuerySchema

bp = Blueprint("tasks", __name__, url_prefix="/api/v1/tasks")

task_create_schema = TaskSchema(
    exclude=("user_id", "completed", "created_at", "updated_at", "id")
)
task_update_schema = TaskSchema(exclude=("created_at", "updated_at", "user_id", "id"))
task_get_schema = TaskSchema(exclude=("user_id",))
task_list_schema = TaskSchema(exclude=("user_id", "created_at", "updated_at"))
task_label_schema = TaskLabelSchema()

task_query_schema = TaskQuerySchema()


@bp.route("", strict_slashes=False, methods=["GET"])
@login_required
@parse_request_params(task_query_schema)
def list(user_id, params):
    tasks, task_count = task_service.list_tasks(user_id, params)
    return jsonify(
        {
            "tasks": [task_get_schema.dump(x) for x in tasks],
            "pageInfo": get_page_info(params, task_count),
        }
    )


@bp.route("/<id>", methods=["GET"])
@login_required
def get(user_id, id):
    task = task_service.get_task(user_id, id)
    return jsonify({"task": task_get_schema.dump(task)})


@bp.route("", strict_slashes=False, methods=["POST"])
@login_required
@parse_request_body(task_create_schema)
def create(user_id, data):
    task_service.create_task(user_id, data)
    return jsonify({"task": task_get_schema.dump(data), "message": "Task added"})


@bp.route("/<id>", methods=["PUT"])
@login_required
@parse_request_body(task_update_schema)
def update(user_id, id, data):
    task = task_service.update_task(user_id, id, data)
    return jsonify({"task": task_get_schema.dump(task), "message": "Task modified"})


@bp.route("/<id>", methods=["DELETE"])
@login_required
def delete(user_id, id):
    task_service.delete_task(user_id, id)
    return jsonify({"message": "Task deleted"})


@bp.route("/attach", methods=["POST"])
@login_required
@parse_request_body(task_label_schema)
def attach(user_id, data):
    task_service.attach_labels_to_task(user_id, data)
    return jsonify({"message": "Attached labels to task"})


@bp.route("/detach", methods=["POST"])
@login_required
@parse_request_body(task_label_schema)
def detach(user_id, data):
    task_service.detach_labels_from_task(user_id, data)
    return jsonify({"message": "Detached labels from task"})
