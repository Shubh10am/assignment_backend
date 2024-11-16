import werkzeug.security
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace

from web.api.resources.assign_submission.admin.parser import register_parser, login_parser
from web.api.resources.assign_submission.admin.serializer import register_user_serializer, login_user_serializer
from web.api.resources.assign_submission.user.model import AssignUser, Assignment
from web.api.resources.assign_submission.user.utils import data_envelope, format_response

ns = Namespace("User API", description="API to interact with User And Assignments", path="/user")


@ns.route("/register")
class RegisterUser(Resource):
    @ns.expect(register_parser, validate=True)
    @ns.marshal_with(data_envelope(register_user_serializer))
    def post(self):
        args = register_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        if not username:
            return format_response(None, 400, "Name Should be there")
        if not email:
            return format_response(None, 400, "Email Should be there")

        if AssignUser.objects(username=username).first():
            return format_response(None, 400, "Username Already Exist, Try Another Username")

        if AssignUser.objects(email=email).first():
            return format_response(None, 400, "Email Already Exist, Try Another Email")

        hashed_password = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256')

        user = AssignUser()
        user.user_id = user.generate_id()
        user.username = username
        user.email = email
        user.password = hashed_password
        user.user_type = "user"

        return format_response(user, 200, "User Successfully Registered")


@ns.route("/login")
class LoginUser(Resource):
    @ns.expect(login_parser, validate=True)
    @ns.marshal_with(data_envelope(login_user_serializer))
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']

        if not username:
            return format_response(None, 400, "Username Is Required")

        user = AssignUser.objects(username=username).first()
        if not user:
            return format_response(None, 400, "User Doesn't Exist, Please Register")
        check_password = werkzeug.security.check_password_hash(user.password, password)
        if not check_password:
            return format_response(None, 400, "Wrong Password, Please Try Again")
        if user and check_password:
            identity = str(user.username)
            access_token = create_access_token(identity=identity)
            AssignUser.objects(username=username).update(set__access_token=access_token)

            user = AssignUser.objects(username=username).first()

            return format_response(user, 200, "Login Successfully", save=False)
        else:
            return format_response(None, 500, "Server Error")


@ns.route("/upload")
class AssignmentUpload(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        task = data.get('task')
        admin = data.get('admin')
        user = AssignUser.objects(username=get_jwt_identity()).first()

        if not task:
            return format_response(None, 400, "Task Is Required")
        if not admin:
            return format_response(None, 400, "Admin Is Required")

        assignment = Assignment(user=user, task=task, admin=admin)
        assignment.assign_id = assignment.generate_id()
        assignment.save()

        return format_response(None, 200, "Assignment uploaded successfully!", custom_ob=task)


@ns.route("/all-admin")
class FetchAllAdmins(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = AssignUser.objects(username=current_user).first()

        if not user or user.user_type != 'admin':
            return format_response(None, 403, "Only user can access this route")

        admins = AssignUser.objects(user_type='admin')
        admin_list = [{"username": admin.username} for admin in admins]

        return format_response(None, 200, "All Admin List", custom_ob=admin_list)
