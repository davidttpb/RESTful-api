# src/api/users.py


from flask import Blueprint, request
from flask_restx import Api, Resource, fields

# new
from src.api.crud import (  # isort:skip
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)


user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @api.marshal_with(user, as_list=True)
    def get(self):
        return get_all_users(), 200  # updated

    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email)  # updated
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        add_user(username, email)  # new

        response_object["message"] = f"{email} was added!"
        return response_object, 201


class Users(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        user = get_user_by_id(user_id)  # updated
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200

    @api.expect(user, validate=True)
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)  # updated
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):  # updated
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        update_user(user, username, email)  # new

        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200

    def delete(self, user_id):
        response_object = {}
        user = get_user_by_id(user_id)  # updated

        if not user:
            api.abort(404, f"User {user_id} does not exist")

        delete_user(user)  # new

        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<int:user_id>")
