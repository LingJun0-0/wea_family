from flask import request, g
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from wea_family.config import get_config
from wea_family.utils.decorators import verify_json_body

product_properties = {
    'name': {'type': 'string'},
    'index_name': {'type': 'string'},
    'description': {'type': 'string'},
    'user_custom_type': {'type': 'string'},
    'start_date': {'type': 'string'},
    'init_cash': {'type': 'number', 'minimum': 0},
    'benchmark': {
        'type': 'object',
        'required': ['type', 'id'],
        'properties': {
            'type': {'type': 'string'},
            'id': {'type': 'string'},
        }
    },
    'resource_ids': {
        'type': 'array',
        'items': {'type': 'string'},
        'uniqueItems': True,
    },
    'source': {'type': 'string'},
}


class IndexProductView(MethodView):

    def get(self, index_name):
        if index_name is None:

            return []
        else:

            res = {
                'start_date': '',
                'resource_ids': []
            }
            return res

    @verify_json_body({
        'type': 'object',
        'required': ['name', 'source', 'start_date', 'init_cash',
                     'benchmark', 'resource_ids', 'user_custom_type'],
        'properties': product_properties
    })
    def post(self):
        json = request.json
        headers = {
            'X-AMS-User': g.x_ams_user,
            'X-AMS-Workspace': g.workspace,
        }

        return {}
