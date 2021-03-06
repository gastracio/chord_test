import pytest
import logging
import random
import os
import json
import time
from id_class import Identifier
from display_processing import Display
from testing_hardware import ChordTestHardware
from smartcard.System import readers
from Py_Keyboard.HID import Keyboard
import common_funcs

# TODO: Сделать выполнение этого кода после прохождения теста на конфигурационный файл
# Making pytest parametrize list for all identifiers
if os.path.isfile("config.json") is False:
    logging.error("Файла config.json не существует")
    assert False
with open('config.json') as config_file:
    identifiers_list = [Identifier(id_param) for id_param in json.load(config_file)["identifiers"]]


def check_correctness_of_interrupt_catching(display: Display):
    """
    :return: True or False
    """
    logging.info("Проверка корректности перехвата прерывания BIOS")
    return display.waiting_interrupt_catching()


def system_reboot(pc: ChordTestHardware, display: Display):
    logging.info("Перезагрузка ПК")
    pc.reboot()

    res = check_correctness_of_interrupt_catching(display)
    if res is False:
        return False

    res = display.waiting_authentication_req()
    if res is False:
        return False

    return True


def apply_settings(keyboard, display):
    logging.info("Применение настроек")
    keyboard.press("F5")
    res = display.waiting_for_message()
    if res is False:
        return False
    keyboard.press("ENTER")
    time.sleep(1.5)
    return True


def check_correctness_of_authentication(display: Display, is_admin=True):
    # TODO: Сделать корректную обработку ошибки
    if is_admin:
        return display.waiting_for_passed_authentication()
    else:
        return display.waiting_for_user_passed_authentication()


def authentication(identifier: Identifier, password, keyboard, display: Display, is_admin=True):
    logging.info("Считывание идентификатора")
    identifier.attach_identifier()
    logging.info("Ввод пароля")
    keyboard.write(password)
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Проверка результата аутентификации")
    return check_correctness_of_authentication(display, is_admin)


def changing_identifier(identifier, keyboard, display):
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
    try:
        logging.info("Проверка на наличие сообщений об ошибке")
        if display.message() is True:
            return False
    except Exception as e:
        logging.error(e)
        return False

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")


def create_account(identifier: Identifier, password, keyboard, display: Display):
    keyboard.press("TAB")

    res = changing_identifier(identifier, keyboard, display)
    if res is False:
        return False

    keyboard.press("TAB")

    try:
        logging.info("Проверка на корректный выход в меню администрирования")
        if display.admin_interface() is False:
            # TODO: Написать ошибку в логи
            return False
    except Exception as e:
        logging.error(e)
        return False

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

    try:
        logging.info("Проверка на корректный выход в меню администрирования")
        if display.admin_interface() is False:
            return False
    except Exception as e:
        logging.error(e)
        return False

    return True


def creating_main_admin(identifier, password, keyboard, display):
    logging.info("Переход в настройки гл. администратора")
    keyboard.press("DOWN_ARROW")
    keyboard.press("TAB")

    logging.info("Создание пользователя")
    return create_account(identifier, password, keyboard, display)


def creating_user(identifier, username, password, keyboard, display):
    logging.info("Нажатие кномки \"Создание новой учетной записи\"")
    keyboard.press("F1")
    logging.info("Ввод имени пользователя: " + username)
    keyboard.write(username)
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")
    logging.info("Переход в настройки пользователя " + username)
    keyboard.press("TAB")
    return create_account(identifier, password, keyboard, display)


def generating_password():
    return "12345678"


