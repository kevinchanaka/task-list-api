from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, InternalServerError
from api.exceptions import InvalidUsageError
from api.controllers.health import bp as bp_health
from api.controllers.task import bp as bp_tasks
from api.controllers.user import bp as bp_users


def init_app(testing=False):
    app = Flask(__name__)

    if testing is True:
        app.config.update({"TESTING": True})

    # Registering blueprints
    app.register_blueprint(bp_health)
    app.register_blueprint(bp_tasks)
    app.register_blueprint(bp_users)

    # Generic HTTP error handler
    @app.errorhandler(HTTPException)
    def handle_general_exception(e: HTTPException):
        return jsonify({"message": e.name}), e.code

    @app.errorhandler(InvalidUsageError)
    def handle_api_usage_error(e: InvalidUsageError):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(InternalServerError)
    def handle_server_exception(e: InternalServerError):
        return jsonify({"message": "An unexpected error occured"}), e.code

    return app


app = init_app()
