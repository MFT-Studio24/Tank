import RPi.GPIO as GPIO
import signal
from flask import Flask, render_template, Response, request
from camera import Camera
from motor import Motor

pin_status_led = 17

app = Flask(__name__)

camera = Camera()
camera.setDaemon(True)
camera.start()

motor = Motor(pin_a1 = 21, pin_a2 = 20, pin_b1 = 16, pin_b2 = 12)
motor.setDaemon(True)
motor.start()

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_status_led, GPIO.OUT)
GPIO.output(pin_status_led, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(get_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_image():
    while True:
        jpeg = camera.jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n')

@app.route('/control')
def control():
    obj = request.args.get('obj')
    move = request.args.get('move')
    mode = request.args.get('mode')
    if (obj == "tank"):
        control_tank(move, mode)
    return ('', 204)

def control_tank(direction, mode):
    if (mode == "start"):
        motor.move_start(direction)
    elif (mode == "stop"):
        motor.move_stop()

def cleanup_gpio():
    GPIO.output(pin_status_led, 0)
    GPIO.cleanup()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, cleanup_gpio)
    try:
        app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()
