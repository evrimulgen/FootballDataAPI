from src import util as util
from peewee import *

DATABASE = SqliteDatabase("FootballData.db")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Country, League, Stadium, Team, Player], safe=True)
    DATABASE.close()


class BaseModel(Model):
    name = CharField(index=True)
    url = CharField(null=True)

    class Meta:
        database = DATABASE


class Country(BaseModel):
    flag_url = CharField(null=True)

    @staticmethod
    def get_country(name):
        try:
            return Country.get(Country.name == name)
        except DoesNotExist:
            return None

    @staticmethod
    def new_instance(name, flag_url):
        country = Country.get_country(name)
        if not country:
            country = Country(name=name, flag_url=flag_url)
            country.save()
            return country
        return country


class League(BaseModel):
    country = ForeignKeyField(Country, related_name="leagues", on_delete='CASCADE', on_update='CASCADE')
    url = CharField()
    code = CharField()

    @staticmethod
    def get_league(url):
        try:
            return League.get(League.url == url)
        except DoesNotExist:
            return None

    @staticmethod
    def new_instance(country, name, url):
        league = League.get_league(url)
        if not league:
            league = League(country=country, name=name, url=url, code=util.find_code(url))
            league.save()
            return league
        return league


class Stadium(BaseModel):
    capacity = CharField(max_length=14, null=True)

    @staticmethod
    def get_stadium(name):
        try:
            return Stadium.get(Stadium.name == name)
        except DoesNotExist:
            return None

    @staticmethod
    def new_instance(name, url, capacity):
        stadium = Stadium.get_stadium(name)
        if not stadium:
            stadium = Stadium(name=name, url=url, capacity=capacity)
            stadium.save()
            return stadium
        return stadium


class Team(BaseModel):
    league = ForeignKeyField(League, related_name="teams", on_delete='CASCADE', on_update='CASCADE')
    logo_url = CharField(null=True)
    website_url = CharField(null=True)
    found_date = CharField(max_length=6, null=True)
    phone_number = CharField(max_length=14, null=True)
    fax_number = CharField(max_length=14, null=True)
    address = CharField(null=True)
    stadium = ForeignKeyField(Stadium, related_name="owners", null=True)
    code = CharField()

    @staticmethod
    def get_team(url):
        try:
            return Team.get(Team.url == url)
        except DoesNotExist:
            return None

    @staticmethod
    def new_instance(name, league, stadium, found_date, address, phone_number, fax_number, website_url, logo_url, url):
        team = Team.get_team(url)
        if not team:
            team = Team(name=name, league=league, stadium=stadium, found_date=found_date, adress=address,
                        phone_number=phone_number, fax_number=fax_number, website_url=website_url, logo_url=logo_url,
                        url=url, code=util.find_code(url))
            team.save()
            return team
        return team


class Player(BaseModel):
    team = ForeignKeyField(Team, related_name="players", on_delete='CASCADE', on_update="CASCADE")
    country = ForeignKeyField(Country, related_name="citizens")
    long_name = CharField(null=True)
    birth_date = CharField(null=True)
    birth_place = CharField(null=True)
    height = IntegerField(null=True)
    weight = IntegerField(null=True)
    position = CharField(null=True)
    contract_expiry_date = CharField(null=True)
    photo_url = CharField(null=True)

    @staticmethod
    def get_player(name):
        try:
            return Player.get(Player.name == name)
        except DoesNotExist:
            return None

    @staticmethod
    def new_instance(name, team, country, long_name, birth_date, birth_place, height, weight, position,
                     contract_expiry_date, photo_url, url):
        player = Player.get_player(name)
        if not player:
            player = Player(name=name, team=team, country=country, long_name=long_name, birth_date=birth_date,
                            birth_place=birth_place, height=height, weight=weight, position=position,
                            contract_expiry_date=contract_expiry_date, photo_url=photo_url, url=url)
            player.save()
            return player

        return player
