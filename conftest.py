import pytest
import logging
import os
import json
import testing_hardware
import time
from Py_Keyboard.HID import Keyboard
from display_processing import Display
from common_funcs import get_test_report_dir
import subprocess
import signal


@pytest.fixture(scope="session", autouse=True)
def test_log():
    test_report_dir = get_test_report_dir()
    command = [
        './tail_logs.sh',
        test_report_dir
    ]

    p = subprocess.Popen(command)

    yield

    subprocess.Popen.terminate(p)
    # os.killpg(os.getpgid(p.pid), signal.SIGTERM)


@pytest.fixture(scope="session")
def display():
    display = Display()
    yield display


@pytest.fixture(scope="session")
def pc(display):
    hardware = testing_hardware.TestingHardware()
    logging.info("Включение питания ПК")
    hardware.power_switch()

    yield hardware

    logging.info("Перезагрузка")
    hardware.reboot(0)

    logging.debug("Задержка 3 секунды")
    time.sleep(3)

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


@pytest.fixture(autouse=True)
def log_test_borders():
    # TODO: Удалить все вызовы фикстуры в тестах
    logging.info("################################## НАЧАЛО ТЕСТА ##################################")
    yield
    logging.info("################################## КОНЕЦ ТЕСТА ###################################")
