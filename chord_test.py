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


def create_account(identifier, password, keyboard):
    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Идентификатор\"")
    logging.info("Выбор пункта \"Использовать существующий\"")
    # TODO Использовать сгенерированный идентификатор
    logging.info("Нажатие кнопки \"Далее\"")

    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(identifier)

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


def check_correctness_of_interrupt_catching():
    """
    :return: True or False
    """
    logging.info("Проверка корректности перехвата прерывания BIOS")
    logging.info("Ожидание запроса аутентификации")


def system_reboot():
    logging.info("Перезагрузка ПК")
    testing_hardware.pc_reboot()

    check_correctness_of_interrupt_catching()


def check_correctness_of_authentication():
    """
    :return: True of False
    """
    pass


def authentication(identifier, password, keyboard):
    """

    :param identifier:
    :param password:
    :param keyboard:
    :param expected_auth_res:  Expected authentication result. Need for tests.
    :return:
    """
    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(identifier)
    logging.info("Ввод пароля")
    keyboard.write(password)
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Проверка удачной аутентификации")
    return check_correctness_of_authentication()


def creating_main_admin(identifier, password, keyboard):
    logging.info("Переход в настройки гл. администратора")
    keyboard.press("ENTER")
    logging.info("Создание пользователя")
    create_account(identifier, password, keyboard)


def creating_user(identifier, username, password, keyboard):
    logging.info("Нажатие кномки \"Создание новой учетной записи\"")
    logging.info("Ввод имени пользователя: " + username)
    keyboard.write(username)
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")
    logging.info("Переход в настройки пользователя " + username)
    create_account(identifier, password, keyboard)


def generating_password():
    # TODO Генерация пароля своими силами, либо силами АМДЗ
    return "12345678"


@pytest.fixture()
def clear_db(keyboard):
    yield
    logging.info("Очитска базы данных")
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")
    check_correctness_of_interrupt_catching()


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="bios_interrupt_catching", scope="session")
def test_bios_interrupt_catching(log_test_borders):
    logging.info("Начало теста перехвата прерывания BIOS")
    logging.info("Включение питания ПК")
    testing_hardware.pc_power_switch()
    check_correctness_of_interrupt_catching()


@pytest.mark.run(order=1)
@pytest.mark.dependency(name="chord_main_admin",
                        scope="session",
                        depends=[
                            "bios_interrupt_catching"
                        ])
@pytest.mark.parametrize("id_number", identifiers_param_list)
def test_chord_main_admin(id_number, keyboard, config, clear_db, log_test_borders):
    logging.info("Начало теста главного администратора Аккорда с идентификатором " + config["identifiers"][id_number])

    main_admin_password = generating_password()
    creating_main_admin(config["identifiers"][id_number], main_admin_password, keyboard)
    logging.info("Применение настроек")
    system_reboot()

    logging.info("Аутентификация с неправильным идентификатором")
    incorrect_id_number = random.choice([x for x in range(len(config["identifiers"])) if x != id_number])
    authentication(config["identifiers"][incorrect_id_number], main_admin_password, keyboard)
    system_reboot()

    logging.info("Аутентификация с неправильным паролем")
    authentication(config["identifiers"][id_number], main_admin_password + "F", keyboard)
    system_reboot()

    logging.info("Аутентификация главного администратора")
    authentication(config["identifiers"][id_number], main_admin_password, keyboard)

    logging.info("Нажатие на кнопку \"Продолжить загрузку\"")
    logging.info("Проверка корректности загрузки ОС")

    system_reboot()
    authentication(config["identifiers"][id_number], main_admin_password, keyboard)
    logging.info("Нажатие на кнопку \"Администрирование\"")


@pytest.mark.run(order=2)
@pytest.mark.dependency(depends=["chord_main_admin"])
@pytest.mark.parametrize("id_number", identifiers_param_list)
def test_chord_user(id_number, keyboard, config, clear_db, log_test_borders):
    logging.info("Начало теста пользователя Аккорда с идентификатором " + config["identifiers"][id_number])

    main_admin_id_number = random.choice([x for x in range(len(config["identifiers"])) if x != id_number])
    main_admin_password = generating_password()
    creating_main_admin(config["identifiers"][main_admin_id_number], main_admin_password, keyboard)
    logging.info("Выбор группы \"Обычные\" в дереве учетных записей")
    username = "User"
    user_password = generating_password()
    creating_user(config["identifiers"][id_number], username, user_password, keyboard)
    logging.info("Применение настроек")
    system_reboot()

    logging.info("Аутентификация пользователя")
    authentication(config["identifiers"][id_number], user_password, keyboard)
    logging.info("Нажатие на кнопку \"Продолжить загрузку\"")
    logging.info("Проверка корректности загрузки ОС")


