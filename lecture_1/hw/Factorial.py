import math, json
from lecture_1.hw.send_resp_http import send_response


async def factorial_handler(scope, recive, send) -> None:
    if scope["type"] != "http":
        await send_response(send, 404, {"error": "Not Found"})
        return

    if scope["method"] != "GET":
        await send_response(send, 404, {"error": "Not Found"})
        return

    query_string = scope["query_string"].decode()
    parse = dict(q.split("=") for q in query_string.split("&"))

    n_str = parse.get("n")

    if n_str is None:
        await send_response(send, 422, {"error": "Missed"})
        return

    n_int = int(n_str)
    if not (isinstance(n_int, int)):
        await send_response(send, 422, {"error": "Number nums be integer"})
        return

    if n_int < 0:
        await send_response(send, 400, {"error": "the number is negative"})
        return

    result = math.factorial(n_int)
    await send_response(send, 200, {"result": result})