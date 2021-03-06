import os
from bs4 import BeautifulSoup
import csv
import json
import time
import requests

URL = "https://pl.jooble.org/praca-opieka-nad-osoba-starsza/Niemcy?date=3"

NEXT_PAGES = []
VISITED_URLS = {}
ID = 0


class HousingOffers:
    def __init__(self, **kwargs):
        self.id = kwargs.pop("id", None)
        self.company_name = kwargs.pop("company_name", None)
        self.salary = kwargs.pop("salary", None)
        self.location = kwargs.pop("location", None)
        self.title = kwargs.pop("title", None)
        self.link = kwargs.pop("link", None)
        self.time = kwargs.pop("time", None)

    def __str__(self):
        return (
            "{id} {company_name} {salary} {location} {link} {title} {link} {time}"
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
        "temu": "",
        "y": "",
        "ę": ""
    }

    for k, v in replacements.items():
        offer.time = offer.time.replace(k, v)

    offer.time = offer.time.strip()


def extract_paging(text):
    global NEXT_PAGES

    soup = BeautifulSoup(text, 'lxml')
    tag = soup.find("div", {"id": "paging"})
    links = tag.find_all("a")
    urls = list(sorted(
        filter(
            bool,
            [link.attrs.get("data-href", None) for link in links],
        )
    ))

    for url in urls:
        if url not in NEXT_PAGES and url not in VISITED_URLS:
            NEXT_PAGES.append(url)


def extract_offers(text):
    global ID
    offers = []

    soup = BeautifulSoup(text, 'lxml')
    jobs = soup.find_all(class_="vacancy_wrapper vacancy-js vacancy_wrapper-js")

    for job in jobs:
        ID += 1
        try:
            company_name = job.find(class_='company-name').text
        except Exception as e:
            print("company_name", e)
            company_name = "EMPTY"
        try:
            salary = job.find(class_='salary').text
        except Exception as e:
            print("salary", e)
            salary = "EMPTY"
        try:
            location = job.find(class_='date_location__region').text
        except Exception as e:
            print("location", e)
            location = "EMPTY"
        try:
            title = job.find(class_='link-position job-marker-js').text.strip()
        except Exception as e:
            print("title", e)
            title = "EMPTY"
        try:
            link1 = job.find(class_='link-position job-marker-js')
            link = link1.attrs["href"]
        except Exception as e:
            print("link", e)
            link = "EMPTY"
        try:
            time = job.find(class_='date_location').text
            time = time[0:17]
        except Exception as e:
            print("date", e)
            time = "EMPTY"

        if "opiek" in title.lower():
            offer = HousingOffers(id=ID, company_name=company_name, salary=salary,
                                  location=location,
                                  title=title, link=link, time=time)
            fix(offer)
            offers.append(offer)

    jobs = soup.find_all(class_="vacancy_wrapper vacancy-js vacancy_wrapper-js vacancy_wrapper--easy-apply")

    for job in jobs:
        ID += 1
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
            time = job.find(class_='date_location').text
            time = time[0:17]
        except Exception as e:
            time = "EMPTY"

        if "opiek" in title.lower():
            offer = HousingOffers(id=ID, company_name=company_name, salary=salary, location=location,
                                  title=title, link=link, time=time)
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
        VISITED_URLS[next_url] = True

        if response.ok:
            print("Extract")
            source = response.text
            offers = extract_offers(source)
            extract_paging(source)

            output_filename = os.path.join(output_dir,
                                           "plik-%d.json" % page_id)
            with open(output_filename, 'w+', encoding='utf-8') as json_file:
                json.dump([o.__dict__ for o in offers], json_file)
                print("WROTE:", output_filename)

            url = NEXT_PAGES.pop(0) if NEXT_PAGES else None
            if not url:
                break
            elif url not in VISITED_URLS:
                next_url = url
        else:
            print("ERROR")
            next_url = None

    create_result_file(output_dir)


def create_result_file(directory):
    merged_dict = {}
    for entry in os.listdir(directory):
        if entry.endswith(".json"):
            json_file = os.path.join(directory, entry)
            offers = json.load(open(json_file, "r"))
            for o in offers:
                merged_dict[o["id"]] = o

    #print(merged_dict)

    output_filename = os.path.join(directory, "results.csv")
    with open(output_filename, 'w+', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile,
                                    fieldnames=["id", "time", "company_name", "salary", "location", "title", "link"],
                                    delimiter=",")
        csv_writer.writeheader()
        csv_writer.writerows(merged_dict.values())


if __name__ == "__main__":
    main()

