import pytest
import logging
import random
import os
import json
import time
from id_class import Identifier
from testing_hardware import TestingHardware


# Making pytest parametrize list for all identifiers
if os.path.isfile("config.json") is False:
    logging.error("Файла config.json не существует")
    assert False
with open('config.json') as config_file:
    identifiers_list = [Identifier(id_param) for id_param in json.load(config_file)["identifiers"]]


def wait_authentication_req():
    logging.info("Ожидание запроса аутентификации")


def check_correctness_of_interrupt_catching():
    """
    :return: True or False
    """
    logging.info("Проверка корректности перехвата прерывания BIOS")


def system_reboot(pc: TestingHardware):
    logging.info("Перезагрузка ПК")
    pc.reboot()

    check_correctness_of_interrupt_catching()
    wait_authentication_req()


def apply_settings(keyboard):
    logging.info("Применение настроек")
    keyboard.press("F5")
    time.sleep(1)
    keyboard.press("ENTER")


def check_correctness_of_authentication():
    """
    :return: True of False
    """
    pass


def authentication(identifier: Identifier, password, keyboard):
    """

    :param identifier:
    :param password:
    :param keyboard:
    :return: authentication result
    """
    logging.info("Считывание идентификатора")
    identifier.attach_identifier()
    logging.info("Ввод пароля")
    keyboard.write(password)
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Проверка результата аутентификации")
    return check_correctness_of_authentication()


def create_account(identifier: Identifier, password, keyboard):
    keyboard.press("TAB")
    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Идентификатор\"")
    keyboard.press("SPACE")
    if identifier.rewritable_key:
        logging.info("Выбор пункта \"Сгенерировать новый\"")
        keyboard.press("TAB")
        keyboard.press("TAB")
        keyboard.press("DOWN_ARROW")
        keyboard.press("TAB")
    else:
        logging.info("Выбор пункта \"Использовать существующий\"")
    logging.info("Нажатие кнопки \"Далее\"")
    keyboard.press("ENTER")

    logging.info("Считывание идентификатора")
    identifier.attach_identifier()
    # TODO Проверить корректность присваивания идентификатора (Для кейса использования идентификатора администратора)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")
    keyboard.press("TAB")

    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Пароль\"")
    keyboard.press("SPACE")
    logging.info("Ввод пароля")
    logging.debug("Пароль: " + password)
    keyboard.write(password)

    logging.info("Повторение пароля пароля")
    keyboard.press("TAB")
    keyboard.write(password)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("TAB")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    # TODO Проверка успешности создания пользователя с помощью логов АМДЗ (Для кейса создания пользователя используя
    #  идентификатор Гл.Администратора)


def creating_main_admin(identifier, password, keyboard):
    logging.info("Переход в настройки гл. администратора")
    keyboard.press("ENTER")
    keyboard.press("DOWN_ARROW")
    keyboard.press("TAB")

    logging.info("Создание пользователя")
    create_account(identifier, password, keyboard)


def creating_user(identifier, username, password, keyboard):
    logging.info("Нажатие кномки \"Создание новой учетной записи\"")
    keyboard.press("F1")
    logging.info("Ввод имени пользователя: " + username)
    keyboard.write(username)
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")
    logging.info("Переход в настройки пользователя " + username)
    keyboard.press("TAB")
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
@pytest.mark.dependency(name="config", scope="session")
def test_config(config, log_test_borders):
    logging.info("Начало теста конфигурационного файла")
    if len(config["identifiers"]) < 2:
        logging.error("В конфигурационном файле указано меньше двух идентификаторов")
        assert False

    for identifier in config["identifiers"]:
        if (identifier["rewritable_key"] != "True") and (identifier["rewritable_key"] != "False"):
            logging.error("В конфигурационном файле неправильное значение у поля rewritable_key")
            assert False


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="bios_interrupt_catching", scope="session")
def test_bios_interrupt_catching(pc, log_test_borders):
    logging.info("Начало теста перехвата прерывания BIOS")
    check_correctness_of_interrupt_catching()


