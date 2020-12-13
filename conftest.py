import pytest
import logging
import os
import json
import testing_hardware
import time
from Py_Keyboard.HID import Keyboard
from display_processing import Display
from common_funcs import wait_authentication_req


@pytest.fixture(scope="session")
def display():
    display = Display()
    yield display


@pytest.fixture(scope="session")
def pc(display):
    hardware = testing_hardware.TestingHardware()
    logging.info("Включение питания ПК")
    hardware.power_switch()
    # TODO Сделать обратную связь из графического интерфейса о загрузке ОС Аккорда
    wait_authentication_req(display)
    # logging.debug("Задержка 15 секунд")
    # time.sleep(15)
    yield hardware
    logging.info("Перезагрузка")
    hardware.reboot(0)

    logging.debug("Задержка 2 секунды")
    time.sleep(2)

    logging.info("Выключение питания")
    hardware.power_switch(0)


@pytest.fixture(scope="session")
def keyboard():
    keyboard = Keyboard("/dev/hidg0")
    yield keyboard


@pytest.fixture(scope="session")
def config():
    if os.path.isfile("config.json") is False:
        logging.error("Файла config.json не существует")
        assert False
    with open('config.json') as config_file:
        yield json.load(config_file)


@pytest.fixture()
def log_test_borders():
    logging.info("################################## НАЧАЛО ТЕСТА ##################################")
    yield
    logging.info("################################## КОНЕЦ ТЕСТА ###################################")
