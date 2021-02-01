from flask import Flask, Response

from wea_family.exceptions import WeBankException
from wea_family.utils.flask_ext import Mongo, ExceptionHandler
from wea_family.utils.type_hints import Dict


http_exception_ext = ExceptionHandler()
mongo = Mongo(appname='wea_family', w='majority')


def create_app(config: Dict) -> Flask:
    app = Flask(__name__)

    app.config.from_mapping(config)

    mongo.init_app(app, connect=False)
    _register_blueprint(app)
    http_exception_ext.init_app(app, debug=app.config.get('WEBANK_DEBUG'))
    return app


def _register_blueprint(app):
    from wea_family.urls import (
        product_api
    )
    app.register_blueprint(product_api.blueprint)


@http_exception_ext.register(WeBankException)
def _response_rqams_exception(err: WeBankException) -> Response:
    return err.as_http_response()
