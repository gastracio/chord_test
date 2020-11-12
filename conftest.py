import pytest
import logging
import os
import json
import testing_hardware
import time
from Py_Keyboard.HID import Keyboard
from display_processing import Display


@pytest.fixture(scope="session")
def pc():
    hardware = testing_hardware.TestingHardware()
    logging.info("Включение питания ПК")
    hardware.power_switch()
    # TODO Сделать обратную связь из графического интерфейса о загрузке ОС Аккорда
    # time.sleep(20)
    yield hardware


@pytest.fixture(scope="session")
def keyboard():
    keyboard = Keyboard("/dev/hidg0")
    yield keyboard


@pytest.fixture(scope="session")
def display():
    display = Display()
    yield display


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
