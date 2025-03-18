import math
from lecture_1.hw.base import Base, send_response


class factorial(Base):
    async def handle(self):
        if self.scope["type"] != "http":
            await send_response(self.send, 404, {"error": "Not Found"})
            return

        if self.scope["method"] != "GET":
            await send_response(self.send, 404, {"error": "Not Found"})
            return

        parse = await self.parse_str("query_string")

        n_str = parse.get("n")

        if n_str is None:
            await send_response(self.send, 422, {"error": "Missed"})
            return

        n_int = int(n_str)
        if not (isinstance(n_int, int)):
            await send_response(self.send, 422, {"error": "Number nums be integer"})
            return

        if n_int < 0:
            await send_response(self.send, 400, {"error": "the number is negative"})
            return

        result = math.factorial(n_int)
        await send_response(self.send, 200, {"result": result})
