# chord_test
Дипломный проект: Стенд автоматизированного тестирования СЗИ НСД "Аккорд-АМДЗ"

## Описание конфигурационного файла
Конфигурационный файл `config.json` содержит информацию необходимую для 
проведения тестирования.

### Описание полей файла
* `identifiers`: массив, состоящий из параметров идентификаторов:
    * `name`: Имя идентификатора, которое будет отображаться в логах тестов
     и отчете о тестировании
    * `path`: Полный путь до прерывателя USB, на котором находится данный дентификатор
    * `rewritable_key`: Имеет ли идентификатор возможность перезаписи. 
    Возможные значения:
        * `True`
        * `False`
    * `identifier_res_time_sec`: Время, которое требуется идентификатору для того, 
    чтобы произвести передачу необходимой для идентификации информации ПК с момента 
    подачи питания. Единицы измерения секуны (Пример: 1, 2, 0.5, 0.1, 0).
    
    

## Запуск тестов
Перед началом тестирования нужно убедиться, что ПК с помощью которого проводится 
тестирования подключен к питанию и находится в выключенном состоянии.

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