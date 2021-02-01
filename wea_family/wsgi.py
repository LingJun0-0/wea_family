from flask import g, request
from json import loads
from base64 import decodebytes

from wea_family.factory import create_app
from wea_family.config import get_config

app = create_app(get_config())


@app.before_request
def set_g_attribute():
    data = request.headers.get('X-AMS-User', as_bytes=True)
    g.x_ams_user = data
    userinfo = loads(decodebytes(data))
    g.current_user = userinfo['userId']

    workspace_id = request.headers.get('X-AMS-Workspace')
    g.workspace = workspace_id


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, use_reloader=True)
