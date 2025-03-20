from lecture_1.hw.base import Base, fibonacci_func, Strategy


class FibonacciHandler(Base, Strategy):
    async def handle(self):
        if self.scope["type"] != "http" or self.scope["method"] != "GET":
            await self.send_response(self.send, 404, {"error": "Not Found"})
            return

        path_parts = await self.parse_str("path")
        n_str = path_parts[-1]

        if n_str is None:
            await self.send_response(self.send, 422, {"error": "Missed"})
            return

        n_int = int(n_str)
        if not (isinstance(n_int, int)):
            await self.send_response(self.send, 422, {"error": "Number nums be integer"})
            return

        if n_int < 0:
            await self.send_response(self.send, 400, {"error": "the number is negative"})
            return

        result = fibonacci_func(n_int)
        await self.send_response(self.send, 200, {"result": result})
