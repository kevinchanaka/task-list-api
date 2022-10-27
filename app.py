import logging
import logging.config
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, InternalServerError
from api.exceptions import InvalidUsageError
from api.controllers.health_controller import bp as bp_health
from api.controllers.user_controller import bp as bp_users
from api.controllers.task_controller import bp as bp_tasks
from api.controllers.label_controller import bp as bp_labels
from api.config import LOGGING_CONFIG, DB_CONNECTION_STRING
from api.models import db

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


def init_app(testing=False):
    app = Flask(__name__)

    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": DB_CONNECTION_STRING,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    if testing is True:
        app.config.update({"TESTING": True})

    db.init_app(app)

    # Registering blueprints
    app.register_blueprint(bp_health)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_tasks)
    app.register_blueprint(bp_labels)

    # Generic HTTP error handler
    @app.errorhandler(HTTPException)
    def handle_general_exception(e: HTTPException):
        logger.info(e)
        return jsonify({"message": e.name}), e.code

    @app.errorhandler(InvalidUsageError)
    def handle_api_usage_error(e: InvalidUsageError):
        logger.info(e.message)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(InternalServerError)
    def handle_server_exception(e: InternalServerError):
        logger.exception(e)
        return jsonify({"message": "An unexpected error occured"}), e.code

    return app


app = init_app()
