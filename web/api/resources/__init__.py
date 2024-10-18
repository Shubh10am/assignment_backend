import importlib
from flask import Blueprint
from flask_restx import Api

api = Api(version="1.0",
          title="Backend API",
          description="API to manage your backend account and Services", ui=False)


resources_blueprint = Blueprint("api", __name__)
api.init_app(resources_blueprint)

from web.api.resources.ottermap_task.views import ns as user_namespace
api.add_namespace(user_namespace)

modules = (
    'web.api.resources.ottermap_task.views',
)


def _init_modules():
    all_modules = modules

    for item in all_modules:
        if isinstance(item, str):
            item = (item, 'ns')  # 'ns' is default package

        module, package = item

        try:
            imported_module = importlib.import_module(module)

            try:
                ns = getattr(imported_module, package)
            except AttributeError:
                raise ModuleNotFoundError

            api.add_namespace(ns)
        except (ImportError, ModuleNotFoundError):
            raise


_init_modules()
