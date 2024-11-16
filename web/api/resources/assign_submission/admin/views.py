import werkzeug.security
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace

from web.api.resources.assign_submission.admin.parser import register_parser, login_parser
from web.api.resources.assign_submission.admin.serializer import register_user_serializer, login_user_serializer
from web.api.resources.assign_submission.user.model import AssignUser, Assignment
from web.api.resources.assign_submission.user.utils import data_envelope, format_response

ns = Namespace("Admin API", description="API to interact with Admin Panel", path="/admin")


@ns.route("/register")
class RegisterAdmin(Resource):
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

        admin = AssignUser()
        admin.user_id = admin.generate_id()
        admin.username = username
        admin.email = email
        admin.password = hashed_password
        admin.user_type = "admin"

        return format_response(admin, 200, "User Successfully Registered")


@ns.route("/login")
class LoginAdmin(Resource):
    @ns.expect(login_parser, validate=True)
    @ns.marshal_with(data_envelope(login_user_serializer))
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']

        if not username:
            return format_response(None, 400, "Username Is Required")

        admin = AssignUser.objects(username=username).first()
        if not admin:
            return format_response(None, 400, "Admin Doesn't Exist, Please Register")
        check_password = werkzeug.security.check_password_hash(admin.password, password)
        if not check_password:
            return format_response(None, 400, "Wrong Password, Please Try Again")
        if admin and check_password:
            identity = str(admin.username)
            access_token = create_access_token(identity=identity)
            AssignUser.objects(username=username).update(set__access_token=access_token)

            admin = AssignUser.objects(username=username).first()

            return format_response(admin, 200, "Login Successfully Admin Panel", save=False)
        else:
            return format_response(None, 500, "Server Error")


@ns.route('/assignments')
class ViewAssignments(Resource):
    @jwt_required()
    def get(self):
        admin_username = get_jwt_identity()

        admin = AssignUser.objects(username=admin_username, user_type="admin").first()
        if not admin:
            return {"message": "Admin not found or not authorized to perform this action"}, 403

        assignments = Assignment.objects(admin=admin_username)
        if not assignments:
            return {"message": "No assignments found for this admin"}, 404

        result = []
        for assignment in assignments:
            result.append({
                "user_name": assignment.user.username,
                "task": assignment.task,
                "assign_id": assignment.assign_id,
                "submitted_at": assignment.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                "status": assignment.status
            })

        return jsonify(assignments=result)


@ns.route("/assignments/<string:assign_id>/accept")
class AcceptAssignment(Resource):
    @jwt_required()
    def post(self, assign_id):
        admin_username = get_jwt_identity()

        admin = AssignUser.objects(username=admin_username, user_type="admin").first()
        if not admin:
            return format_response(None, 403, "Admin not found or not authorized to perform this action")

        assignment = Assignment.objects(assign_id=assign_id).first()
        if not assignment:
            return format_response(None, 404, "Assignment not found")

        if assignment.status in ["accepted", "rejected"]:
            return format_response(None, 400, "Assignment has already been processed")

        if assignment.admin != admin.username:
            return format_response(None, 403, "This assignment is not assigned to you")

        assignment.update(status="accepted")

        return format_response(None, 200, f"Assignment {assign_id} accepted successfully")


@ns.route("/assignments/<string:assign_id>/reject")
class RejectAssignment(Resource):
    @jwt_required()
    def post(self, assign_id):
        admin_username = get_jwt_identity()

        admin = AssignUser.objects(username=admin_username, user_type="admin").first()
        if not admin:
            return format_response(None, 403, "Admin not found or not authorized to perform this action")

        assignment = Assignment.objects(assign_id=assign_id).first()
        if not assignment:
            return format_response(None, 404, "Assignment not found")

        if assignment.status in ["accepted", "rejected"]:
            return format_response(None, 400, "Assignment has already been processed")

        if assignment.admin != admin.username:
            return format_response(None, 403, "This assignment is not assigned to you")

        assignment.update(status="rejected")

        return format_response(None, 200, f"Assignment {assign_id} rejected successfully")
