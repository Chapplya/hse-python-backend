from lecture_1.hw.Factorial import factorial_handler, json
from lecture_1.hw.fibonacci import fibonacci_handler
from lecture_1.hw.mean import mean_handler
from lecture_1.hw.send_resp_http import send_response


async def app(scope, receive, send):
    path = scope["path"]

    if path == "/factorial":
        await factorial_handler(scope, receive, send)
    elif "/fibonacci" in path:
        await fibonacci_handler(scope, receive, send)
    elif "/mean" in path:
        await mean_handler(scope, receive, send)
    else:
        await send_response(send, 404, {"error": "poshel nahuy"})
