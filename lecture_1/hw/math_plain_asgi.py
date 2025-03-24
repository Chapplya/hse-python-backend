from lecture_1.hw.Factorial import FactorialHandler
from lecture_1.hw.fibonacci import FibonacciHandler
from lecture_1.hw.mean import MeanHandler
from lecture_1.hw.base import Base


handler_reg = {
    "factorial": FactorialHandler,
    "fibonacci": FibonacciHandler,
    "mean": MeanHandler,
}


async def app(scope, receive, send):
    send_resp = Base(scope, receive, send)
    path = scope["path"]
    path_splitted = path.strip("/").split("/")
    path_str = path_splitted[0]
    if (handler_class := handler_reg.get(path_str)) is not None:
        await handler_class(scope, receive, send).handle()
    else:
        await send_resp(send, 404, {"error": "Not Found!"})
