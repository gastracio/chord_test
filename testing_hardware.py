import logging
import time
import os
import json


# Making pytest parametrize list for all identifiers
if os.path.isfile("config.json") is False:
    logging.error("Файла config.json не существует")
    assert False
with open('config.json') as config_file:
    config = json.load(config_file)


def attach_identifier(identifier: str):
    """
    USB interrupter management function
    :param identifier: USB interrupter path
    :return:
    """
    logging.debug("Подключение идентификатора " + identifier)
    time.sleep(config["identifiers_res_time_sec"])
    logging.debug("Отключение идентификатора " + identifier)


def pc_power_switch():
    pass


def pc_reboot():
    pass


