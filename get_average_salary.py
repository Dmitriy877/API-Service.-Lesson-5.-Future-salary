import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable
from time import sleep


def get_it_vacancy_found_head_hunter(language):
    moscow_id = 1
    payload = {
        "text": language,
        "area": moscow_id,
        "premium": True,
        }
    url = "https://api.hh.ru/vacancies"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()["found"]


def get_it_vacancy_found_super_job(language, api_key):
    headers = {"X-Api-App-Id": api_key}
    payload_super_job = {
        "count": 100,
        "page": 0,
        "town": "Москва",
        "keyword": language,
        "no_agreement": 1
        }
    url = "https://api.superjob.ru/2.0/vacancies/"
    response = requests.get(url, headers=headers, params=payload_super_job)
    response.raise_for_status()
    answer = response.json()["total"]
    return answer


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    if not salary_from and salary_to:
        return salary_to*0.8
    if salary_from and not salary_to:
        return salary_from*1.2


def predict_rub_salary_head_hunter(vacancy):
    salary_from = vacancy["salary"]["from"]
    salary_to = vacancy["salary"]["to"]
    predict_salary = predict_rub_salary(salary_from, salary_to)
    return predict_salary


def predict_rub_salary_super_job(vacancy):
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    predict_salary = predict_rub_salary(salary_from, salary_to)
    return predict_salary


def get_head_hunter_vacancy(languages):
    it_vacancies = []
    only_salary = []
    salary_head_hunter = {}
    moscow_id = 1

    for language in languages:
        sleep(1)
        page = 0
        pages = 1

        while page < pages:
            payload = {
                "text": language,
                "area": moscow_id,
                "premium": True,
                "only_with_salary": True,
                "page": page
                }
            url = "https://api.hh.ru/vacancies"
            response = requests.get(url, params=payload)
            response.raise_for_status()
            vacancies = response.json()["items"]
            for vacancy in vacancies:
                it_vacancies.append(vacancy)
            page += 1
            pages = response.json()["pages"]
            sleep(1)
        for vacancy in it_vacancies:
            only_salary.append(predict_rub_salary_head_hunter(vacancy))

        vacancy_found = get_it_vacancy_found_head_hunter(language)
        processed_salary = len(only_salary)
        average_salary = int((sum(only_salary)/len(only_salary)))
        salary_head_hunter.update({language: {
            "vacancy_found": vacancy_found,
            "processed_salary": processed_salary,
            "average_salary": average_salary,
            }})
    return salary_head_hunter


def get_super_job_vacancy_info(api_key, languages):
    super_job_vacancy = []
    average_salaries = []
    salary_information_super_job = {}

    for language in languages:
        sleep(1)
        page = 0
        pages = 1
        while page < pages:
            headers = {"X-Api-App-Id": api_key}
            payload_super_job = {
                "count": 100,
                "page": page,
                "town": "Москва",
                "keyword": language,
                "no_agreement": 1
                }
            url = "https://api.superjob.ru/2.0/vacancies/"
            response = requests.get(url, headers=headers, params=payload_super_job)
            response.raise_for_status()
            for vacancy in response.json()["objects"]:
                super_job_vacancy.append(vacancy)
            page += 1
            pages += 1
            sleep(1)
            if not response.json()["more"]:
                break

        for vacancy in super_job_vacancy:
            average_salaries.append(predict_rub_salary_super_job(vacancy))

        vacancies_found = get_it_vacancy_found_super_job(language, api_key)
        vacancies_processed = len(average_salaries)
        average_salary = int((sum(average_salaries)/len(average_salaries)))
        salary_information_super_job.update({language: {
            "vacancy_found": vacancies_found,
            "processed_salary": vacancies_processed,
            "average_salary": average_salary,
            }})
    return salary_information_super_job


def make_table_salary_statisctis(it_spheres_vacancy, title):
    table_data = [
          [
           "Язык программирования",
           "Вакансий найдено",
           "Вакансий обработано",
           "Средняя зарплата"
          ]
    ]
    for it_sphere in it_spheres_vacancy:
        table_data.append([it_sphere,
                           it_spheres_vacancy[it_sphere]["vacancy_found"],
                           it_spheres_vacancy[it_sphere]["processed_salary"],
                           it_spheres_vacancy[it_sphere]["average_salary"]
                           ])
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()


def show_table_salary_statisctis(api_key, languages):
    title_head_hunter = "HeadHunter Moscow"
    title_super_job = "SuperJob Moscow"
    head_hunter_it_spheres = get_head_hunter_vacancy(languages)
    super_job_it_spheres = get_super_job_vacancy_info(api_key,
                                                      languages)
    make_table_salary_statisctis(head_hunter_it_spheres,
                                 title_head_hunter)
    make_table_salary_statisctis(super_job_it_spheres, title_super_job)
    

def main():
    load_dotenv()
    super_job_api_key = os.environ["SUPER_JOB_SECRET_KEY"]
    languages = [
        "GO",
        "C++",
        "C",
        "C#",
        "Python"
        "Java",
        "JavaScript"
        ]
    title_head_hunter = "HeadHunter Moscow"
    title_super_job = "SuperJob Moscow"
    head_hunter_vacancy_info = get_head_hunter_vacancy(languages)
    super_job_vacancy_info = get_super_job_vacancy_info(super_job_api_key,
                                                        languages)
    make_table_salary_statisctis(head_hunter_vacancy_info, title_head_hunter)
    make_table_salary_statisctis(super_job_vacancy_info, title_super_job)


if __name__ == "__main__":
    main()
