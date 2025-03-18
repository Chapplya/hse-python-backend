from lecture_1.hw.Factorial import factorial
from lecture_1.hw.fibonacci import FibonacciHandler
from lecture_1.hw.mean import Mean
from lecture_1.hw.base import send_response


async def app(scope, receive, send):
    path = scope["path"]

    if path == "/factorial":
        await factorial(scope, receive, send).handle()
    elif "/fibonacci" in path:
        await FibonacciHandler(scope, receive, send).handle()
    elif "/mean" in path:
        await Mean(scope, receive, send).handle()
    else:
        await send_response(send, 404, {"error": "Not Found!"})
