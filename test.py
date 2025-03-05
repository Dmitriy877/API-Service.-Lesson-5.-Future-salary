import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable
from time import sleep

salary_super_job = {}
languages = [
        "GO",
        "Python"
    ]
title_super_job = "SuperJob Moscow"

for language in languages:
    salary_super_job[language] = {
            "vacancy_found": language,
            "processed_salary": language,
            "average_salary": language,
            }


def make_table_salary_statisctis(it_spheres_vacancy, title):
    table_data = [
          [
           "Язык программирования",
           "Вакансий найдено",
           "Вакансий обработано",
           "Средняя зарплата"
          ]
    ]
    for it_sphere, statistics in it_spheres_vacancy.items():
        table_data.append([
                           it_sphere,
                           statistics["vacancy_found"], language,
                           statistics["processed_salary"], language,
                           statistics["average_salary"], language
        ])
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table

print(make_table_salary_statisctis(salary_super_job, title_super_job))
