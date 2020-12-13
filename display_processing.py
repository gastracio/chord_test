import os
import logging
import json
import requests
import cv2 as cv
from matplotlib import pyplot as plt
from datetime import datetime
import glob


class Display:
    report_dir = "test_report_" + str(max([int(report.split('_')[-1]) for report in glob.glob("test_report_*")]))
    _info_message_template = cv.imread('templates/info_message.jpeg', 0)
    _authentication_template = cv.imread('templates/authentication_template.jpg', 0)
    _interrupt_catching_template = cv.imread('templates/interrupt_catching_template.jpg', 0)

    def __init__(self):
        if os.path.isfile("config.json") is False:
            logging.error("Файла config.json не существует")
            assert False
        with open('config.json') as config_file:
            self.__img_url = json.load(config_file)["display_snapshot_url"]

    def snapshot(self):
        res = requests.get(self.__img_url, allow_redirects=True, timeout=1)
        snapshot_name = 'snapshot_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '.jpg'
        logging.debug(snapshot_name)
        open(self.report_dir + "/" + snapshot_name, 'wb').write(res.content)
        return res.status_code, snapshot_name

    def info_message(self):
        res_code, snapshot_name = self.snapshot()
        if res_code != 200:
            return res_code, False
        return res_code, match_template(self.report_dir + "/" + snapshot_name, self._info_message_template)

    def authentication(self):
        res_code, snapshot_name = self.snapshot()
        if res_code != 200:
            return res_code, False
        return res_code, match_template(self.report_dir + "/" + snapshot_name, self._authentication_template)

    def interrupt_catching(self):
        res_code, snapshot_name = self.snapshot()
        if res_code != 200:
            return res_code, False
        return res_code, match_template(self.report_dir + "/" + snapshot_name, self._interrupt_catching_template)


def match_template(image_path, template):
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
    if max_val > 0.7:
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

    fig, ax = plt.subplots(figsize=(20, 10))
    plt.axis("off")
    axim = ax.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.draw()
    plt.pause(0.05)

    if max_val > 0.9:
        return True
    return False
