import os
from bs4 import BeautifulSoup
import csv
import json
import time
import requests

URL = "https://pl.jooble.org/praca-opieka-nad-osoba-starsza/Niemcy?date=3"


class HousingOffers:
    def __init__(self, **kwargs):
        self.id = kwargs.pop("id", None)
        self.company_name = kwargs.pop("company_name", None)
        self.salary = kwargs.pop("salary", None)
        self.location = kwargs.pop("location", None)
        self.title = kwargs.pop("title", None)
        self.link = kwargs.pop("link", None)
        self.date = kwargs.pop("date", None)

    def __str__(self):
        return (
            "{id} {company_name} {salary} {location} {link} {title} {link} {date}"
        ).format(
            **self.__dict__
        )


def fix(offer):
    replacements = {
        "1 dzień temu": "24",
        "2 dni temu": "48",
        "3 dni temu": "72",
        "4 dni temu": "96",
        "5 dni temu": "120",
        "6 dni temu": "144",
        "7 dni temu": "168",
        "godzin": "",
        "temu": ""
    }

    for k, v in replacements.items():
        offer.date = offer.date.replace(k, v)

    offer.date = offer.date.strip()


def extract_next_url(text):
    soup = BeautifulSoup(text, 'lxml')
    tag = soup.find(attrs={"data-dir": "next"})
    next_url = tag.attrs["href"] if tag else None
    print("NEXT URL", next_url)
    return next_url


def extract_offers(text):
    offers = []

    soup = BeautifulSoup(text, 'lxml')
    jobs = soup.find_all(class_="vacancy_wrapper vacancy-js vacancy_wrapper-js")
    id = 0
    for job in jobs:
        id += 1
        try:
            company_name = job.find(class_='company-name').text
        except Exception as e:
            company_name = "EMPTY"
        try:
            salary = job.find(class_='salary').text
        except Exception as e:
            salary = "EMPTY"
        try:
            location = job.find(class_='date_location__region').text
        except Exception as e:
            location = "EMPTY"
        try:
            title = job.find(class_='link-position job-marker-js').text.strip()
        except Exception as e:
            title = "EMPTY"
        try:
            link1 = job.find(class_='link-position job-marker-js')
            link = link1.attrs["href"]
        except Exception as e:
            link = "EMPTY"
        try:
            date = job.find(class_='date_location').text
            date = date[0:17]
        except Exception as e:
            date = "EMPTY"

        offer = HousingOffers(id=id, company_name=company_name, salary=salary, location=location,
                              title=title, link=link, date=date)
        fix(offer)
        offers.append(offer)

    jobs = soup.find_all(class_="vacancy_wrapper vacancy-js vacancy_wrapper-js vacancy_wrapper--easy-apply")

    for job in jobs:
        id += 1
        try:
            company_name = job.find(class_='company-name').text
        except Exception as e:
            company_name = "EMPTY"
        try:
            salary = job.find(class_='salary').text
        except Exception as e:
            salary = "EMPTY"
        try:
            location = job.find(class_='date_location__region').text
        except Exception as e:
            location = "EMPTY"
        try:
            title = job.find(class_='link-position job-marker-js').text.strip()
        except Exception as e:
            title = "EMPTY"
        try:
            link1 = job.find(class_='link-position job-marker-js')
            link = link1.attrs["href"]
        except Exception as e:
            link = "EMPTY"
        try:
            date = job.find(class_='date_location').text
            date = date[0:17]
        except Exception as e:
            date = "EMPTY"

        offer = HousingOffers(id=id, company_name=company_name, salary=salary, location=location,
                              title=title, link=link, date=date)
        fix(offer)
        offers.append(offer)

    return offers


def main():
    session = requests.Session()

    session.headers["USER-AGENT"] = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64;"
        "Trident/7.0; rv:11.0) like Gecko"
    )

    next_url = URL

    dir_id = time.strftime("%Y-%m-%d-%s", time.localtime())
    output_dir = os.path.join("data", dir_id)
    os.makedirs(output_dir, exist_ok=True)

    page_id = 0

    while next_url:
        page_id += 1
        response = session.get(next_url)

        if response.ok:
            print("Extract")
            source = response.text
            offers = extract_offers(source)
            next_url = extract_next_url(source)

            output_filename = os.path.join(output_dir,
                                           "plik-%d.json" % page_id)
            with open(output_filename, 'w+', encoding='utf-8') as json_file:
                json.dump([o.__dict__ for o in offers], json_file)
                print("WROTE:", output_filename)
        else:
            print("ERROR")
            next_url = None

        print(next_url)

    create_result_file(output_dir)


def create_result_file(directory):
    merged_dict = {}
    for entry in os.listdir(directory):
        if entry.endswith(".json"):
            json_file = os.path.join(directory, entry)
            offers = json.load(open(json_file, "r"))
            for o in offers:
                merged_dict[o["id"]] = o

    print(merged_dict)

    output_filename = os.path.join(directory, "results.csv")
    with open(output_filename, 'w+', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile,
                                    fieldnames=["id", "date", "company_name", "salary", "location", "title", "link"],
                                    delimiter=",")
        csv_writer.writeheader()
        csv_writer.writerows(merged_dict.values())


if __name__ == "__main__":
    main()

