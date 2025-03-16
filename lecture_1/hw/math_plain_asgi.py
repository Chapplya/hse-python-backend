from lecture_1.hw.Factorial import factorial_handler, json

async def app(scope, receive, send):
    path = scope['path']

    if path == '/factorial':
        await factorial_handler(scope, receive, send)
    else:
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'error': 'Not Found'}).encode()
        })
