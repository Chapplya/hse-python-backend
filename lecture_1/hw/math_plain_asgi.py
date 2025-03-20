from lecture_1.hw.Factorial import FactorialHandler
from lecture_1.hw.fibonacci import FibonacciHandler
from lecture_1.hw.mean import MeanHandler
from lecture_1.hw.base import send_response



handler_reg = {
    "factorial": FactorialHandler,
    "fibonacci": FibonacciHandler,
    "mean" : MeanHandler
}

async def app(scope, receive, send):
    path = scope["path"]
    path_splitted = path.strip('/').split('/')
    path_str = path_splitted[0]
    if path_str in handler_reg:
        handler_class = handler_reg[path_str]
        handler = handler_class(scope, receive, send)
        await handler.handle()
    else:
        await send_response(send, 404, {"error": "Not Found!"})

