import src.util as util
from src import MackolikAPI as api
from src.models import DATABASE, initialize, League, Team, Player


def print_leagues(leagues):
    count = 1
    print("ID |REAL ID |LEAGUE" + " " * 34 + "|COUNTRY" + " " * 8 + "|URL")
    for i in leagues:
        print(str(count) + " " * (3 - len(str(count))) + "|" + str(i))
        count += 1


def print_teams(teams):
    count = 1
    print("ID |REAL ID |TEAM" + " " * 31 + "|URL")

    for i in teams:
        print(str(count) + " " * (3 - len(str(count))) + "|" + str(i))
        count += 1


def print_players(players):
    count = 1
    print("ID |NAME")

    for i in players:
        print(str(count) + " " * (3 - len(str(count))) + "|" + str(i))
        count += 1


def give_difference_list(existed_ones, url_list):
    difference_list = []
    if not url_list:
        return difference_list
    for url in url_list:
        if not is_saved_already(existed_ones, url):
            difference_list.append(url)
    return difference_list


def is_saved_already(existed_ones, url):
    for existed in existed_ones:
        if existed.url == url:
            return True
    return False


def parse():
    league_urls = util.check_exception(api.get_league_urls, ())
    existed_league_objects = list(League.select())

    difference_list = give_difference_list(existed_league_objects, league_urls)
    print("The league difference is " + str(len(difference_list)))
    for url in difference_list:
        league = gather_league(url)
        if league:
            existed_league_objects.append(gather_league(url))

    # Start gather teams of league. It will looks database first.
    for league in existed_league_objects:
        gather_teams_of_league(league)

    # Start gather player of team. It will looks database first.
    for team in list(Team.select()):
        gather_players_of_team(team)

    return existed_league_objects


def gather_league(league_url):
    print("Starting to gathering league data with giving url; " + league_url)
    league = util.check_exception(api.get_league, (league_url,))

    if league:
        print(league.name + " is gathered successfully.")
        return league


def gather_teams_of_league(league):
    print("\tStarting to gathering teams data of " + league.name)
    team_urls = util.check_exception(api.get_team_urls, (league,))
    existed_team_objects = list(Team.select().join(League).where(League.id == league.id))

    difference_list = give_difference_list(existed_team_objects, team_urls)
    print("The team difference of " + league.name + " is " + str(len(difference_list)))
    for url in difference_list:
        team = util.check_exception(api.get_team, (league, url))
        if team:
            existed_team_objects.append(team)
            print("\t\t" + team.name + "'s data gathered successfully.")
    print("\tTeam data of {} gathered successfully. There are {} teams.\n".format(league.name, len(difference_list)))
    return existed_team_objects


def gather_players_of_team(team):
    print("\t\t\tStarting to gathering player data of " + team.name)
    player_urls = util.check_exception(api.get_player_urls, (team,))
    existed_player_objects = list(Player.select().join(Team).where(Team.id == team.id))

    difference_list = give_difference_list(existed_player_objects, player_urls)

    for url in difference_list:
        player = util.check_exception(api.get_player, (team, url,))
        if player:
            existed_player_objects.append(player)
            print("\t\t\t\t" + player.name + "'s data gathered successfully.")
    print("\t\t\tPlayer data of {} gathered successfully. There are {} players.\n".format(team.name,
                                                                                          len(difference_list)))
    return existed_player_objects


def menu(leagues):
    while True:
        try:
            print_leagues(leagues)
            print("\n\n")
            input("Opening menu enter something...")
            line = input("\n\nEnter league id (QUIT for quit): ")
            if line == "QUIT":
                break
            league_id = int(line)

            teams = leagues[league_id - 1].teams
            print_teams(teams)
            line = input("\n\nEnter team id (QUIT for quit) (-14 for index): ")
            if line == "QUIT":
                break
            if line == "-14":
                continue
            team_id = int(line)

            teams[team_id - 1].info()
            print("==============================================")
            players = teams[team_id - 1].players
            print_players(players)
            line = input("\n\nEnter player id (QUIT for quit) (-14 for index): ")
            if line == "QUIT":
                break
            if line == "-14":
                continue
            player_id = int(line)

            print(players[player_id - 1].info())
            input("Press something to start over...")

        except Exception:
            print("Enter valid value")


if __name__ == "__main__":
    initialize()
    leagues = parse()
    menu(leagues)
