from bs4 import BeautifulSoup
import requests, os, sys, json


BASE_URL = "http://www.mackolik.com/"


def control_none(func, args):
    result = None
    trial_count = 0
    while result is None:
        try:
            result = func(*args)
            trial_count += 1
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
            if trial_count == 0:
                print("\t\t\t" + "-" * 38)
            print("\t\t\tError. Program will try again {} times. ".format(3-trial_count+1))
            if trial_count == 3:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                msg = str(exc_type) + "\t" + str(file_name) + "\t" + str(exc_tb.tb_lineno) + "\t" + \
                      func.__name__ + "\t" + str(e)
                write_error("Giving Up Error --- " + msg)
                print("\t\t\tGiving up trying. Error can't solve. " + msg)
                print("\t\t\t" + "-" * len(msg))
                return None
            trial_count += 1
            pass




def get_value(dict, key):
    try:
        return dict[key]
    except KeyError:
        return None


def open_url(url, headers):
    return requests.get(url, headers=headers)


def soup(url, headers):
    return BeautifulSoup(control_none(open_url, (url, headers)).text, "html.parser")


def get_soup(url, headers=None):
    return control_none(soup, (url, headers))


def json_without_check(url, headers):
    return json.loads(control_none(open_url, (url, headers)).text)


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
    with open('errors.txt', 'a') as file:
        file.write(error_message + "\n")