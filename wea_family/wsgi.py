from flask import g, request

from wea_family.factory import create_app
from wea_family.config import get_config

app = create_app(get_config())


@app.before_request
def set_g_attribute():
    ...


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, use_reloader=True)
