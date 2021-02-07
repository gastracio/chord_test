import os
import logging
import json
import decimal
import requests
import cv2 as cv
from matplotlib import pyplot as plt
from datetime import datetime
from common_funcs import get_test_report_dir
import numpy as np
import time


# TODO: Вынести все magic numbers в config.json
class Display:
    report_dir = get_test_report_dir()
    __info_message_template = cv.imread('templates/info_message_template.jpg', 0)
    __authentication_template = cv.imread('templates/authentication_template.jpg', 0)
    __passed_authentication_template = cv.imread('templates/passed_authentication_template_1.jpg', 0)
    # TODO: Костыль
    __user_passed_authentication_template = cv.imread('templates/user_passed_authentication_template_1.jpg', 0)
    __interrupt_catching_template = cv.imread('templates/interrupt_catching_template.jpg', 0)
    __message_template = cv.imread('templates/message_template.jpg', 0)
    __admin_interface_template = cv.imread('templates/admin_interface_template.jpg', 0)

    def __init__(self):
        if os.path.isfile("config.json") is False:
            logging.error("Файла config.json не существует")
            assert False
        with open('config.json') as config_file:
            conf = json.load(config_file, parse_float=decimal.Decimal)
            self.__img_url = conf["display_snapshot_url"]
            self.__min_correlation = float(conf["min_correlation"])

        fig, ax = plt.subplots(figsize=(8, 9), dpi=125)
        plt.get_current_fig_manager().window.wm_geometry("+923+35")
        plt.axis("off")
        fig.subplots_adjust(0.010, 0.010, 0.990, 0.990)
        data = np.zeros((1080, 1920))
        self.image_plt = ax.imshow(data)
        # plt.draw()
        # plt.pause(0.05)

    def snapshot(self):
        res = requests.get(self.__img_url, allow_redirects=True, timeout=1)
        if res.status_code != 200:
            assert False
        snapshot_name = 'snapshot_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '.jpg'
        logging.debug(snapshot_name)
        open(self.report_dir + "/" + snapshot_name, 'wb').write(res.content)
        return snapshot_name

    def match_template(self, image_path, template):
        img = cv.imread(image_path, 0)
        img2 = img.copy()
        w, h = template.shape[::-1]

        img = img2.copy()
        method = eval('cv.TM_CCOEFF_NORMED')
        # Apply template Matching
        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        logging.debug("min_val: " + str(min_val) + " max_val: " + str(max_val))
        logging.debug("")
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if max_val > self.__min_correlation:
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

        self.image_plt.set_data(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        plt.draw()
        plt.pause(0.05)

        if max_val > self.__min_correlation:
            return True
        return False

    def info_message(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__info_message_template)

    def authentication(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__authentication_template)

    def interrupt_catching(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__interrupt_catching_template)

    def passed_authentication(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__passed_authentication_template)

    # TODO: Костыль
    def user_passed_authentication(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__user_passed_authentication_template)

    def message(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__message_template)

    def admin_interface(self):
        snapshot_name = self.snapshot()
        return self.match_template(self.report_dir + "/" + snapshot_name, self.__admin_interface_template)

    def waiting_interrupt_catching(self):
        logging.info("Ожидание перехвата прерывания BIOS")
        for i in range(20):
            if self.interrupt_catching() is True:
                return True
            time.sleep(3)
        return False

    def waiting_authentication_req(self):
        logging.info("Ожидание запроса аутентификации")
        for i in range(40):
            if self.authentication() is True:
                return True
            time.sleep(3)
        return False

    def waiting_first_setup(self):
        logging.info("Ожидание загрузки меню первичной настройки")
        for i in range(40):
            if self.info_message() is True:
                return True
            time.sleep(3)
        return False

    def waiting_for_passed_authentication(self):
        logging.info("Ожидание окна контроля целостности")
        for i in range(6):
            if self.passed_authentication() is True:
                return True
            time.sleep(3)
        return False

    # TODO: Костыль
    def waiting_for_user_passed_authentication(self):
        logging.info("Ожидание окна контроля целостности")
        for i in range(6):
            if self.user_passed_authentication() is True:
                return True
            time.sleep(3)
        return False

    def waiting_for_admin_interface(self):
        logging.info("Ожидание интерфейса администрирования без лишних окон")
        for i in range(3):
            if self.admin_interface() is True:
                return True
            time.sleep(2)
        return False

    def waiting_for_message(self):
        logging.info("Ожидание появления сообщения")
        for i in range(3):
            if self.message() is True:
                return True
            time.sleep(2)
        return False
