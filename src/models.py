from src import util as util


class Country:
    country_list = []

    def __init__(self, name, flag_url):
        self.name = name
        self.flag_url = flag_url
        Country.country_list.append(self)

    def asd(self):
        return "asd";

    def __str__(self):
        return self.name

    @staticmethod
    def is_exist(name):
        for country in Country.country_list:
            if name == country.name:
                return True
        return False

    @staticmethod
    def get_country(name):
        for country in Country.country_list:
            if name == country.name:
                return country
        return None

    @staticmethod
    def new_instance(name, flag_url):
        if Country.is_exist(name):
            return Country.get_country(name)
        else:
            return Country(name, flag_url)


class League:
    def __init__(self, country, name, url):
        self.country = country
        self.name = name.strip()
        self.url = url
        self.code = util.find_code(url)
        self.teams = []

    def __str__(self):
        return str(self.code) + " " * (8-len(str(self.code))) + "|" + \
               self.name + " " * (40-len(self.name)) + "|" + \
               str(self.country) + " " * (15-len(str(self.country))) + "|" + \
               self.url


class Team:
    def __init__(self, league, name, logo_url, website_url, found_date, phone_number, fax_number, address, stadium, url):
        self.league = league
        self.name = name
        self.logo_url = logo_url
        self.website_url = website_url
        self.found_date = found_date
        self.phone_number = phone_number
        self.fax_number = fax_number
        self.address = address
        self.stadium = stadium
        stadium.team = self
        self.url = url
        self.code = util.find_code(url)
        self.players = []

    def __str__(self):
        return str(self.code) + " " * (8 - len(str(self.code))) + "|" + self.name + " " * (35 - len(self.name)) + "|" + self.url

    def info(self):
        print("Name: " + self.name + "\nFound: " + self.found_date + "\nStadium: " + str(self.stadium) + "\nWebsite: " +
              self.website_url + "\nPhone Number: " + self.phone_number + "\nAdress: " + self.adress + "\nLogo: " + self.logo_url)


class Stadium:
    def __init__(self, name, capacity, url):
        self.name = name
        self.capacity = capacity
        self.url = url

    def __str__(self):
        return self.name + " (" + self.capacity + ")"


class Player:

    def __init__(self, team, name, long_name, birth_date, birth_place, height, weight, position, contract_expiry_date, country, photo_url, url):
        self.team = team
        self.name = name
        self.long_name = long_name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.height = height
        self.weight = weight
        self.position = position
        self.contract_expiry_date = contract_expiry_date
        self.country = country
        self.photo_url = photo_url
        self.url = url

    def __str__(self):
        return self.name

    def info(self):
        print("Name: " + self.name + "\nTeam: " + str(self.team) + "\nLong Name: " + self.long_name + "\nBirth Date: " + self.birth_date +
              "\nBirth Place: " + self.birth_place + "\nHeight: " + self.height + "\nWeight: " + self.weight + "\nPosition: " + self.position +
              "\nContract Expiry Date: " + self.contract_expiry_date + "\nCountry: " + str(self.country) + "\nPhoto URL: " + self.photo_url)




