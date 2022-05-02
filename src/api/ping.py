# src/api/ping.py


from flask_restx import Namespace, Resource  # updated

ping_namespace = Namespace("ping")  # new


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong"}


ping_namespace.add_resource(Ping, "")  # updated
