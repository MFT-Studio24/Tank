import RPi.GPIO as GPIO
import time
import threading
import numpy as np
import copy

class Motor(threading.Thread):
    def __init__(self, pin_a1 = 21, pin_a2 = 20, pin_b1 = 16, pin_b2 = 12):
        super(Motor, self).__init__()

        self.motors = { "right": "m1", "left": "m2" }
        self.pins = { "m1": [pin_a1, pin_a2], "m2": [pin_b1, pin_b2] }
        self.state = { "stop": [1, 1], "forward": [0, 1], "backward": [1, 0] }
        self.motor_state = { "m1": "stop", "m2": "stop" }

        GPIO.setmode(GPIO.BCM)
        for pin_set in self.pins.values():
            for pin in pin_set:
                GPIO.setup(pin, GPIO.OUT)

        time.sleep(0.3)

    def __del__(self):
        self.stop()
        GPIO.cleanup()

    def run(self):
        while True:
            self._update_state()

    def move_start(self, key):
        if (key == "forward"):
            self.go_forward()
        elif (key == "backward"):
            self.go_backward()
        elif (key == "left"):
            self.turn_left()
        elif (key == "right"):
            self.turn_right()

    def move_stop(self):
        self.motor_state[self.motors["right"]] = "stop"
        self.motor_state[self.motors["left"]] = "stop"

    def go_forward(self):
        self.motor_state[self.motors["right"]] = "forward"
        self.motor_state[self.motors["left"]] = "forward"

    def go_backward(self):
        self.motor_state[self.motors["right"]] = "backward"
        self.motor_state[self.motors["left"]] = "backward"

    def turn_left(self):
        self.motor_state[self.motors["right"]] = "forward"
        self.motor_state[self.motors["left"]] = "backward"

    def turn_right(self):
        self.motor_state[self.motors["right"]] = "backward"
        self.motor_state[self.motors["left"]] = "forward"

    def _update_state(self):
        self._set_output("right", self.motor_state[self.motors["right"]])
        self._set_output("left", self.motor_state[self.motors["left"]])

    def _set_output(self, motor, state):
        m = self.motors[motor]
        GPIO.output(self.pins[m][0], self.state[state][0])
        GPIO.output(self.pins[m][1], self.state[state][1])

