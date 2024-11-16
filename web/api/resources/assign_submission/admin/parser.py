from flask_restx import reqparse

register_parser = reqparse.RequestParser(bundle_errors=True)
register_parser.add_argument("email", type=str, nullable=False, help="User Email")
register_parser.add_argument("username", type=str,  help="Name of User")
register_parser.add_argument("password", type=str, default=None, help="Password")

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username of the user')
login_parser.add_argument('password', type=str, required=True, help='Password of the user')