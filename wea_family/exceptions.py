from flask import jsonify, Response


class WeBankException(Exception):
    errno = 10001
    status_code = 500

    def __init__(self, message):
        self.msg = message

    @property
    def message(self):
        return str(self.msg)

    def __str__(self):
        return f"{self.message:.80}"

    def as_http_response(self):
        response: Response = jsonify({
            "errno": self.errno,
            "error_message": 'Internal Error',
            "error_detail": str(self),
        })
        response.status_code = self.status_code
        return response
