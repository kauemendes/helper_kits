import flask
import os

from pymysql.cursors import Cursor
from sqlalchemy import text

from app import app, db
from flask import make_response, abort


class ApplicationKit:

    @staticmethod
    def do_database_commit():
        db.session.commit()

    @staticmethod
    def do_database_rollback():
        db.session.rollback()

    @staticmethod
    def execute_query(query: str, values: dict) -> Cursor:
        return db.session.connection().execute(text(query), values)

    @staticmethod
    def allow_large_concats():
        ApplicationKit.execute_query("SET SESSION group_concat_max_len = 1000000;", {})

    @staticmethod
    def get_request():
        return flask.request

    @staticmethod
    def get_request_json() -> dict:
        return flask.request.json

    @staticmethod
    def response_success(data: object):

        result = {
            "data": data,
            "meta": {
                "success": True,
                "url": ApplicationKit.get_request().url
            }
        }

        return make_response(flask.jsonify(result), 200)

    @staticmethod
    def response_auth_fail():
        ApplicationKit.response_error("Falha na Autenticação")

    @staticmethod
    def response_fail_data():
        ApplicationKit.response_error("Erro ao recuperar dados")

    @staticmethod
    def response_error(message: str):
        abort(400, message)

    @staticmethod
    def is_dev_mode() -> bool:
        if os.getenv('APP_SETTINGS') == "config.DevelopmentConfig" or \
                os.getenv('APP_SETTINGS') == "config.DevelopmentContainerConfig" or \
                app.config["DEBUG"]:
            return True

        return False
