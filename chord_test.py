import logging
import testing_hardware


def test_chord_init(keyboard, config, log_test_borders):
    logging.info("Начало теста инициализации Аккорда")
    logging.info("Нажатие клавиши enter")
    keyboard.press("ENTER")

    logging.info("Переход в настройки администратора")
    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Идентификатор\"")
    logging.info("Выбор пункта \"Использовать существующий\"")
    logging.info("Нажатие кнопки \"Далее\"")
    logging.info("Считывание идентификатора")

    testing_hardware.attach_identifier(config["identifiers"][0],
                                       config["identifiers_res_time_sec"])

    