@pytest.fixture()
def clear_db(keyboard, display):
    # TODO: Перенести эту фикстуру в conftes.py
    yield
    logging.info("Очитска базы данных")
    keyboard.press("F6")

    res = display.waiting_for_message()
    if res is False:
        assert False

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    res = display.waiting_for_message()
    if res is False:
        assert False

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    # TODO: Вынести это в отдельную функцию вместе с system_reboot
    res = check_correctness_of_interrupt_catching(display)
    if res is False:
        assert False

    res = display.waiting_first_setup()
    if res is False:
        assert False


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="config", scope="session")
def test_config(config):
    logging.info("Начало теста конфигурационного файла")
    # TODO: Добавить проверки на наличие всех необходимых полей в конфигурационном файле
    # TODO: Добавить проверку на наличие идентификатора, типа TM в конфигурационном файле
    if len(config["identifiers"]) < 2:
        logging.error("В конфигурационном файле указано меньше двух идентификаторов")
        assert False

    for identifier in config["identifiers"]:
        if (identifier["rewritable_key"] != "True") and (identifier["rewritable_key"] != "False"):
            logging.error("В конфигурационном файле неправильное значение у поля rewritable_key")
            assert False


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="video_grabber", scope="session")
def test_video_grabber(display):
    logging.info("Начало теста устройства захвата видео")
    logging.info("Попытка сделать скриншон экрана")
    try:
        display.snapshot()
    except Exception as e:
        logging.error("Устройство захвата видео отсоединено или работает не корректно")
        logging.error(e)
        assert False


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="interrupter", scope="session")
def test_interrupters():
    logging.info("Начало теста прерывателей USB")
    readers_list = readers()
    if len(readers_list) < 2:
        logging.error("К стенду подключено меньше двух прерывателей")
        assert False

    interrupters_paths = [identifier.path for identifier in identifiers_list]
    reader_names = [reader.name for reader in readers_list]
    for interrupter in interrupters_paths:
        if interrupter not in reader_names:
            logging.error("Указанный в конфигурационном файле идентификатор не подключен к стенду")
            logging.debug("Данный прерыватель не подключен к стенду" + interrupter)


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="bios_interrupt_catching", scope="session")
def test_bios_interrupt_catching(pc, display):
    logging.info("Начало теста перехвата прерывания BIOS")
    res = check_correctness_of_interrupt_catching(display)
    if res is False:
        logging.error("Ошибка перехвата прерывания BIOS")
        assert False


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="bios_interrupt_catching", scope="session")
def test_setup_in_first_boot(pc, display):
    logging.info("Начало теста попадания в меню конфигурации при первой загрузке")
    res = display.waiting_first_setup()
    if res is False:
        logging.error("Ошибка, не появился экран первичной настройки")
        assert False


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="keyboard_connecting",
                        scope="session",
                        depends=[
                            "bios_interrupt_catching"
                        ])
def test_keyboard_connecting(pc):
    logging.info("Начало теста проверки соединения для эмуляции клавиатуры")
    error_fl = False
    try:
        logging.info("Попытка провести инициализацию модуля эмуляции клавиатуры")
        Keyboard("/dev/hidg0")
    except Exception as e:
        logging.error("Проблема при инициализации модуля эмуляции клавиатуры")
        logging.error(e)
        logging.info("Проверьте шнур USB type C -- USB, который используется для эмуляции клавиатуры")
        error_fl = True

    if error_fl:
        assert False


@pytest.mark.run(order=1)
@pytest.mark.dependency(name="chord_main_admin",
                        scope="session",
                        depends=[
                            "bios_interrupt_catching",
                            "keyboard_connecting",
                            "video_grabber",
                            "interrupter",
                            "config"
                        ])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_chord_main_admin(identifier: Identifier, keyboard, pc, display, clear_db):
    # TODO: Проверить на соответствие ПМИ
    logging.info("Начало теста главного администратора Аккорда с идентификатором " + identifier.name)

    keyboard.press("ENTER")
    main_admin_password = generating_password()
    assert creating_main_admin(identifier, main_admin_password, keyboard, display)
    apply_settings(keyboard, display)
    keyboard.press("ENTER")
    assert system_reboot(pc, display)

    logging.info("Аутентификация с незарегистрированным идентификатором")
    incorrect_identifier = random.choice([id1 for id1 in identifiers_list if id1 != identifier])
    assert not authentication(incorrect_identifier, main_admin_password, keyboard, display)
    assert system_reboot(pc, display)

    logging.info("Аутентификация с неправильным паролем")
    assert not authentication(identifier, main_admin_password + "F", keyboard, display)
    assert system_reboot(pc, display)

    logging.info("Аутентификация главного администратора")
    assert authentication(identifier, main_admin_password, keyboard, display)

    logging.info("Нажатие на кнопку \"Продолжить загрузку\"")
    keyboard.press("TAB")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    logging.info("Проверка корректности загрузки ОС")
    assert system_reboot(pc, display)

    assert authentication(identifier, main_admin_password, keyboard, display)
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    try:
        display.waiting_for_admin_interface()
    except Exception as e:
        logging.error(e)
        assert False


def use_main_admin_id_in_other_users(identifier: Identifier, is_admin, keyboard, pc, display: Display):
    if is_admin:
        logging.info("Начало теста создания администратора с идентификатором главного администратора " +
                     identifier.name)
    else:
        logging.info("Начало теста создания пользователя с идентификатором главного администратора " +
                     identifier.name)

    keyboard.press("ENTER")
    main_admin_password = generating_password()
    res = creating_main_admin(identifier, main_admin_password, keyboard, display)
    if res is False:
        return False
    apply_settings(keyboard, display)

    user_password = generating_password()
    if is_admin:
        logging.info("Выбор группы \"Администраторы\" в дереве учетных записей")
        username = "Admin"
        logging.info("Попытка создать администратора с идентификатором главного администратора")
    else:
        logging.info("Выбор группы \"Обычные\" в дереве учетных записей")
        keyboard.press("DOWN_ARROW")
        keyboard.press("DOWN_ARROW")
        username = "User"
        logging.info("Попытка создать пользователя с идентификатором главного администратора")
    res = creating_user(identifier, username, user_password, keyboard, display)
    if res is not False:
        return False

    res = system_reboot(pc, display)
    if res is False:
        return False

    res = authentication(identifier, main_admin_password, keyboard, display)
    if res is False:
        return False
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")
    return True


