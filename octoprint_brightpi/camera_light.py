# coding=utf-8
from .brightpilib import *

class CameraLight(object):
    """
    The :class: LightCtrl implements Bright-Pi LED control.
    """

    def __init__(self):
        self.brightPi = BrightPi()
        self.brightPi.reset()

    def white_light_off(self):
        self.brightPi.set_led_on_off(LED_WHITE, OFF)

    def white_light_on(self):
        self.brightPi.set_led_on_off(LED_WHITE, ON)

    def ir_light_off(self):
        self.brightPi.set_led_on_off(LED_IR, OFF)

    def ir_light_on(self):
        self.brightPi.set_led_on_off(LED_IR, ON)
