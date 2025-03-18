from lecture_1.hw.send_resp_http import send_response

def fibonacci_func(n):
    if n <= 1:
        return n
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


async def fibonacci_handler(scope, recive, send):
    if scope["type"] != "http":
        await send_response(send, 404, {"error": "Not Found"})
        return

    if scope["method"] != "GET":
        await send_response(send, 404, {"error": "Not Found"})
       

    path = scope["path"]
    path_parts = path.split("/")

    n_str = path_parts[-1]

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
    
    result = fibonacci_func(n_int)
    await send_response(send, 200, {"result": result})
