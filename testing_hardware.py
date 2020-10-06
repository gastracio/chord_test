import logging
import time


def attach_identifier(identifier: str, sleep_time):
    """
    USB interrupter management function
    :param identifier: USB interrupter path
    :param sleep_time: Identifier boot and response time.
    :return:
    """
    logging.debug("Подключение идентификатора " + identifier)
    time.sleep(sleep_time)
    logging.debug("Отключение идентификатора " + identifier)
