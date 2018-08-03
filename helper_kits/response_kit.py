from flask import make_response, jsonify

from util_kit import prepare_json_response


class ResponseReturnKit(object):

    @staticmethod
    def error400(msg="Failed to complete your request"):
        return {"error": msg}, 400

    @staticmethod
    def error404(msg="Not found"):
        return {"error": msg}, 404

    @staticmethod
    def error500(msg="Failed to complete your request"):
        return {"error": msg}, 500

    @staticmethod
    def http200(msg="Success", data={}):
        return make_response(
                jsonify(
                    prepare_json_response(
                        success=True,
                        message=msg,
                        data=data
                    )
                ), 200)