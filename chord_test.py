import pytest
import logging
import testing_hardware


def create_user(keyboard, identifier, identifier_res_time_sec, password):
    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Идентификатор\"")
    logging.info("Выбор пункта \"Использовать существующий\"")
    logging.info("Нажатие кнопки \"Далее\"")

    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(identifier, identifier_res_time_sec)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Пароль\"")
    logging.info("Ввод пароля")
    keyboard.write(password)

    logging.info("Повторение пароля пароля")
    keyboard.press("TAB")
    keyboard.write(password)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("TAB")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    # TODO Проверка успешности создания пользователя с помощью логов АМДЗ


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="bios_interrupt_catching", scope="session")
def test_bios_interrupt_catching(log_test_borders):
    logging.info("Начало теста перехвата прерывания BIOS")
    logging.info("Включение питания ПК")
    testing_hardware.pc_power_switch()

    logging.info("Проверка успешности перехвата прерывания")
    # TODO Проверка успешности перехвата прерывания АМДЗ


@pytest.mark.run(order=1)
@pytest.mark.dependency(name="chord_init",
                        scope="session",
                        depends=[
                            "bios_interrupt_catching"
                        ])
def test_chord_init(keyboard, config, log_test_borders):
    logging.info("Начало теста инициализации Аккорда")
    logging.info("Ожидание начала настройки")

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Переход в настройки гл. администратора")

    logging.info("Создание пользователя")
    # TODO Генерация пароля своими силами, либо силами АМДЗ
    password = "12345678"
    create_user(keyboard, config["identifiers"][0], config["identifiers_res_time_sec"], password)

    logging.info("Применение настроек")

    logging.info("Перезагрузка ПК")
    testing_hardware.pc_reboot()

    logging.info("Ожидание начала аутентификации")

    for i in range(1, len(config["identifiers"])):
        logging.info("Считывание неправильного идентификатора")
        testing_hardware.attach_identifier(config["identifiers"][i], config["identifiers_res_time_sec"])

        logging.info("Ввод пароля")
        keyboard.write(password)

        logging.info("Нажатие кнопки ОК")
        keyboard.press("ENTER")

        logging.info("Проверка неудачной аутентификации")
        # TODO Проверка неудачной аутентификации

    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(config["identifiers"][0], config["identifiers_res_time_sec"])

    logging.info("Ввод пароля")
    keyboard.write(password)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Проверка удачной аутентификации аутентификации")

    logging.info("Переход в режим администрирования")
