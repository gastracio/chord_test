import pytest
import logging
from Py_Keyboard.HID import Keyboard
import os
import json


@pytest.fixture(scope="session")
def keyboard():
    # TODO Add linux gadget hid device
    file = open('keyboard.txt', 'w+')
    file.close()
    keyboard = Keyboard("keyboard.txt")
    yield keyboard


@pytest.fixture(scope="session")
def config():
    if os.path.isfile("config.json") is False:
        logging.error("There is no config.json file")
        assert False
    with open('config.json') as config_file:
        yield json.load(config_file)


@pytest.fixture()
def log_test_borders():
    logging.info("################################## НАЧАЛО ТЕСТА ##################################")
    yield
    logging.info("################################## КОНЕЦ ТЕСТА ###################################")
