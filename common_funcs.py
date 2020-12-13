import logging
import time
from display_processing import Display


def waiting_interrupt_catching(display: Display):
    logging.info("Ожидание перехвата прерывания BIOS")
    for i in range(20):
        if display.interrupt_catching() is True:
            return True
        time.sleep(3)
    return False


def waiting_authentication_req(display: Display):
    logging.info("Ожидание запроса аутентификации")
    for i in range(40):
        if display.authentication() is True:
            return True
        time.sleep(3)
    return False


def waiting_first_setup(display: Display):
    logging.info("Ожидание загрузки меню первичной настройки")
    for i in range(40):
        if display.info_message() is True:
            return True
        time.sleep(3)
    return False


def waiting_for_passed_authentication(display: Display):
    logging.info("Ожидание окна контроля целостности")
    for i in range(2):
        if display.passed_authentication() is True:
            return True
        time.sleep(1)
    return False


def waiting_for_admin_interface(display: Display):
    logging.info("Ожидание интерфейса администрирования без лишних окон")
    for i in range(2):
        if display.admin_interface() is True:
            return True
        time.sleep(2)
    return False

