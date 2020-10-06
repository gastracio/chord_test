import pytest
import logging
import testing_hardware


def create_user(keyboard, identifier, identifier_res_time_sec):
    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Идентификатор\"")
    logging.info("Выбор пункта \"Использовать существующий\"")
    logging.info("Нажатие кнопки \"Далее\"")

    logging.info("Считывание идентификатора")
    testing_hardware.attach_identifier(identifier, identifier_res_time_sec)

    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Нажатие кнопки \"Сменить...\" в поле \"Пароль\"")
    logging.info("Ввод пароля")
    # TODO Генерация пароля своими силами, либо силами АМДЗ
    keyboard.write("12345678")

    logging.info("Повторение пароля пароля")
    keyboard.press("TAB")
    keyboard.write("12345678")

    logging.info("Нажатие кнопки ОК")
    keyboard.press("TAB")
    keyboard.press("TAB")
    keyboard.press("ENTER")

    # TODO Проверка успешности создания пользователя с помощью логов АМДЗ


@pytest.mark.run(order=0)
@pytest.mark.dependency(name="catching_bios_interrupt", scope="session")
def test_catching_bios_interrupt(log_test_borders):
    logging.info("Начало теста перехвата прерывания BIOS")
    logging.info("Включение питания ПК")
    testing_hardware.pc_power_switch()

    logging.info("Проверка успешности перехвата прерывания")
    # TODO Проверка успешности перехвата прерывания АМДЗ


@pytest.mark.run(order=1)
@pytest.mark.dependency(name="chord_init",
                        scope="session",
                        depends=[
                            "catching_bios_interrupt"
                        ])
def test_chord_init(keyboard, config, log_test_borders):
    logging.info("Начало теста инициализации Аккорда")
    logging.info("Нажатие кнопки ОК")
    keyboard.press("ENTER")

    logging.info("Переход в настройки гл. администратора")
    logging.info("Создание пользователя")
    create_user(keyboard, config["identifiers"][0], config["identifiers_res_time_sec"])
    logging.info("Применение настроек")

    logging.info("Перезагрузка ПК")



