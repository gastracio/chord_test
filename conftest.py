import pytest
import logging
from Py_Keyboard.HID import Keyboard
import os
import json
import testing_hardware


@pytest.fixture(scope="session")
def pc_power():
    logging.info("Включение питания ПК")
    testing_hardware.pc_power_switch()


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
