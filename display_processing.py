import os
import logging
import json
import requests


class Display:
    def __init__(self):
        if os.path.isfile("config.json") is False:
            logging.error("Файла config.json не существует")
            assert False
        with open('config.json') as config_file:
            self.__img_url = json.load(config_file)["display_snapshot_url"]

    def snapshot(self):
        res = requests.get(self.__img_url, allow_redirects=True, timeout=1)
        print(res)
        open('snapshot.jpg', 'wb').write(res.content)
        return res.status_code









