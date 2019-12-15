# Генерация заданий по языку С при помощи онтологии #
### Making quiz on С programming language with ontology #

Статус: начало исследований

## Приближение 1. Алгоритмические структуры и трасса пошагового исполнения программы

**Задача**: по данному алгоритму и фрагменту трассы найти все ошибки и сгенерировать понятные человеку объяснения по каждой из них.

## Технологии

- OWL 2 + SWRL ([tutorial](http://dior.ics.muni.cz/~makub/owl))
- Pellet 2+ reasoner
- Ontology & rules editor: Protege 5.5 ([official docs](http://protegeproject.github.io/protege/class-expression-syntax/), [SWRL docs](https://github.com/protegeproject/swrlapi/wiki))
- [?] Stardog knoledge base ([?] SPARQL endpoint)
- [Owlready2 Python library](https://pypi.org/project/Owlready2/) ships with Pellet2 ([docs](https://owlready2.readthedocs.io/))


