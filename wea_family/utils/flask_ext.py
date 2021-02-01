from functools import partial
from typing import Optional, Type, Union, List, Dict

import pymongo
from flask import Blueprint, Flask, jsonify
from flask.views import MethodView
from pymongo.database import Database
from werkzeug.exceptions import HTTPException, default_exceptions


class MethodViewApi:
    default_url_prefix = '/api/rqams_wz/v1'

    def __init__(self, blueprint: Blueprint = None, url_prefix: Optional[str] = None):
        self.blueprint = blueprint
        self.to_do = []
        self._view_func_to_do = []
        if url_prefix is not None:
            self.check_url(url_prefix)
            self.url_prefix = url_prefix
        else:
            self.url_prefix = self.default_url_prefix
        if blueprint:
            self.init_app(blueprint)

    @staticmethod
    def check_url(url: str) -> None:
        assert isinstance(url, str)
        if url != '/' and url != '':
            if url.endswith('/'):
                raise ValueError('url should not endswith a slash')
            if not url.startswith('/'):
                raise ValueError('url must startswith a slash')

    def init_app(self, blueprint: Blueprint):
        for view, url, endpoint, class_args, class_kwargs, options in self.to_do:
            self.register_method_view(view, url, endpoint, class_args, class_kwargs, **options)
        self.to_do.clear()

        for arguments in self._view_func_to_do:
            self.register_view_func(**arguments)
        self._view_func_to_do.clear()

    def ensure_url(self, url):
        self.check_url(url)
        if url != '/':
            url = self.url_prefix + url
        else:
            url = self.url_prefix
        return url

    def register_method_view(self, method_view: Type[MethodView], url: str, endpoint=None, class_args=None, class_kwargs=None, **options):
        if not issubclass(method_view, MethodView):
            raise TypeError(f'unknown method view: {method_view}')

        bp = self.blueprint
        url = self.ensure_url(url)

        # 当不同路由注册同一个 MethodView 时对其 as_view 名字区分
        if getattr(method_view, 'call_counts', None) is None:
            setattr(method_view, 'call_counts', 0)
        else:
            method_view.call_counts += 1

        if bp:
            class_args = class_args or ()
            class_kwargs = class_kwargs or {}
            bp.add_url_rule(
                url, endpoint=endpoint,
                view_func=method_view.as_view(
                    method_view.__qualname__+str(method_view.call_counts), *class_args, **class_kwargs
                ),
                **options
            )
        else:
            self.to_do.append((method_view, url, endpoint, class_args, class_kwargs, options))

    def register_view_func(self, view_func: callable, route: str, methods: Union[List[str], str] = None):
        bp = self.blueprint

        if methods is None:
            methods = getattr(view_func, 'http_method', None)

        if isinstance(methods, str):
            methods = [methods]

        route = self.ensure_url(route)

        if bp:
            bp.add_url_rule(route, view_func=view_func, methods=methods)
        else:
            arguments = dict(
                route=route,
                view_func=view_func,
                methods=methods,
            )
            self._view_func_to_do.append(arguments)


class ExceptionHandler(object):
    def __init__(self, app: Optional[Flask] = None, debug: bool = False):
        self.app: Flask = app
        self.debug = debug
        self._to_do = []
        if app:
            self.init_app(app)

    def std_handler(self, error, code=None, message=None):
        if isinstance(error, HTTPException):
            code = error.code
            error_message = error.description
        else:
            code = 500 if code is None else code
            error_message = message or str(error)
        if code == 500:
            response = jsonify(errno=10000, error_message=error_message)
        else:
            response = jsonify(error_message=error_message)
        response.status_code = code
        return response

    def init_app(self, app, debug=None):
        self.app = app
        if debug is not None:
            self.debug = debug
        if self.debug is None:
            self.debug = app.debug

        self.register_with_handler(HTTPException)
        for code, v in default_exceptions.items():
            self.register_with_handler(code)
            self.register_with_handler(v)
        if not self._to_do:
            return
        for exception_or_code, handler in self._to_do:
            self.app.errorhandler(exception_or_code)(handler)

    def register(self, exception_or_code):
        def decorator(f):
            self.register_with_handler(exception_or_code, f)
            return f

        return decorator

    def register_with_handler(self, exception_or_code, handler=None):
        if self.app:
            self.app.errorhandler(exception_or_code)(handler or self.std_handler)
        else:
            self._to_do.append((exception_or_code, handler or self.std_handler))

    def register_std_handle(self, exception_or_code, code: int, message: Optional[str] = None):
        handler = partial(self.std_handler, code=code, message=message)
        if self.app:
            self.app.errorhandler(exception_or_code)(handler)
        else:
            self._to_do.append((exception_or_code, handler))


class Mongo:
    def __init__(self, app=None, uri=None, db_name=None, **kwargs):
        self.app: Flask = app
        self.db_name: str = db_name
        self.uri: str = uri
        self.client: pymongo.MongoClient = None
        self.database: Database = None
        self.gridfs: gridfs.GridFS = None
        self.kwargs: Dict = kwargs
        if self.app:
            self.init_app(app, uri, **kwargs)

    def init_app(self, app: Flask, uri=None, db_name=None, **kwargs):
        self.app = app
        if uri:
            self.uri = uri
        if db_name:
            self.db_name = db_name
        if kwargs:
            self.kwargs.update(kwargs)

        if not self.uri:
            self.uri = app.config['MONGO_URL']

        self.app = app
        self.client = pymongo.MongoClient(self.uri, **self.kwargs)
        self.database = self.client.get_database(
            self.db_name, write_concern=pymongo.WriteConcern(w='majority')
        )
        self.gridfs = gridfs.GridFS(self.database)  # mongo 文件存储, coll: fs.*
        self.app.extensions['mongo'] = self
