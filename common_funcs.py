import logging
import time
from display_processing import Display


def waiting_interrupt_catching(display: Display):
    logging.info("Ожидание перехвата прерывания BIOS")
    for i in range(20):
        res_code, match_status = display.interrupt_catching()
        if res_code != 200:
            logging.error("Ошибка запроса снимка экрана")
            return False
        if match_status is True:
            return True
        time.sleep(3)

    return False


def wait_authentication_req(display: Display):
    logging.info("Ожидание запроса аутентификации")
    for i in range(40):
        res_code, match_status = display.authentication()
        if res_code != 200:
            logging.error("Ошибка запроса снимка экрана")
            return False
        if match_status is True:
            return True
        time.sleep(3)

    return False


def wait_first_setup(display: Display):
    logging.info("Ожидание загрузки меню первичной настройки")
    for i in range(40):
        res_code, match_status = display.info_message()
        if res_code != 200:
            logging.error("Ошибка запроса снимка экрана")
            return False
        if match_status is True:
            return True
        time.sleep(3)

    return False

