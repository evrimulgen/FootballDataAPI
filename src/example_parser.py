import src.util as util
from src import MackolikAPI as api


def print_leagues(leagues):
    count = 1
    print("ID |REAL ID |LEAGUE" + " " * 34 + "|COUNTRY" + " " * 8 + "|URL")
    for i in leagues:
        print(str(count) + " " * (3-len(str(count))) + "|" + str(i))
        count += 1


def print_teams(teams):
    count = 1
    print("ID |REAL ID |TEAM" + " " * 31 + "|URL")

    for i in teams:
        print(str(count) + " " * (3-len(str(count))) + "|" + str(i))
        count += 1


def print_players(players):
    count = 1
    print("ID |NAME")

    for i in players:
        print(str(count) + " " * (3-len(str(count))) + "|" + str(i))
        count += 1


def parse():
    league_urls = util.check_exception(api.get_league_urls, ())
    leagues = []
    for league_url in league_urls:
        leagues.append(gather_league(league_url))
    return leagues


def gather_league(league_url):
    print("Starting to gathering league data with giving url; " + league_url)
    league = util.check_exception(api.get_league, (league_url,))

    if league:
        print(league.name + " is gathered successfully.")

        teams = gather_teams_of_league(league)

        for team in teams:
            gather_players_of_team(team)

        return league


def gather_teams_of_league(league):
    print("\tStarting to gathering teams data of " + league.name)
    team_objects = []
    team_urls = util.check_exception(api.get_team_urls, (league,))
    for team_url in team_urls:
        team = util.check_exception(api.get_team, (league, team_url))
        if team:
            team_objects.append(team)
            print("\t\t" + team.name + "'s data gathered successfully.")
    print("\tTeam data of {} gathered successfully. There are {} teams.\n".format(league.name, len(team_objects)))
    return team_objects


def gather_players_of_team(team):
    print("\t\t\tStarting to gathering player data of " + team.name)
    player_objects = []
    player_urls = util.check_exception(api.get_player_urls, (team,))
    for player_url in player_urls:
        player = util.check_exception(api.get_player, (team, player_url))
        if player:
            player_objects.append(player)
            print("\t\t\t\t" + player.name + "'s data gathered successfully.")
    print("\t\t\tPlayer data of {} gathered successfully. There are {} players.\n".format(team.name,
                                                                                          len(player_objects)))
    return player_objects


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

            teams = leagues[league_id-1].teams
            print_teams(teams)
            line = input("\n\nEnter team id (QUIT for quit) (-14 for index): ")
            if line == "QUIT":
                break
            if line == "-14":
                continue
            team_id = int(line)

            teams[team_id-1].info()
            print("==============================================")
            players = teams[team_id-1].players
            print_players(players)
            line = input("\n\nEnter player id (QUIT for quit) (-14 for index): ")
            if line == "QUIT":
                break
            if line == "-14":
                continue
            player_id = int(line)

            print(players[player_id-1].info())
            input("Press something to start over...")

        except Exception:
            print("Enter valid value")


if __name__ == "__main__":
    ln = input("To start press Y: ")
    if ln == "Y":
        league_objs = parse()
        menu(league_objs)











