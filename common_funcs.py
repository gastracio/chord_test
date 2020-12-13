import logging
import time
from display_processing import Display


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



