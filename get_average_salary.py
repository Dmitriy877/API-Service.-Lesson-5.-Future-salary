import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable
from time import sleep


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    if not salary_from and salary_to:
        return salary_to*0.8
    if salary_from and not salary_to:
        return salary_from*1.2
    if not salary_from and not salary_to:
        return None


def predict_rub_salary_head_hunter(vacancy):
    salary_from = vacancy["salary"]["from"]
    salary_to = vacancy["salary"]["to"]
    expected_salary = predict_rub_salary(salary_from, salary_to)
    return expected_salary


def predict_rub_salary_super_job(vacancy):
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    expected_salary = predict_rub_salary(salary_from, salary_to)
    return expected_salary


def get_head_hunter_statistics(languages):
    it_vacancies = []
    expected_salaries = []
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
                "page": page,
                "only_with_salary": True
            }
            url = "https://api.hh.ru/vacancies"
            response = requests.get(url, params=payload)
            response.raise_for_status()
            page_answer = response.json()
            for vacancy in page_answer["items"]:
                it_vacancies.append(vacancy)
            page += 1
            pages = page_answer["pages"]
            sleep(1)
        for vacancy in it_vacancies:
            expected_salaries.append(predict_rub_salary_head_hunter(vacancy))

        vacancy_found = page_answer["found"]
        processed_salary = len(expected_salaries)
        if processed_salary:
            average_salary = int((sum(expected_salaries)/len(expected_salaries)))
        else:
            average_salary = "Недостаточно вакансий для расчета"
        salary_head_hunter[language] = {
            "vacancy_found": vacancy_found,
            "processed_salary": processed_salary,
            "average_salary": average_salary,
        }
    return salary_head_hunter


def get_super_job_statistics(api_key, languages):
    super_job_vacancy = []
    expected_salaries = []
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
            page_answer = response.json()
            for vacancy in page_answer["objects"]:
                super_job_vacancy.append(vacancy)
            page += 1
            pages += 1
            sleep(1)
            if not page_answer["more"]:
                break

        for vacancy in super_job_vacancy:
            expected_salaries.append(predict_rub_salary_super_job(vacancy))

        vacancies_found = page_answer["total"]
        processed_salary = len(expected_salaries)
        if processed_salary:
            average_salary = int((sum(expected_salaries)/len(expected_salaries)))
        else:
            average_salary = "Недостаточно вакансий для расчета"
        salary_information_super_job[language] = {
            "vacancy_found": vacancies_found,
            "processed_salary": processed_salary,
            "average_salary": average_salary,
            }
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
        table_data.append([
                           it_sphere,
                           it_spheres_vacancy[it_sphere]["vacancy_found"],
                           it_spheres_vacancy[it_sphere]["processed_salary"],
                           it_spheres_vacancy[it_sphere]["average_salary"]
        ])
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
    

def main():
    load_dotenv()
    super_job_api_key = os.environ["SUPER_JOB_SECRET_KEY"]
    languages = [
        "GO"
    ]
    title_head_hunter = "HeadHunter Moscow"
    title_super_job = "SuperJob Moscow"
    head_hunter_vacancy = get_head_hunter_statistics(languages)
    super_job_vacancy = get_super_job_statistics(super_job_api_key,
                                                 languages)
    print(make_table_salary_statisctis(head_hunter_vacancy, title_head_hunter))
    print(make_table_salary_statisctis(super_job_vacancy, title_super_job))


if __name__ == "__main__":
    main()
