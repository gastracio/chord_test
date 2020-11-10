import RPi.GPIO as GPIO
import time
import logging


class TestingHardware:
    def __init__(self):
        self.reboot_pin = 37
        self.power_pin = 38
        # TODO Установить инициализирующее значение в разомкнутое
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.reboot_pin, GPIO.OUT)
        GPIO.setup(self.power_pin, GPIO.OUT)

    def pc_power_switch(self):
        logging.debug("Нажатие на кнопку подачи питания на АРМ")
        GPIO.output(self.power_pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.power_pin, GPIO.LOW)

    def pc_reboot(self):
        logging.debug("Нажатие на кнопку перезагрузки питания на АРМ")
        GPIO.output(self.reboot_pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.reboot_pin, GPIO.LOW)
        pass

    def __del__(self):
        GPIO.cleanup()
