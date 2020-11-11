import RPi.GPIO as GPIO
import time
import logging


class TestingHardware:
    def __init__(self):
        self.__reboot_pin = 37
        self.__power_pin = 38
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.__reboot_pin, GPIO.OUT)
        GPIO.output(self.__reboot_pin, GPIO.HIGH)

        GPIO.setup(self.__power_pin, GPIO.OUT)
        GPIO.output(self.__power_pin, GPIO.HIGH)

    def power_switch(self):
        logging.debug("Нажатие на кнопку подачи питания на АРМ")
        GPIO.output(self.__power_pin, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(self.__power_pin, GPIO.HIGH)

    def reboot(self):
        logging.debug("Нажатие на кнопку перезагрузки питания на АРМ")
        GPIO.output(self.__reboot_pin, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(self.__reboot_pin, GPIO.HIGH)

    def __del__(self):
        GPIO.cleanup()
