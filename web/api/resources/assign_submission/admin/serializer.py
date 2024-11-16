from flask_restx import Api, fields


api = Api(version="1.0",
          title="Task Manage API",
          description="API to manage your Task and Services", ui=False)

register_user_serializer = api.model("Work Flow User Details", {
    "user_id": fields.String(description="Client ID of User"),
    "email": fields.String(description="Email of User"),
    "username": fields.String(description="Name of User"),
    "created_at": fields.DateTime(description="Account Created")
})

login_user_serializer = api.model("User details", {
    "email": fields.String(description="Email of User"),
    "username": fields.String(description="Name of User"),
    "access_token": fields.String(description="access token of user")
})