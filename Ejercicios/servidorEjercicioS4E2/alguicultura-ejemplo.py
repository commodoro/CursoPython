import json
from bottle import request, route, run, abort, response


def check_headers():
    headers = ['User-Agent', 'Accept', 'Content-Length']
    for h in headers:
        if request.get_header(h) is None:
            return False
    return True


@route('/explotacion')
def explotacion():
    if not check_headers():
        abort(400, "Few headers")
    with open('./alguicultura.json', 'r') as f:
        data = json.load(f)
    out = json.dumps(data)
    response.add_header("Content-Type",
                        "application/json; charset=UTF-8")
    return out


@route('/explotacion/piscinas')
def piscinas():
    if not check_headers():
        abort(400, "Few headers")
    with open('./alguicultura.json', 'r') as f:
        data = json.load(f)
    out = json.dumps(data['pools'])
    response.add_header("Content-Type",
                        "application/json; charset=UTF-8")
    return out


@route('/explotacion/piscinas/<n:int>')
def piscina(n):
    if not check_headers():
        abort(400, "Few headers")
    with open('./alguicultura.json', 'r') as f:
        data = json.load(f)
    if n >= len(data['pools']):
        abort(400, f'Not found pool #{n}')
    if n < 0:
        abort(400, 'Pool index starts at 0')
    out = json.dumps(data['pools'][n])
    response.add_header("Content-Type",
                        "application/json; charset=UTF-8")
    return out


@route('/explotacion/piscinas/<n:int>/sensores')
def sensores(n):
    if not check_headers():
        abort(400, "Few headers")
    with open('./alguicultura.json', 'r') as f:
        data = json.load(f)
    if n >= len(data['pools']):
        abort(400, f'Not found pool #{n}')
    if n < 0:
        abort(400, 'Pool index starts at 0')
    out = json.dumps(data['pools'][n]['sensors'])
    response.add_header("Content-Type",
                        "application/json; charset=UTF-8")
    return out


@route('/explotacion/piscinas/<n:int>/sensores/<sensor>')
def sensor(n, sensor):
    if not check_headers():
        abort(400, "Few headers")
    with open('./alguicultura.json', 'r') as f:
        data = json.load(f)
    if n >= len(data['pools']):
        abort(400, f'Not found pool #{n}')
    if n < 0:
        abort(400, 'Pool index starts at 0')
    if sensor not in ['ph', 'temp', 'sali', 'refr']:
        abort(400, f"Sensor '{sensor}' does not exist")
    out = json.dumps(data['pools'][n]['sensors'][sensor])
    response.add_header("Content-Type",
                        "application/json; charset=UTF-8")
    return out


@route('/set/piscinas/<n:int>')
def gset_piscinas(n):
    if not check_headers():
        abort(400, "Few headers")
    info = request.get_header('info')
    if info is not None and info == 'false':
        response.add_header("Content-Type",
                            "application/json; charset=UTF-8")
        with open('./auto-alguicultura.json', 'r') as f:
            data = json.load(f)
            return json.dumps(data['pools'][n])
    else:
        response.add_header("Content-Type",
                            "text/html; charset=UTF-8")
        return '''<b>This is a example of payload</b>
        <p>{'ph': 7.25, 'temp': 20.2, 'refr': 4.1, 'sali': 33}</p>
        '''


@route('/set/piscinas/<n:int>', method='POST')
def set_piscinas(n):
    if not request.get_header('content-type') == 'application/json':
        abort(400, "POST methods only accept content in json format")
    data = request.json
    for key in data.keys():
        if key not in ['ph', 'temp', 'sali', 'refr']:
            abort(400, f"Sensor '{key}' does not exist")
    for key in ['ph', 'temp', 'sali', 'refr']:
        if key not in data:
            abort(400, f"Sensor '{key}' not found in request")
    for value in data.values():
        if type(value) not in (int, float):
            abort(400, f"Arguments must be numbers")
    with open('./auto-alguicultura.json', 'r+') as f:
        base = json.load(f)
        base['pools'][n] = data
        f.seek(0)
        f.truncate()
        json.dump(base, f, indent=4)
    return 'OK'


@route('/set/piscinas/<n:int>/<sensor>')
def gset_sensor(n, sensor):
    if not check_headers():
        abort(400, "Few headers")
    if sensor not in ['ph', 'temp', 'sali', 'refr']:
        abort(400, f"Sensor '{sensor}' does not exist")
    info = request.get_header('info')
    if info is not None and info == 'false':
        response.add_header("Content-Type",
                            "application/json; charset=UTF-8")
        with open('./auto-alguicultura.json', 'r') as f:
            data = json.load(f)
            return json.dumps({sensor: data['pools'][n][sensor]})
    else:
        response.add_header("Content-Type",
                            "text/html; charset=UTF-8")
        return '''<b>This is a example of payload</b>
        <p>{'ph': 7.25}</p>
        '''


@route('/set/piscinas/<n:int>/<sensor>', method='POST')
def set_sensor(n, sensor):
    if not request.get_header('content-type') == 'application/json':
        abort(400, "POST methods only accept content in json format")
    data = request.json
    if sensor not in ['ph', 'temp', 'sali', 'refr']:
        abort(400, f"Sensor {sensor} does not exist")
    if not len(data) == 1:
        abort(400, "/set/piscinas/<n:int>/<sensor> only accepts one argument")
    if sensor not in data:
        abort(400, f"Bad argument")
    value = data[sensor]
    if type(value) not in (int, float):
        abort(400, f"Arguments must be numbers")
    with open('./auto-alguicultura.json', 'r+') as f:
        base = json.load(f)
        base['pools'][n][sensor] = value
        f.seek(0)
        f.truncate()
        json.dump(base, f, indent=4)
    return 'OK'


if __name__ == "__main__":
    run(host='0.0.0.0', port=50600)
