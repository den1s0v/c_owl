[![Build Status](https://travis-ci.com/den1s0v/c_owl.svg?branch=master)](https://travis-ci.com/den1s0v/c_owl)

# Генерация и проверка заданий по алгоритмическим структурам при помощи логического вывода на онтологии #
## Приближение 1. Алгоритмические структуры и трасса пошагового исполнения программы (Algorithmic structures and a trace of stepwise program execution)

### Construction of algorithm execution traces and student trace verification #

Status: proof-of-concept prototype.

**Задача**: по данному алгоритму и фрагменту трассы найти все ошибки и сгенерировать понятные человеку объяснения по каждой из них.
(**Task**: find all mistakes using this algorithm and a trace fragment and generate explanations for each of them that are clear to people.)

## Технологии (Technologies)

- OWL 2 + SWRL ([tutorial](http://dior.ics.muni.cz/~makub/owl))
- Pellet 2.3 reasoner
- Ontology & rules editor: Stanford Protégé 5.5 ([official docs](http://protegeproject.github.io/protege/class-expression-syntax/), [SWRL docs](https://github.com/protegeproject/swrlapi/wiki))
- [Owlready2 Python library](https://pypi.org/project/Owlready2/) ships with Pellet2 ([docs](https://owlready2.readthedocs.io/))


## Требования (Prerequisites)

- Python 3.6+ (tested on 3.7)
- Stanford Protégé 5.5 [optional]

## Установка (Setup)

`pip3 install -r requirements.txt`

## Запуск (Run)

 `python3 ctrlstrct_test.py`

- note that all the examples (see handcrafted_traces/\*.txt) designed in Russian language.
