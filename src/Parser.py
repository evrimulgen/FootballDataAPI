import util as util

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

    print(str(len(league_urls)) + " league urls gathered.")
    league_objects = []

    for league_url in league_urls:
        league = util.check_exception(api.get_league, (league_url,))
        if league:
            league_objects.append(league)
            print("\t" + league.name + " is parsed.")
    print(str(len(league_objects)) + " league objects created.\n\n")
    print_leagues(league_objects)

    line = input("\n\nTo continue to collect team data press Y: ")
    if line != "Y":
        return

    print("Starting to collecting team data")
    team_objects = []
    for league in league_objects:
        team_dict = util.check_exception(api.get_team_urls, (league,))
        for team_urls in team_dict["url_list"]:
            team = util.check_exception(api.get_team, (team_dict["league"], team_urls))
            if team:
                team_objects.append(team)
                print("\t" + team.name + " -> OK")
        print(league.name + "'s teams gathered.")
    print(str(len(team_objects)) + " team parsed and translated to league object.\n\n")
    #print_teams(team_objects)

    line = input("\n\nTo continue to collect player data press Y: ")
    if line != "Y":
        return

    print("Starting to collect player data")
    player_objects = []
    for team in team_objects:
        player_urls = util.check_exception(api.get_player_urls, team)
        for player_url in player_urls:
            player = util.check_exception(api.get_player, (team, player_url))
            if player:
                player_objects.append(player)
                print("\t\t" + player.name + " -> OK")
        print(team.name + "'s players gathered.")
    print(str(len(player_objects)) + " player parsed and translated to league object.\n\n")
    #print_players(player_objects)
    print("Parsing complete...")
    return league_objects


def menu(leagues):
    while(True):
        try:
            print_leagues(leagues)
            line = input("\n\nEnter league id (QUIT for quit): ")
            if line == "QUIT":
                break
            id = int(line)

            teams = leagues[id-1].teams
            print_teams(teams)
            line = input("\n\nEnter team id (QUIT for quit) (-14 for index): ")
            if line == "QUIT":
                break
            if line == "-14":
                continue
            id = int(line)

            teams[id-1].info()
            print("==============================================")
            players = teams[id-1].players
            print_players(players)
            line = input("\n\nEnter player id (QUIT for quit) (-14 for index): ")
            if line == "QUIT":
                break
            if line == "-14":
                continue
            id = int(line)

            print(players[id-1].info())
            input("Press something to start over...")

        except:
            print("Enter valid value")


if __name__ == "__main__":
    line = input("To start press Y: ")
    if line == "Y":
        leagues = parse()
        menu(leagues)










