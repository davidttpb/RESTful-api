# src/api/ping.py


from flask import Blueprint
from flask_restx import Api, Namespace, Resource  # updated

ping_namespace = Namespace("ping")  # new


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


ping_namespace.add_resource(Ping, "")  # updated
