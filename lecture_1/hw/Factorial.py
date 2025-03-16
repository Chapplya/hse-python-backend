import math, json

async def factorial_handler(scope, recive, send) -> None:
    if scope['type'] != 'http':
        await send({
            'type' : 'http.response.start',
            'status' : 404,
            'header' : [(b'content-type', b'application/json')]
        })
        
        await send ( {
            'type' : 'http.response.body',
            'body' : json.dumps({'error' : 'Not Found'}).encode()
        })
        return
    
    if scope['method'] != 'GET':
        await send({
            'type' : 'http.response.start',
            'status' : 404,
            'header' : [(b'content-type', b'application/json')]
        })
        
        await send({
            'type' : 'http.response.body',
            'body' : json.dumps({'error' : 'Not Found'}).encode()
        })
        return
    
    query_string = scope['query_string'].decode()
    parse = dict(q.split('=') for q in query_string.split('&'))
    
    n_str = parse.get('n')
    
    if n_str is None:
        await send({
            'type' : 'http.response.start',
            'status' : 422,
            'header' : [(b'content-type', b'application/json')]
        })
        
        await send({
            'type' : 'http.response.body',
            'body' : json.dumps({'error' : 'Missed'}).encode()
        })
        return
    
    n_int = int(n_str)
    if not(isinstance(n_int, int)):
        await send({
            'type' : 'http.response.start',
            'status' : 422,
            'header' : [(b'content-type', b'application/json')]
        })
        
        await send({
            'type' : 'http.response.body',
            'body' : json.dumps({'error' : 'Number musm be integer'}).encode()
        })
        return
    
    if n_int < 0:
        await send({
            'type' : 'http.response.start',
            'status' : 400,
            'header' : [(b'content-type', b'application/json')]
        })
        
        await send({
            'type' : 'http.response.body',
            'body' : json.dumps({'error' : 'the number is negative'}).encode()
        })
        return
        
    result = math.factorial(n_int)
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'application/json')]
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps({'result': result}).encode()
    })