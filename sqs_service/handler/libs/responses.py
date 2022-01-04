from typing import Any
from http import HTTPStatus
import json


def success_response(
    status_code: HTTPStatus,
    response: Any,
):
    return {
        "statusCode": status_code.value or HTTPStatus.OK.value,
        "body": json.dumps(response),
    }


def error_response(
    status_code: HTTPStatus,
    message: str = None,
):
    return {
        "statusCode": status_code.value or HTTPStatus.INTERNAL_SERVER_ERROR.value,
        "body": json.dumps(
            {
                "message": message
                or status_code.description
                or HTTPStatus.INTERNAL_SERVER_ERROR.description,
            }
        ),
    }
