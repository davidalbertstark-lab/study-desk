from typing import Any


def success_response(
    data: Any = None,
    message: str = "success"
):
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }


def error_response(
    message: str,
    errors: Any = None
):
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }