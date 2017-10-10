import util as util

from src.models import Country, League, Team, Stadium, Player


def get_league_urls():
    entry_url = "http://www.mackolik.com/Puan-Durumu/1/TURKIYE-Super-Lig"
    options = util.get_soup(entry_url).find("select", {"id": "cboLeague"}).find_all("option")

    league_urls = []
    for option in options:
        code = option["value"].split("-")[0]
        name = option.text
        league_urls.append(util.get_league_table_url(code, name))
    return league_urls


def get_league(url):
    soup = util.get_soup(url)
    img_tag = soup.find("h1", {"class": "season-league"}).find("img")
    country = Country.new_instance(img_tag.text.strip().split()[0], img_tag["src"])
    league_name = " ".join(img_tag.text.strip().split(" ")[1:len(img_tag.text.strip())])
    return League(country, league_name, url)


def get_team_urls(league):
    base_url = "http://www.mackolik.com/AjaxHandlers/StandingHandler.aspx?command=getSerials&id="
    headers = {"Host": "www.mackolik.com", "Connection": "keep-alive", "Accept": "*/*",
               "X-Requested-With": "XMLHttpRequest",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
               "Referer": "http://www.mackolik.com/Puan-Durumu/1/TURKIYE-Super-Lig", "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.6,en;q=0.4",
               "Cookie": "__gfp_64b=dhmw9J1QJnLwqLN7bKvnZQ4P_a7RmXolhpw5k90hn5r.U7; __auc=ab3f6f1e15e8fdec736d894ca2f; _ga=GA1.2.455780513.1505652296; _gid=GA1.2.1230460567.1507370259"}
    soup = util.get_soup(base_url + str(league.code), headers=headers)
    tag_list = soup.find_all("a")
    dict = {"league": league, "url_list": []}
    for tag in tag_list:
        dict["url_list"].append(tag["href"])
    return dict


def get_team(league, team_url):
    soup = util.get_soup(team_url)
    div = soup.find("div", {"id": "dvClubLogo"})
    name = div.find("h1", {"itemprop": "name"}).text.strip()
    logo_url = div.find("img")["src"]

    rows = div.find("table", {"class":"kulup-tbl"}).find_all("tr")
    raw_data = []
    for row in rows:
        try:
            raw_data.append(row.find_all("td")[2])
            raw_data.append(row.find_all("td")[5])
        except IndexError:
            pass

    stadium_name = raw_data[1].text.strip()
    capacity = raw_data[3].text.strip()
    try:
        stadium_url = raw_data[1].find("a")["href"]
    except:
        stadium_url = None
        util.write_error("Parse Error --- " + name + " has stadium url error...")
    stadium = Stadium(stadium_name, capacity, stadium_url)

    found_date = raw_data[0].text.strip()
    website_url = raw_data[2].text.strip()
    phone_number = raw_data[4].text.strip()
    fax_number = raw_data[5].text.strip()
    address = raw_data[6].text.strip()

    team = Team(league, name, logo_url, website_url, found_date, phone_number, fax_number, address, stadium, team_url)

    return team


def get_player_urls(team):
    base_url = "http://www.mackolik.com/Team/SquadData.aspx?id="
    json = util.get_json(base_url + str(team.code))
    squad = json["s"]

    url_list = []
    for pos in squad:
        for player in pos["s"]:
            url_list.append("http://www.mackolik.com/Player/Default.aspx?id=" + str(player[1]) + "&season=2017%2F2018")
    return url_list


def get_player(team, url):
    soup = util.get_soup(url)
    div = soup.find("div", {"id": "dvPlayerDetails"}).contents

    left_div = div[1]
    right_div = div[3]

    photo_url = left_div.find("img")["src"]
    name = right_div.find("h1", {"itemprop": "name"}).text.strip()

    country_name = right_div.find("img", {"itemprop": "image"})["alt"].strip()
    country_flag = right_div.find("img", {"itemprop": "image"})["src"]
    country = Country.new_instance(country_name, country_flag)

    info_div = right_div.find("div", {"id": "dvPlayerInfo"}).find_all("div")
    long_name = info_div[1].text.replace(":","").strip()
    birth_date = info_div[3].text.replace(":", "").strip()[0:10]
    birth_place = info_div[5].text.replace(":", "").strip()
    height = info_div[7].text.replace(":", "").strip()
    weight = info_div[9].text.replace(":", "").strip()
    position = info_div[11].text.replace(":", "").strip()
    contract_expiry_date = info_div[13].text.replace(":", "").strip()
    player = Player(team, name, long_name, birth_date, birth_place, height, weight, position, contract_expiry_date, country, photo_url, url)
    team.players.append(player)

    return player




