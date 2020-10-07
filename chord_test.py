import pytest
import logging
import testing_hardware
import random
import os
import json


# Making pytest parametrize list for all identifiers
if os.path.isfile("config.json") is False:
    logging.error("Файла config.json не существует")
    assert False
with open('config.json') as config_file:
    id_conf = json.load(config_file)["identifiers"]
identifiers_param_list = []
for i in range(len(id_conf)):
    identifiers_param_list.append(pytest.param(i, id=id_conf[i]))


def create_user(keyboard, identifier, identifier_res_time_sec, password):
    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Идентификатор\"")
    logging.info("Выбор пункта \"Использовать существующий\"")
    # TODO Использовать сгенерированный идентификатор
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


def pc_reboot():
    logging.info("Перезагрузка ПК")
    testing_hardware.pc_reboot()

    logging.info("Проверка корректности перехвата прерывания BIOS")

    logging.info("Ожидание начала аутентификации")


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="bios_interrupt_catching", scope="session")
def test_bios_interrupt_catching(log_test_borders):
    logging.info("Начало теста перехвата прерывания BIOS")
    logging.info("Включение питания ПК")
    testing_hardware.pc_power_switch()

    logging.info("Проверка успешности перехвата прерывания")
    # TODO Проверка успешности перехвата прерывания АМДЗ


@pytest.mark.run(order=1)
@pytest.mark.dependency(name="chord_main_admin",
                        scope="session",
                        depends=[
                            "bios_interrupt_catching"
                        ])
@pytest.mark.parametrize("id_number", identifiers_param_list)
def test_chord_main_admin(id_number, keyboard, config, log_test_borders):
    logging.info("Начало теста главного администратора Аккорда с идентификатором " + config["identifiers"][id_number])
    logging.info("Ожидание начала настройки")

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Переход в настройки гл. администратора")

    logging.info("Создание пользователя")
    # TODO Генерация пароля своими силами, либо силами АМДЗ
    password = "12345678"
    create_user(keyboard, config["identifiers"][id_number], config["identifiers_res_time_sec"], password)

    logging.info("Применение настроек")

    pc_reboot()

    logging.info("Считывание неправильного идентификатора")
    incorrect_id_number = random.choice([x for x in range(len(config["identifiers"])) if x != id_number])
    testing_hardware.attach_identifier(config["identifiers"][incorrect_id_number],
                                       config["identifiers_res_time_sec"])

    logging.info("Ввод пароля")
    keyboard.write(password)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Проверка неудачной аутентификации")
    # TODO Проверка неудачной аутентификации
    pc_reboot()

    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(config["identifiers"][id_number], config["identifiers_res_time_sec"])

    logging.info("Ввод неправильного пароля")
    keyboard.write(password + "F")

    logging.info("Проверка неудачной аутентификации")
    # TODO Проверка неудачной аутентификации

    pc_reboot()

    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(config["identifiers"][id_number], config["identifiers_res_time_sec"])

    logging.info("Ввод пароля")
    keyboard.write(password)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Проверка удачной аутентификации аутентификации")

    logging.info("Нажатие на кнопку продолжить загрузку")

    logging.info("Проверка корректности загрузки ОС")


