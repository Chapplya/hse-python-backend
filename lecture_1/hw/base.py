import json
import http
from typing import Any, Callable, Awaitable


class Base:
    def __init__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ):
        self.scope = scope
        self.receive = receive
        self.send = send

    def fibonacci_func(self, n):
        if n <= 1:
            return n
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

    async def parse_str(self, scope_quest):
        if scope_quest == "query_string":
            query_string = self.scope[f"{scope_quest}"].decode()
            return dict(q.split("=") for q in query_string.split("&"))
        elif scope_quest == "path":
            path = self.scope["path"]
            return path.split("/")

    async def get_body(self):
        get_body = await self.recive()  # вытягиает тело запроса клиента как слвоарь

        return json.loads(get_body.get("body", b""))


async def send_response(send, status_code: http.HTTPStatus, body: dict):
    response_body = json.dumps(body).encode("utf-8")
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(response_body)).encode("utf-8")),
    ]
    await send(
        {"type": "http.response.start", "status": status_code, "headers": headers}
    )
    await send(
        {
            "type": "http.response.body",
            "body": response_body,
        }
    )
