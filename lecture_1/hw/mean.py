import json
from lecture_1.hw.send_resp_http import send_response


async def mean_handler(scope, recive, send):
    if scope["type"] != "http":
        await send_response(send, 404, {"error": "Not Found"})
        return

    if scope["method"] != "GET":
        await send_response(send, 404, {"error": "Not Found"})
        return

    get_body = await recive()  # вытягиает тело запроса клиента как слвоарь

    get_mas = json.loads(
        get_body.get("body", b"")
    )  # json.loads()  преобразует полученный объект в словарь

    if not (get_mas):
        await send_response(send, 422, {"error": "Missed"})
        return

    if not (isinstance(get_mas, list)):
        await send_response(send, 422, {"error": "Number nums be integer"})
        return

    if len(get_mas) == 0:
        await send_response(send, 400, {"error": "Array cannot be empty"})
        return

    for elem in get_mas:
        if not (isinstance(elem, float)):
            await send_response(send, 422, {"error": "There is no float"})
            return

    result = sum(get_mas) / len(get_mas)

    await send_response(send, 200, {"result": result})
    return
