from flask import Blueprint

from wea_family.utils.flask_ext import MethodViewApi
from wea_family.views.product.product import IndexProductView

bp = Blueprint(__name__, __name__, url_prefix='/api/rqams_wz/v1')
api = MethodViewApi(bp, url_prefix='/products')

api.register_method_view(IndexProductView, '/indexes', defaults={'index_name': None}, methods=['GET'])
api.register_method_view(IndexProductView, '/indexes/<string:index_name>', methods=['GET'])
api.register_method_view(IndexProductView, '/indexes', methods=['POST'])