@pytest.mark.run(order=2)
@pytest.mark.dependency(name="creating_user_with_main_admin_id", depends=["chord_main_admin"])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_creating_user_with_main_admin_id(identifier: Identifier, keyboard, pc, display, clear_db):
    assert use_main_admin_id_in_other_users(identifier, False, keyboard, pc, display)


@pytest.mark.run(order=2)
@pytest.mark.dependency(name="creating_admin_with_main_admin_id", depends=["creating_user_with_main_admin_id"])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_creating_admin_with_main_admin_id(identifier: Identifier, keyboard, pc, display, clear_db):
    assert use_main_admin_id_in_other_users(identifier, True, keyboard, pc, display)


def account_test(identifier: Identifier, pc: ChordTestHardware, config, keyboard, display: Display):
    # TODO: Проверить на соответствие ПМИ
    if config == "admin":
        logging.info("Начало теста администратора Аккорда с идентификатором " + identifier.name)
    elif config == "user":
        logging.info("Начало теста пользователя Аккорда с идентификатором " + identifier.name)
    elif config == "group":
        logging.info("Начало теста пользователя группы Аккорда с идентификатором " + identifier.name)
    else:
        assert False

    keyboard.press("ENTER")
    main_admin_id = random.choice([id1 for id1 in identifiers_list if id1 != identifier])
    main_admin_password = generating_password()
    assert creating_main_admin(main_admin_id, main_admin_password, keyboard, display)
    apply_settings(keyboard, display)

    if config == "admin":
        logging.info("Выбор группы \"Администраторы\" в дереве учетных записей")
        account_name = "Admin"
    elif config == "user":
        logging.info("Выбор группы \"Обычные\" в дереве учетных записей")
        keyboard.press("DOWN_ARROW")
        keyboard.press("DOWN_ARROW")
        account_name = "User"
    else:
        logging.info("Добавить группу USERS")
        keyboard.press("F3")
        keyboard.write("users")
        keyboard.press("ENTER")
        assert display.waiting_for_message()
        keyboard.press("ENTER")

        logging.info("Выбор группы \"USERS\" в дереве учетных записей")
        keyboard.press("DOWN_ARROW")
        keyboard.press("DOWN_ARROW")
        keyboard.press("DOWN_ARROW")
        account_name = "User"

    account_password = generating_password()
    assert creating_user(identifier, account_name, account_password, keyboard, display)
    apply_settings(keyboard, display)
    assert system_reboot(pc, display)

    if config == "admin":
        logging.info("Аутентификация администратора")
        assert authentication(identifier, account_password, keyboard, display)
    else:
        logging.info("Аутентификация пользователя")
        assert authentication(identifier, account_password, keyboard, display, False)
    # TODO: Проверка корректности загрузки ОС
    # logging.info("Нажатие на кнопку \"Продолжить загрузку\"")
    # keyboard.press("TAB")
    # keyboard.press("TAB")
    # keyboard.press("ENTER")
    # logging.info("Проверка корректности загрузки ОС")
    assert system_reboot(pc, display)

    logging.info("Аутентификация главным администратором")
    assert authentication(main_admin_id, main_admin_password, keyboard, display)
    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")
    # TODO: Сделать обратную связь из GUI


@pytest.mark.run(order=2)
@pytest.mark.dependency(name="chord_user", depends=["creating_admin_with_main_admin_id"])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_chord_user(identifier: Identifier, keyboard, display, pc, clear_db):
    try:
        account_test(identifier, pc, "admin", keyboard, display)
    except AssertionError:
        assert False
    except Exception as e:
        logging.error(e)
        assert False


@pytest.mark.run(order=2)
@pytest.mark.dependency(name="chord_admin", depends=["chord_user"])
@pytest.mark.parametrize("identifier",
                         [pytest.param(identifier, id=identifier.name) for identifier in identifiers_list])
def test_chord_admin(identifier: Identifier, keyboard, display, pc, clear_db):
    try:
        account_test(identifier, pc, "user", keyboard, display)
    except AssertionError:
        assert False
    except Exception as e:
        logging.error(e)
        assert False


