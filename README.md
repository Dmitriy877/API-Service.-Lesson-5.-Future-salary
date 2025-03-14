# Получение средних зарплат с сайтов Head Hunter и Super Job в зависимости от языка программирования

get_average_salary.py Данный скрипт выводит на экран таблицу с указанием языков программирования и средней зарплаты специалистов с сайтов Head Hunter и Super Job.

Для работы необходимо запустить скрипт в консоли, например: 

```python get_average_salary.py ```

Скрипты содержат следующие переменные:

`super_job_api_key` - переменная которая хранит ключ SUPER_JOB_SECRET_KEY, импортированный из .env файла (Необходимы для работы API Super Job).

### Как установить

Python3 должен быть установлен.
Затем используйте "pip" (или "pip3", есть конфлик с python2) для устанвки зависимостей:

```python
pip install -r requerements.txt
```

Перед запуском необходимо создать .env файл где разместить ключ SUPER_JOB_SECRET_KEY в переменной `SUPER_JOB_SECRET_KEY` 
Рекомендуется использовать [vitrualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.

### Как запустить

Для запуска скриптов убедитесь что вложили в папку с скриптом файл .env с переменной `SUPER_JOB_SECRET_KEY` и передали в данную переменную соответсвующий ключ.
Для выведения информации по дополнительным языкам программирования дополните список `languages` в скрипте `python get_average_salary.py` (можно открыть блокнотом).

Например:

* Откройте консоль
* Перейдите в консоли в папку с скриптом , например:

```python
cd ./Documents/GitHub/API-Service.-Lesson-5.-Future-salary
```

* введите в консоль команду запуска скрипта:

```python
python get_average_salary.py 
```

* Произойдет выведение на экран 2 таблиц со средними зарплатами по вакансиям специалистов различных языков в зависимости от сайта вакансий (Head Hunter и Super Job)

ВНИМАНИЕ: ИНОГДА САЙТЫ БЛОКИРУЮТ РАБОТЫ СКРИПТА, ИЗ ЗА СЛИШКОМ БОЛЬШОГО КОЛИЧЕСТВА ЗАПРОСОВ К НИМ СО СТОРОНЫ СКРИПТА

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/)