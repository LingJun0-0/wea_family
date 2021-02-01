from functools import wraps
from jsonschema import Draft7Validator

from flask import request
from werkzeug.exceptions import BadRequest

from wea_family.utils.type_hints import Type, Dict


def verify_json_body(schema: Dict, error_class: Type[Exception] = BadRequest):
    """ a request args validator decorator

    :param schema: json schema draft7
    :param error_class: error class when have error
    :return: function
    """
    validator = Draft7Validator(schema)

    def decorator(user_func):
        @wraps(user_func)
        def wrapper(*args, **kwargs):
            for i in validator.iter_errors(request.json):
                a = '.'.join(str(j) for j in i.absolute_path)
                msg = f"{a}: {i.message}"
                raise error_class(msg)

            return user_func(*args, **kwargs)

        return wrapper

    return decorator
