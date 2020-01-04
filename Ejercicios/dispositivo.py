#!/usr/bin/python3

import serial
import numpy as np
import sys
import time
from collections import deque
from threading import Timer
import re

TIME_ZERO = time.time()
CYCLE = 365*24*60*60
interval = 5
name = 'Device 1'

if sys.platform.startswith('win'):
    # Windows
    port = serial.Serial('COM200', 115200)
else:
    # Linux
    port = serial.Serial('/dev/ttyS1', 115200)


def measure_value(t: float) -> float:
    def omega(period: float) -> float:
        return 2*np.pi*period**-1
    x = t % CYCLE
    return 6*np.sin(x*omega(365*24*60*60)) + \
        4*np.sin(x*omega(24*60*60)) + \
        0.2*np.sin(x*omega(60*60)) + \
        0.01*np.sin(x*omega(60)) + \
        0.003*np.sin(x*omega(1)) + 10


def read(*args):
    assert len(args) <= 1
    load = ''
    if len(args) == 0:
        load = str(round(measure_value(time.time()), 4)) + '\n'
    else:
        if args[0] == 'HEAD':
            load = str(historic[-1][0]) + ' ' + \
                   str(round(historic[-1][1], 4)) + '\n'
        elif args[0] == 'ALL':
            for t, value in historic:
                load += str(t) + ' ' + str(value) + '\n'
        elif re.match(r'[0-9]+?[:]?[0-9]*', args[0]):
            indexes = args[0].split(':')
            if len(indexes) == 1:
                left = None if indexes[0] == '' else int(indexes[0])
                right = None
            else:
                left = None if indexes[0] == '' else int(indexes[0])
                right = None if indexes[1] == '' else int(indexes[1])

            if left is not None and right is not None:
                if left > right:
                    raise AssertionError('read a:b -> a < b')
            for t, value in historic:
                if left is not None and t < left:
                    continue
                elif right is not None and t > right:
                    break
                load += str(t) + ' ' + str(value) + '\n'

    port.write(bytes(load, 'ascii'))
    port.write(b'\n')


def get_value(*args):
    assert len(args) == 1
    if args[0] == 'INTERVAL':
        port.write(bytes(str(interval), 'ascii'))
    elif args[0] == 'NAME':
        port.write(bytes(str(name), 'ascii'))
    else:
        raise AssertionError('NO FOUND VALUE')
    port.write(b'\n')


def set_value(*args):
    global interval, name
    assert len(args) >= 2
    if args[0] == 'INTERVAL':
        try:
            interval = abs(int(args[1]))
        except ValueError:
            raise AssertionError('Input must be integer > 0')
        else:
            port.write(b'OK')
    elif args[0] == 'NAME':
        try:
            old = name
            name = ' '.join(args[1:])
            assert len(name) > 0
        except AssertionError:
            name = old
            port.write(b'Length of device name must be >0.')
        else:
            port.write(b'OK')
    else:
        raise AssertionError('NO FOUND VALUE')
    port.write(b'\n')


def delete(*args):
    global historic
    assert len(args) == 0
    historic = deque()
    port.write(b'OK\n')


def unknow_command():
    port.write(b'[ERROR]: UNKNOWN COMMAND\n')


def unknow_syntax(error):
    e = bytes(f'{str(error).upper()}', encoding='ascii')
    if len(e) == 0:
        e = b'BAD SYNTAX'
    port.write(b'[ERROR]: ' + e + b'\n')


def next_measure():
    global tim
    tim = Timer(interval, next_measure)
    tim.start()
    historic.append((int(time.time()), round(measure_value(time.time()), 4)))


RESP = {
    'read': read,
    'set': set_value,
    'get': get_value,
    'delete': delete
}


if __name__ == '__main__':
    historic = deque()
    t_0 = round(time.time())
    for i in range(60*24*30*6//5):
        t = t_0 - i*5
        historic.appendleft((t, round(measure_value(t), 4)))

    tim = Timer(interval, next_measure)
    tim.start()

    while True:
        if port.in_waiting > 0:
            data = port.readline()
            try:
                data = data.decode('ascii')
            except UnicodeDecodeError:
                data = 'ERROR'
            data = data.replace('\r', '')
            data = data.replace('\n', '')
            command, *arguments = data.split(' ')
            try:
                f = RESP[command]
                f(*arguments)
            except KeyError:
                unknow_command()
            except AssertionError as err:
                unknow_syntax(err)