@pytest.mark.run(order=2)
@pytest.mark.dependency(name="user_group", dpends=["chord_admin"])
def test_user_group(keyboard, pc, display, clear_db):
    identifier = random.choice([id1 for id1 in identifiers_list])
    try:
        account_test(identifier, pc, "group", keyboard, display)
    except AssertionError:
        assert False
    except Exception as e:
        logging.error(e)
        assert False


def set_id_page(id_page: int, keyboard, display):
    if id_page < 0 or id_page > 255:
        return False

    logging.info("Переход в настройки")
    keyboard.press("SHIFT TAB")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("ENTER")

    logging.info("Установка значения " + str(id_page) + " \"Станица идентификатора\"")
    keyboard.press("TAB")
    keyboard.write(str(id_page))

    logging.info("Применение настроек")
    keyboard.press("F2")
    res = display.waiting_for_message()
    if res is False:
        return False

    logging.info("Нажатие кнопки OK")
    keyboard.press("ENTER")

    logging.info("Переход обратно в настройки пользователей")
    keyboard.press("SHIFT TAB")
    keyboard.press("UP_ARROW")
    keyboard.press("UP_ARROW")
    keyboard.press("UP_ARROW")
    keyboard.press("UP_ARROW")
    keyboard.press("UP_ARROW")
    keyboard.press("UP_ARROW")
    keyboard.press("ENTER")
    keyboard.press("TAB")

    return True


def touch_memory_sub_test(main_admin_id,
                          main_admin_password,
                          identifier,
                          account_password,
                          keyboard,
                          pc,
                          display):
    logging.info("Проверка невозможности аутентификации пользователя")
    assert not authentication(identifier, account_password, keyboard, display, False)
    assert system_reboot(pc, display)

    logging.info("Аутентификация главного администратора")
    assert authentication(main_admin_id, main_admin_password, keyboard, display)

    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    logging.info("Переход в настройки пользователя")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")
    keyboard.press("TAB")

    logging.info("Смена идентификатора пользователя на тот же самый с генерацией")
    keyboard.press("TAB")
    assert changing_identifier(identifier, keyboard, display)
    assert apply_settings(keyboard, display)
    assert system_reboot(pc, display)

    logging.info("Аутентификация пользователя")
    assert authentication(identifier, account_password, keyboard, display, False)
    assert system_reboot(pc, display)

    logging.info("Аутентификация главного администратора")
    assert authentication(main_admin_id, main_admin_password, keyboard, display)

    logging.info("Нажатие на кнопку \"Администрирование\"")
    keyboard.press("TAB")
    keyboard.press("ENTER")


@pytest.mark.run(order=2)
@pytest.mark.dependency(name="touch_memory", dpends=["user_group"])
def test_touch_memory(keyboard, pc, display):
    identifier = random.choice([id1 for id1 in identifiers_list])
    logging.info("Начало теста с идентификатором TM: " + identifier.name)

    # TODO: Использовать идентификатор, типа ТМ
    keyboard.press("ENTER")
    main_admin_id = random.choice([id1 for id1 in identifiers_list if id1 != identifier])
    main_admin_password = generating_password()
    assert creating_main_admin(main_admin_id, main_admin_password, keyboard, display)
    assert apply_settings(keyboard, display)

    # TODO: Сделать проверку в config.json на наличие TM идентификаторов

    logging.info("Выбор группы \"Обычные\" в дереве учетных записей")
    keyboard.press("DOWN_ARROW")
    keyboard.press("DOWN_ARROW")

    account_name = "User"
    account_password = generating_password()
    assert creating_user(identifier, account_name, account_password, keyboard, display)
    assert apply_settings(keyboard, display)

    assert set_id_page(1, keyboard, display)

    logging.info("Заново устанавливаем идентификатор и пароль для главного администратора")
    keyboard.press("UP_ARROW")
    keyboard.press("UP_ARROW")
    assert creating_main_admin(main_admin_id, main_admin_password, keyboard, display)
    assert apply_settings(keyboard, display)
    assert system_reboot(pc, display)

    try:
        touch_memory_sub_test(main_admin_id, main_admin_password,
                              identifier, account_password,
                              keyboard, pc, display)
    except AssertionError:
        assert False
    except Exception as e:
        logging.error(e)
        assert False

    assert set_id_page(0, keyboard, display)

    logging.info("Заново устанавливаем идентификатор и пароль для главного администратора")
    assert creating_main_admin(main_admin_id, main_admin_password, keyboard, display)
    assert apply_settings(keyboard, display)
    assert system_reboot(pc, display)

    try:
        touch_memory_sub_test(main_admin_id, main_admin_password,
                              identifier, account_password,
                              keyboard, pc, display)
    except AssertionError:
        assert False
    except Exception as e:
        logging.error(e)
        assert False

# TODO: Поменять входное состояние перед всеми тестами на выключенный ПК
