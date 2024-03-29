[![Build Status](https://travis-ci.com/den1s0v/c_owl.svg?branch=master)](https://travis-ci.com/den1s0v/c_owl)

# Генерация (нет ;-)) и проверка заданий по алгоритмическим структурам при помощи логического вывода на онтологии #
## Приближение 1. Алгоритмические структуры и трасса пошагового исполнения программы (Algorithmic structures and a trace of stepwise program execution)

### Construction of algorithm execution traces and student trace verification #

Status: proof-of-concept prototype.

**Задача**: по данному алгоритму и фрагменту трассы найти все ошибки и сгенерировать понятные человеку объяснения по каждой из них.

(**Task**: find all mistakes using this algorithm and a trace fragment and generate explanations for each of them that are clear to people.)

- note that all the examples (see `handcrafted_traces/\*.txt`) designed in Russian language.

## Технологии (Technologies)

- OWL 2 + SWRL ([tutorial](http://dior.ics.muni.cz/~makub/owl))
- Pellet 2.3 reasoner / Apache Jena / batched SPARQL Update queries / SWI-Prolog + rdf11 lib
- Ontology & rules editor: Stanford Protégé 5.5 ([official docs](http://protegeproject.github.io/protege/class-expression-syntax/), [SWRL docs](https://github.com/protegeproject/swrlapi/wiki))
- [Owlready2 Python library](https://pypi.org/project/Owlready2/) ships with Pellet2 ([docs](https://owlready2.readthedocs.io/))


## Требования (Prerequisites)

- Python 3.6+ (tested on 3.7, 3.9)
- Stanford Protégé 5.5 [optional]

## Установка (Setup)

`pip3 install -r requirements.txt`

## Запуск (Run) веб-сервера Flask

#### Запуск с параметрами по умолчанию:

 `python3 -u web_server.py`

(Или `start-web-server.bat` на Windows)

#### Запуск с указанием хоста и/или порта:

 `python3 -u web_server.py host=109.206.169.214`

 `python3 -u web_server.py port=2020`

 `python3 -u web_server.py host=localhost port=1234`

Небольшое замечание: Включение режима `DEBUG` не вынесено в параметры командной строки, т.к. по умолчанию этот режим активируется только на Windows (см. далее).

### Изменение настроек по умолчанию

В `options.py` можно задать несколько опций, который влияют на работу веб-сервиса, в зависимости от платформы, на которой производится запуск:
- `DEBUG` - `True`: запуск в режиме отладки (медленный development server - включен только на Windows), `False`: используется быстрый кросс-платформенный сервер waitress (зато не показывает ошибки в процессе работы сервера)

- `RUN_LOCALLY` - запускать на localhost (`True`) или в конфигурации для некоторого VDS (`False`).

Порт по умолчанию задан как `2020`, подробнее - см. конец файла `web_server.py`.

### Использование

После запуска веб-сервера на `localhost:2020` становятся доступны несколько страниц:

- `/demo` - Демонстрационная страница, подготовленная для ISWC2020 (может уже не работать корректно)
- `/api_test` - Описание API (пока что 2 запроса) и кнопки для их тестирования
- и др. оговоренные точки доступа.
