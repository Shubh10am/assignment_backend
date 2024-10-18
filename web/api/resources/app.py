from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv(find_dotenv())
from lib.config import app
from web.api.resources import resources_blueprint

jwt = JWTManager()


def init_resources():
    jwt.init_app(app)
    app.config["PROJECT_ID"] = '_BACKEND'
    app.config['RESTPLUS_MASK_HEADER'] = False
    app.register_blueprint(resources_blueprint)


# init_manager()
init_resources()
app.config["BUNDLE_ERRORS"] = True
CORS(app, supports_credentials=True)

if __name__ == "__main__":
    app.run()
