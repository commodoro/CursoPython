# Ejercicio: Extrae Info
# %% Enunciado

'''
    Recibimos cada pocos minutos mensaje desde una estación meteorológica con este formato:
        “temp:00X-hum:X-lluvia:[si|no]”
    Es decir, la temperatura en kelvin, la humedad en porcentaje relativo (0-99) y ‘si’ o ‘no’ cuando hay lluvia. Un ejemplo puede ser:
        “temp:290-hum:54-lluvia:si”
    Extrae la información y muestra por pantalla la misma información con mejor formato y la temperatura en grados centígrados.
'''

# %% Resolución

ejemplo = 'temp:290-hum:44-lluvia:si'

# Averiguamos la posición relativa de cada elemento
temp_pos = ejemplo.find('temp:') + len('temp:')
hum_pos = ejemplo.find('hum:') + len('hum:')
rain_pos = ejemplo.find('lluvia:') + len('lluvia:')

# Como la cadena puede cambiar de tamaño en 1 unidad hay que tenerlo en cuenta
# a la hora de leer el dato de la humedad
LONG_MAX_STRING = 25
hum_lon = 2 - (LONG_MAX_STRING - len(ejemplo))

# Extraemos info
temp = int(ejemplo[temp_pos:temp_pos+3])
hum = int(ejemplo[hum_pos:hum_pos+hum_lon])
rain = ejemplo[rain_pos:rain_pos+2]

# Imprimimos con Formato
out = f'''
Temperatura [C]:    {temp-273}
Humedad [%]:        {hum}
Lluvia:             {rain.capitalize()}
'''
print(out)