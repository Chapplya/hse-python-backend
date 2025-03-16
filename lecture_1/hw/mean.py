import json


async def mean_handler(scope, recive, send):
    if scope["type"] != "http":
        await send(
            {
                "type": "http.response.start",
                "status": 404,
                "header": [(b"content-type", b"application/json")],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": json.dumps({"error": "Not Found"}).encode(),
            }
        )
        return

    if scope["method"] != "GET":
        await send(
            {
                "type": "http.response.start",
                "status": 404,
                "header": [(b"content-type", b"application/json")],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": json.dumps({"error": "Not Found"}).encode(),
            }
        )
        return

    get_body = await recive()  # вытягиает тело запроса клиента как слвоарь

    get_mas = json.loads(
        get_body.get("body", b"")
    )  # json.loads()  преобразует полученный объект в словарь

    if not (get_mas):
        await send(
            {
                "type": "http.response.start",
                "status": 422,
                "header": [(b"content-type", b"application/json")],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": json.dumps({"error": "Missed"}).encode(),
            }
        )
        return

    if not (isinstance(get_mas, list)):
        await send(
            {
                "type": "http.response.start",
                "status": 422,
                "header": [(b"content-type", b"application/json")],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": json.dumps({"error": "Number musm be integer"}).encode(),
            }
        )
        return

    if len(get_mas) == 0:
        await send(
            {
                "type": "http.response.start",
                "status": 400,
                "headers": [(b"content-type", b"application/json")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": json.dumps({"error": "Array cannot be empty"}).encode(),
            }
        )
        return

    for elem in get_mas:
        if not (isinstance(elem, float)):
            await send(
                {
                    "type": "http.response.start",
                    "status": 422,
                    "headers": [(b"content-type", b"application/json")],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": json.dumps({"error": "There is no float"}).encode(),
                }
            )
            return

    result = sum(get_mas) / len(get_mas)

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {"type": "http.response.body", "body": json.dumps({"result": result}).encode()}
    )
