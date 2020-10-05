# chord_test
Дипломный проект: Стенд автоматизированного тестирования СЗИ НСД "Аккорд-АМДЗ"

## Запуск тестов
Чтобы запустить тесты нужно:

* Создать виртуальное окружение в папке с тестами:
```commandline
python3 -m venv ./venv
```

* Зайти в окружение:
```commandline
source venv/bin/activate
```

* Установить зависимости:
```commandline
pip install -r requirements.txt
```

* Перезапустить окружение:
```commandline
deactivate && source venv/bin/activate
```

* Записать необходимую конфигурационую информацию в `config.json`

* Запустить тесты:
```commandline
pytest
```