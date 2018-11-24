import requests
import json
import os

class State:
    is_good = False
    
def send(message):
    print('Sending message {}'.format(message))
    os.system("telegram-send '{}'".format(message))

URL_BASE = 'https://apigtw.vaisala.com/hackjunction2018/saunameasurements/'
CGI = 'latest?SensorID={}&limit=1'
URL_TEMPLATE = URL_BASE + CGI

MY_BEST_TEMPERATURE = 67.2

def get_message(temp):
    if temp > MY_BEST_TEMPERATURE:
        if not sauna_state.is_good:
            sauna_state.is_good = True
            return True, '{} degrees are waiting for You right now!'.format(temp)
    else :
        if sauna_state.is_good:
            sauna_state.is_good = False
            return True, 'Sauna is no so hot right now :('.format(temp)
    
    print('Status: {}, Temp ={} // No info, exiting.'.format(sauna_state.is_good, temp))
    return False, None

def get_temp(sensor_id):
    response = requests.get(URL_TEMPLATE.format(sensor_id))
    json_array = json.loads(response.text)
    temp = json_array[0]['Measurements']['Temperature']['value']
    return temp

def callback_fn(sensor_id):
    try:
        temp = get_temp(sensor_id)
        need_message, text = get_message(temp)
        if need_message:
            send('{}::{}'.format(sensor_id, text))
    except e:
        send("Excepcion caught: " + str(e))

def main_loop():
    while True:
        try:
            time.sleep(5)
            callback_fn('Bench1')
        except e:
            print('Uncaught exception: ' + str(e))
sauna_state = State()
main_loop()