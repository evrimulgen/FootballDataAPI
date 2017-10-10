from bs4 import BeautifulSoup
import json
import requests

BASE_URL = "http://www.mackolik.com/"


def control_none(func, args):
    result = None
    trial_count = 0
    while result is None:
        try:
            result = func(*args)
        except Exception:
            pass
        if trial_count == 5:
            write_error("Network Problem --- " + func.__name__ + " faced problem....")
    return result


def check_exception(func, args):
    trial_count = 0
    while True:
        try:
            return func(*args)
        except Exception as e:
            print("Error trying again " + func.__name__ + " " + str(e))
            if trial_count == 3:
                print("Giving up " + func.__name__ + " " + str(e))
                write_error("Giving Up Error --- Giving up\t" + func.__name__ + "\t" + str(e) + "\t" + str(args))
                return None
            trial_count += 1
            pass


def open_url(url, headers):
    return requests.get(url, headers=headers)


def soup(url, headers):
    return BeautifulSoup(control_none(open_url, (url, headers)).text, "html.parser")


def get_soup(url, headers=None):
    return control_none(soup, (url, headers))


def json(url, headers):
    return json.loads(open_url(control_none(open_url, (url, headers)).text, headers))


def get_json(url, headers=None):
    return control_none(json, (url, headers))


def translate(str):
    change = {'ı': "i", 'ç': "c", 'ş': "s", 'ü': "u", 'ö': "o", 'ğ': "g", 'İ': "I", 'Ç': "C", 'Ş': "S", 'Ü': "U",
            'Ö': "O", 'Ğ': "G"}
    new = str
    for key in change:
        new = new.replace(key, change[key])
    return "-".join(new.split())


def get_league_table_url(code, name):
    return BASE_URL + "/Puan-Durumu/" + code + "/" + translate(name)


def find_code(url):
    for i in url.split("/"):
        if i.isdigit():
            return int(i)


def write_error(error_message):
    print("\t\t\t\t" + error_message)
    with open('errors.txt', 'a') as file:
        file.write(error_message + "\n")