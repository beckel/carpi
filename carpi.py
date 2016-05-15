from __future__ import print_function

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import jsonify

import os
import sys
import time

from sensors.camera import Camera
from sensors.alarm import Alarm
from sensors.temp_pressure import TemperaturePressure
from sensors.imu import IMU
from internet import Internet

app = Flask(__name__)

@app.route("/")
def hello():
    return send_from_directory('static', 'index.html')

##################
## CAMERA
##################
@app.route('/camera', methods=['GET'])
def print_camera():
    return send_from_directory('static', 'camera.html')

@app.route('/state_camera', methods=['GET'])
def get_camera_state():
    return jsonify({'State': camera.get_state()})

@app.route('/camera', methods=['POST'])
def update_camera():
    if (request.form['switch'] == "on"):
        camera.switch_on()
    else:
        camera.switch_off()
    return 'OK'


##################
## ALARM
##################
@app.route('/alarm', methods=['GET'])
def print_alarm():
    return send_from_directory('static', 'alarm.html')

@app.route('/state_alarm', methods=['GET'])
def get_alarm_state():
    return jsonify({'State': alarm.get_state()})
    
@app.route('/alarm', methods=['POST'])
def update_alarm():
    if (request.form['switch'] == "on"):
        alarm.switch_on()
    else:
        alarm.switch_off()
    return 'OK'




##################
## ROOM CLIMATE
##################
@app.route('/room_climate', methods=['GET'])
def print_room_climate():
    return send_from_directory('static', 'room_climate.html')

@app.route('/temperature_and_pressure', methods=['GET'])
def get_temperature_and_pressure():
    (temperature, pressure) = temp_pressure.read()
    return jsonify({'Temperature': temperature, 'Pressure': pressure})





##################
## SETTINGS
##################
@app.route('/settings', methods=['GET'])
def print_settings():
    return send_from_directory('static', 'settings.html')

@app.route('/state_internet', methods=['GET'])
def get_internet_state():
    return jsonify({'State': internet.get_state()})

@app.route('/internet', methods=['POST'])
def update_internet():
    if (request.form['switch'] == "on"):
        internet.switch_on()
    else:
        internet.switch_off()
    return 'OK'
    
@app.route('/state_internet_ping', methods=['GET'])
def get_state_ping_successful():
    return jsonify({'State': internet.get_state_ping_successful()})
    






##################
## SENSORS
##################
@app.route('/sensor_view', methods=['GET'])
def print_sensors():
    return send_from_directory('static', 'sensor_view.html')
    
@app.route('/sensors/accelerometer', methods=['GET'])
def get_acceleration():
    (x,y,z) = imu.read_simple_accelerometer()
    return jsonify({'ACCx': x, 'ACCy': y, 'ACCz': z})






##################
## SHUTDOWN
##################
@app.route('/shutdown', methods=['GET'])
def print_shutdown():
    print('Shutdown page requested', file=sys.stderr)
    return send_from_directory('static', 'shutdown.html')
    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    print('Shutting down', file=sys.stderr)
    time.sleep(1)
    os.system("sudo shutdown -h now")
    return 'OK'





if __name__ == "__main__":
    camera = Camera()
    temp_pressure = TemperaturePressure()
    imu = IMU()
    alarm = Alarm(imu)
    internet = Internet()
    app.run(debug=True, host='0.0.0.0')
    
