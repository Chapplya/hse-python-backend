import json 
import http
async def send_response(send, status_code: http.HTTPStatus, body: dict):
    response_body = json.dumps(body).encode('utf-8')
    headers = [
        (b'content-type', b'application/json'),
        (b'content-length', str(len(response_body)).encode('utf-8'))
    ]
    await send({
        'type': 'http.response.start',
        'status': status_code,
        'headers': headers
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
    })