import time
import logging


class Identifier:
    def __init__(self, id_param):
        """

        :param id_param: Identifier parameters dict from config.json
        """
        self.name = id_param["name"]
        self.path = id_param["path"]
        if id_param["rewritable_key"] == "True":
            self.rewritable_key = True
        else:
            self.rewritable_key = False

        self.response_time = id_param["identifier_res_time_sec"]

    def attach_identifier(self):
        logging.debug("Подключение идентификатора " + self.name)
        time.sleep(self.response_time)
        logging.debug("Отключение идентификатора " + self.name)



