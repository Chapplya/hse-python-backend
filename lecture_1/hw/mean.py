import json
from lecture_1.hw.base import send_response, Base, Strategy


class MeanHandler(Base, Strategy):
    async def handle(self):
        if self.scope["type"] != "http" or self.scope["method"] != "GET":
           await send_response(self.send, 404, {"error": "Not Found"})
           return

        get_mas = await self.get_body

        if not (get_mas):
            await send_response(self.send, 422, {"error": "Missed"})
            return

        if not (isinstance(get_mas, list)):
            await send_response(self.send, 422, {"error": "Number nums be integer"})
            return

        if len(get_mas) == 0:
            await send_response(self.send, 400, {"error": "Array cannot be empty"})
            return

        for elem in get_mas:
            if not (isinstance(elem, float)):
                await send_response(self.send, 422, {"error": "There is no float"})
                return

        result = sum(get_mas) / len(get_mas)

        await send_response(self.send, 200, {"result": result})
        return