@pytest.mark.run(order=1)
@pytest.mark.dependency(name="chord_main_admin",
                        scope="session",
                        depends=[
                            "bios_interrupt_catching",
                            "config"
                        ])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_chord_main_admin(identifier: Identifier, keyboard, pc, clear_db, log_test_borders):
    logging.info("Начало теста главного администратора Аккорда с идентификатором " + identifier.name)

    main_admin_password = generating_password()
    creating_main_admin(identifier, main_admin_password, keyboard)
    apply_settings(keyboard)
    keyboard.press("ENTER")
    system_reboot(pc)

    logging.info("Аутентификация с неправильным идентификатором")
    incorrect_identifier = random.choice([id1 for id1 in identifiers_list if id1 != identifier])
    authentication(incorrect_identifier, main_admin_password, keyboard)
    system_reboot(pc)

    logging.info("Аутентификация с неправильным паролем")
    # TODO Сделать три попытки аутентификации с детектированием события превышения попыток аутентификации
    #  (для кейса проверки неправильных паролей)
    authentication(identifier, main_admin_password + "F", keyboard)
    system_reboot(pc)

    logging.info("Аутентификация главного администратора")
    authentication(identifier, main_admin_password, keyboard)

    logging.info("Нажатие на кнопку \"Продолжить загрузку\"")
    keyboard.press("TAB")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    logging.info("Проверка корректности загрузки ОС")
    system_reboot(pc)

    authentication(identifier, main_admin_password, keyboard)
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")


@pytest.mark.run(order=2)
@pytest.mark.dependency(depends=["chord_main_admin"])
def test_creating_user_with_admin_id(keyboard, pc, clear_db, log_test_borders):
    logging.info("Начало теста создания пользователя с идентификатором главного администратора")

    main_admin_id = random.choice([identifier for identifier in identifiers_list])
    main_admin_password = generating_password()
    creating_main_admin(main_admin_id, main_admin_password, keyboard)
    apply_settings(keyboard)
    system_reboot(pc)

    authentication(main_admin_id, main_admin_password, keyboard)
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    logging.info("Выбор группы \"Обычные\" в дереве учетных записей")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    username = "User"
    user_password = generating_password()
    logging.info("Попытка создать пользователя с идентификатором главного администратора")
    creating_user(main_admin_id, username, user_password, keyboard)
    # TODO Сделать проверку ошибки присваивания неправильного идентификатора
    system_reboot(pc)

    authentication(main_admin_id, main_admin_password, keyboard)
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")


def account_test(identifier: Identifier, pc: TestingHardware, is_admin, keyboard):
    if is_admin:
        logging.info("Начало теста администратора Аккорда с идентификатором " + identifier.name)
    else:
        logging.info("Начало теста пользователя Аккорда с идентификатором " + identifier.name)

    main_admin_id = random.choice([id1 for id1 in identifiers_list if id1 != identifier])
    main_admin_password = generating_password()
    creating_main_admin(main_admin_id, main_admin_password, keyboard)
    if is_admin:
        logging.info("Выбор группы \"Администраторы\" в дереве учетных записей")
        account_name = "Admin"
    else:
        logging.info("Выбор группы \"Обычные\" в дереве учетных записей")
        keyboard.press("DOWN_ARROW")
        keyboard.press("DOWN_ARROW")
        account_name = "User"
    account_password = generating_password()
    creating_user(identifier, account_name, account_password, keyboard)
    apply_settings(keyboard)
    system_reboot(pc)

    logging.info("Аутентификация с неправильным паролем")
    # TODO Делать аутентификацию до тех пор, пока не закроется доступ до администрирования (для кейса с неправильным
    #  паролем)
    authentication(identifier, account_password + "F", keyboard)
    system_reboot(pc)

    if is_admin:
        logging.info("Аутентификация администратора")
    else:
        logging.info("Аутентификация пользователя")
    authentication(identifier, account_password, keyboard)
    logging.info("Нажатие на кнопку \"Продолжить загрузку\"")
    keyboard.press("TAB")
    keyboard.press("TAB")
    keyboard.press("ENTER")
    logging.info("Проверка корректности загрузки ОС")
    system_reboot(pc)

    authentication(main_admin_id, main_admin_password, keyboard)
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")


@pytest.mark.run(order=2)
@pytest.mark.dependency(depends=["chord_main_admin"])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_chord_user(identifier: Identifier, keyboard, pc, clear_db, log_test_borders):
    account_test(identifier, pc, False, keyboard)


@pytest.mark.run(order=2)
@pytest.mark.dependency(depends=["chord_main_admin"])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_chord_admin(identifier: Identifier, keyboard, pc, clear_db, log_test_borders):
    account_test(identifier, pc, True, keyboard)
