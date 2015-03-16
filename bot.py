import sys
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import requests
from lxml import html
import random
 
BOLD = "\x02"
 
def bold(text):
    return BOLD + text + BOLD
 
category_dict = {
    "fg%": "Field Goal Pct",
    "3p%": "3-Pt Field Goal Pct",
    "ft%": "Free Throw Pct",
    "mpg": "Minutes Per Game",
    "ppg": "Points Per Game",
    "rpg": "Rebounds Per Game",
    "apg": "Assists Per Game",
    "spg": "Steals Per Game",
    "bpg": "Blocks Per Game",
    "per": "Player Efficiency Rating",
    "ts%": "True Shooting Pct",
    "usg%": "Usage Pct",
    "ortg": "Offensive Rating",
    "drtg": "Defensive Rating",
    "ws": "Win Shares",
    "ws/48": "Win Shares Per 48 Minutes"
}
 
proxies = {
    "http:": "http://221.10.40.238",
    "https:": "https://221.231.135.149",
}
 
entities = [('&nbsp;', u'\u00a0')]
 
def num(s):
    try:
        return int(s)
    except ValueError:
        return -1
 
def check_url(page, player):
    url = page
    page = requests.get(url, proxies = proxies)
    tree = html.fromstring(page.text)
 
    try:
        name = tree.xpath('//div[@id="info_box"]/h1/text()')[0]
    except Exception:
        try:
            name = tree.xpath('//div[@class="person_image_offset"]/h1/text()')[0]
        except IndexError:
            return 0;
 
    name = name.lower().replace('.', '').replace('-', ' ').replace('\'', '')
    if str(player) == name:
        return 1
    else:
        return 0
 
class Bot(irc.IRCClient):
 
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)
 
    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % self.nickname
 
    def joined(self, channel):
        print "Joined %s." % channel
 
    def privmsg(self, user, channel, msg):
        nick = user.split('!', 1)[0]
        print nick + ": " + msg
        if msg.startswith('.nstats'):
            parts = msg.split('.nstats ')
            data = str(parts[1])
            more_data = data.split(' ')
            first = str(more_data[0]).lower()
            try:
                temp = str(more_data[2])
            except IndexError:
                temp = None
                middle = None
 
            if temp:
                try:
                    temp_2 = str(more_data[3])
                except IndexError:
                    temp_2 = None
 
            if temp:
                if temp.isdigit():
                    year = temp
                    middle = None
                    last = str(more_data[1].lower().replace('\'', ''))
                elif temp.isalpha():
                    if temp_2:
                        if temp_2.isdigit():
                            year = temp_2
                        else:
                            year = "2015"
                    else:
                        year = "2015"
                    last = temp.lower().replace('\'', '')
                    middle = str(more_data[1]).lower().replace('\'', '')
                else:
                    year = "2015"
                    middle = None
                    last = str(more_data[1]).lower().replace('\'', '')
            else:
                last = str(more_data[1]).lower().replace('\'', '')
                year = "2015"
                middle = None
 
            if middle:
                player = str(first) + " " + str(middle) + " " + str(last)
                if len(middle) <= 5:
                    url_end1 = str(middle[0]) + "/" + str(middle) + str(first[0:2]) + "01.html"
                    url_end2 = str(middle[0]) + "/" + str(middle) + str(first[0:2]) + "02.html"
                    url_end3 = str(middle[0]) + "/" + str(middle) + str(first[0:2]) + "03.html"
                    url_end4 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "01.html"
                    url_end5 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "02.html"
                    url_end6 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "03.html"
                else:
                    url_end1 = str(middle[0]) + "/" + str(middle[0:5]) + str(first[0:2]) + "01.html"
                    url_end2 = str(middle[0]) + "/" + str(middle[0:5]) + str(first[0:2]) + "02.html"
                    url_end3 = str(middle[0]) + "/" + str(middle[0:5]) + str(first[0:2]) + "03.html"
                    url_end4 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "01.html"
                    url_end5 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "02.html"
                    url_end6 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "03.html"
 
            else:
                player = str(first) + " " + str(last)
                if len(last) <= 5:
                    url_end1 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "01.html"
                    url_end2 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "02.html"
                    url_end3 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "03.html"
                else:
                    url_end1 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "01.html"
                    url_end2 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "02.html"
                    url_end3 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "03.html"
 
            url1 = "http://www.basketball-reference.com/players/" + url_end1
            url2 = "http://www.basketball-reference.com/players/" + url_end2
            url3 = "http://www.basketball-reference.com/players/" + url_end3
            if middle:
                url4 = "http://www.basketball-reference.com/players/" + url_end4
                url5 = "http://www.basketball-reference.com/players/" + url_end5
                url6 = "http://www.basketball-reference.com/players/" + url_end6
 
            if check_url(url1, player) == 1:
                final_url = url1
            elif check_url(url2, player) == 1:
                final_url = url2
            elif check_url(url3, player) == 1:
                final_url = url3
            elif check_url(url4, player) == 1:
                final_url = url4
            elif check_url(url5, player) == 1:
                final_url = url5
            else:
                final_url = url6
 
            bballref = requests.get(final_url, proxies = proxies)
            bballtree = html.fromstring(bballref.text)
 
            try:
                fullname = bballtree.xpath('//div[@id="info_box"]/h1/text()')[0]
            except Exception:
                fullname = bballtree.xpath('//div[@class="person_image_offset"]/h1/text()')[0]
 
            page_year = bballtree.xpath('//tr[@id="per_game.%s"]' % year)
 
            for stat in page_year:
                age = stat.xpath('td[2]/text()')[0]
                try:
                    team = stat.xpath('td[3]/a/text()')[0]
                except IndexError:
                    team = stat.xpath('td[3]/text()')[0]
                try:
                    position = stat.xpath('td[5]/text()')[0]
                except IndexError:
                    position = "Not listed"
                games_played = stat.xpath('td[6]/text()')[0]
                fg_pct = stat.xpath('td[11]/text()')[0]
                try:
                    season = stat.xpath('td[1]/a/text()')[0]
                except IndexError:
                    season = stat.xpath('td[1]/text()')[0]
                try:
                    minutes = stat.xpath('td[8]/text()')[0]
                except IndexError:
                    minutes = "Not recorded"
                try:
                    three_pct = stat.xpath('td[14]/text()')[0]
                except IndexError:
                    three_pct = "Not recorded"
                try:
                    stl = stat.xpath('td[25]/text()')[0]
                    blk = stat.xpath('td[26]/text()')[0]
                except IndexError:
                    stl = "Not recorded"
                    blk = "Not recorded"
                try:
                    tov = stat.xpath('td[27]/text()')[0]
                except IndexError:
                    tov = "Not recorded"
                try:
                    rpg = stat.xpath('td[23]/text()')[0]
                except IndexError:
                    rpg = "Not recorded"
                try:
                    free_throw_pct = stat.xpath('td[20]/text()')[0]
                except IndexError:
                    free_throw_pct = "Didn't take any"
                apg = stat.xpath('td[24]/text()')[0]
                fouls = stat.xpath('td[28]/text()')[0]
                ppg = stat.xpath('td[29]/text()')[0]
 
            try:
                msg = "%s: %s | %s | %s | %s | Age: %s | GP: %s | MPG: %s | FG%%: %s | 3P%%: %s | FT%%: %s | PTS: %s | REB: %s | AST: %s | STL: %s | BLK: %s | TO: %s | PF: %s |" % (nick, fullname, season, team, position, age, games_played, minutes, fg_pct, three_pct, free_throw_pct, ppg, rpg, apg, stl, blk, tov, fouls)
            except UnboundLocalError:
                if year.isdigit():
                    msg = fullname + " did not play that year!"
                elif year == " ":
                    msg = fullname + " did not play last year!"
                else:
                    msg = "Proper format is .nstats [first name] [last name] [year (optional, default is last season)]"
 
            self.msg(channel, msg)
 
        if msg.startswith('.anstats'):
            parts = msg.split('.anstats ')
            data = str(parts[1])
            more_data = data.split(' ')
            first = str(more_data[0]).lower()
            try:
                temp = str(more_data[2])
            except IndexError:
                temp = None
                middle = None
 
            if temp:
                try:
                    temp_2 = str(more_data[3])
                except IndexError:
                    temp_2 = None
 
            if temp:
                if temp.isdigit():
                    year = temp
                    middle = None
                    last = str(more_data[1].lower().replace('\'', ''))
                elif temp.isalpha():
                    if temp_2:
                        if temp_2.isdigit():
                            year = temp_2
                        else:
                            year = "2015"
                    else:
                        year = "2015"
                    last = temp.lower().replace('\'', '')
                    middle = str(more_data[1]).lower().replace('\'', '')
                else:
                    year = "2015"
                    middle = None
                    last = str(more_data[1]).lower().replace('\'', '')
            else:
                last = str(more_data[1]).lower().replace('\'', '')
                year = "2015"
                middle = None
 
            if middle:
                player = str(first) + " " + str(middle) + " " + str(last)
                if len(middle) <= 5:
                    url_end1 = str(middle[0]) + "/" + str(middle) + str(first[0:2]) + "01.html"
                    url_end2 = str(middle[0]) + "/" + str(middle) + str(first[0:2]) + "02.html"
                    url_end3 = str(middle[0]) + "/" + str(middle) + str(first[0:2]) + "03.html"
                    url_end4 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "01.html"
                    url_end5 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "02.html"
                    url_end6 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "03.html"
                else:
                    url_end1 = str(middle[0]) + "/" + str(middle[0:5]) + str(first[0:2]) + "01.html"
                    url_end2 = str(middle[0]) + "/" + str(middle[0:5]) + str(first[0:2]) + "02.html"
                    url_end3 = str(middle[0]) + "/" + str(middle[0:5]) + str(first[0:2]) + "03.html"
                    url_end4 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "01.html"
                    url_end5 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "02.html"
                    url_end6 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "03.html"
 
            else:
                player = str(first) + " " + str(last)
                if len(last) <= 5:
                    url_end1 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "01.html"
                    url_end2 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "02.html"
                    url_end3 = str(last[0]) + "/" + str(last) + str(first[0:2]) + "03.html"
                else:
                    url_end1 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "01.html"
                    url_end2 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "02.html"
                    url_end3 = str(last[0]) + "/" + str(last[0:5]) + str(first[0:2]) + "03.html"
 
            url1 = "http://www.basketball-reference.com/players/" + url_end1
            url2 = "http://www.basketball-reference.com/players/" + url_end2
            url3 = "http://www.basketball-reference.com/players/" + url_end3
            if middle:
                url4 = "http://www.basketball-reference.com/players/" + url_end4
                url5 = "http://www.basketball-reference.com/players/" + url_end5
                url6 = "http://www.basketball-reference.com/players/" + url_end6
 
            if check_url(url1, player) == 1:
                final_url = url1
            elif check_url(url2, player) == 1:
                final_url = url2
            elif check_url(url3, player) == 1:
                final_url = url3
            elif check_url(url4, player) == 1:
                final_url = url4
            elif check_url(url5, player) == 1:
                final_url = url5
            else:
                final_url = url6
 
            bballref = requests.get(final_url, proxies = proxies)
            bballtree = html.fromstring(bballref.text)
 
            try:
                fullname = bballtree.xpath('//div[@id="info_box"]/h1/text()')[0]
            except Exception:
                fullname = bballtree.xpath('//div[@class="person_image_offset"]/h1/text()')[0]
 
            basic_year = bballtree.xpath('//tr[@id="per_game.%s"]' % year)
            page_year = bballtree.xpath('//tr[@id="advanced.%s"]' % year)
            poss_year = bballtree.xpath('//tr[@id="per_poss.%s"]' % year)
 
            for basic in basic_year:
                try:
                    minutes = basic.xpath('td[8]/text()')[0]
                except IndexError:
                    minutes = "Not recorded"
 
            for poss in poss_year:
                try:
                    ortg = poss.xpath('td[31]/text()')[0]
                    drtg = poss.xpath('td[32]/text()')[0]
                except IndexError:
                    ortg = "Not recorded"
                    drtg = "Not recorded"
 
            for stat in page_year:
                age = stat.xpath('td[2]/text()')[0]
                try:
                    team = stat.xpath('td[3]/a/text()')[0]
                except IndexError:
                    team = stat.xpath('td[3]/text()')[0]
                try:
                    position = stat.xpath('td[5]/text()')[0]
                except IndexError:
                    position = "Not listed"
                games_played = stat.xpath('td[6]/text()')[0]
                true_pct = stat.xpath('td[9]/text()')[0]
                try:
                    season = stat.xpath('td[1]/a/text()')[0]
                except IndexError:
                    season = stat.xpath('td[1]/text()')[0]
                try:
                    per = stat.xpath('td[8]/text()')[0]
                except IndexError:
                    per = "Not recorded"
                try:
                    reb_pct = stat.xpath('td[14]/text()')[0]
                except IndexError:
                    reb_pct = "Not recorded"
                try:
                    ast_pct = stat.xpath('td[15]/text()')[0]
                except IndexError:
                    ast_pct = "Not recorded"
                try:
                    usage = stat.xpath('td[19]/text()')[0]
                except IndexError:
                    usage = "Not recorded"
                ws = stat.xpath('td[23]/text()')[0]
                try:
                    plus_min = stat.xpath('td[28]/text()')[0]
                except IndexError:
                    plus_min = "Not recorded"
 
            try:
                msg = "%s: %s | %s | %s | %s | Age: %s | GP: %s | MPG: %s | PER: %s | TS%%: %s | REB%%: %s | AST%%: %s | USG%%: %s | Win Shares: %s | ORTG: %s | DRTG: %s | +/-: %s" % (nick, fullname, season, team, position, age, games_played, minutes, per, true_pct, reb_pct, ast_pct, usage, ws, ortg, drtg, plus_min)
            except UnboundLocalError:
                if year.isdigit():
                    msg = fullname + " did not play that year!"
                elif year == " ":
                    msg = fullname + " did not play last year!"
                else:
                    msg = "Proper format is .nstats [first name] [last name] [year (optional, default is most recent season)]"
 
            self.msg(channel, msg)
 
        if msg.startswith('.teamstats'):
            parts = msg.split('.teamstats ')
            data = parts[1]
            relevant_data = data.split(' ')
            team_name = str(relevant_data[0]).upper()
            try:
                year = relevant_data[1]
            except Exception:
                year = "2015"
 
            url = 'http://www.basketball-reference.com/teams/' + team_name + '/' + year + '.html'
            try:
                page = requests.get(url, proxies = proxies)
            except Exception:
                self.msg(channel, "Please enter the 3 letter abbreviation for the team.")
            tree = html.fromstring(page.text)
 
            full_title = tree.xpath('//div[@id="info_box"]/h1/text()')[0]
            team_year = full_title.split(" Roster")
            team_season = team_year[0]
 
            dirty_record = tree.xpath('//div[@id="info_box"]/p[2]/text()')[0]
            record = dirty_record.split(", ")[0].replace(' ', '')
 
            dirty_division = tree.xpath('//div[@id="info_box"]/p[2]/text()')[1]
            division = dirty_division.split(" (")[0][1:]
            standing = dirty_record.split(", ")[1] + division
 
            coach = tree.xpath('//div[@id="info_box"]/p[2]/a[3]/text()')[0]
            try:
                other_coach = tree.xpath('//div[@id="info_box"]/p[2]/a[4]/text()')[0]
            except IndexError:
                other_coach = None
 
            dirty_ppg = tree.xpath('//div[@id="info_box"]/p[3]/text()')[0].encode('utf-8')
            # for before, after in entities:
            #     dirty_ppg = dirty_ppg.replace(before, after.decode('utf-8'))
            ppg = dirty_ppg.split('&nbsp;')[0][1:-7]
            dirty_oppg = tree.xpath('//div[@id="info_box"]/p[3]/text()')[1]
            oppg = dirty_oppg[1:]
 
            dirty_arena = tree.xpath('//div[@id="info_box"]/p[4]/text()')[0].encode('utf-8')
            # for before, after in entities:
            #     dirty_arena = dirty_arena.replace(before, after.decode('utf-8'))
            arena = dirty_arena.split('&nbsp;')[0][1:-7]
            dirty_attendance = tree.xpath('//div[@id="info_box"]/p[4]/text()')[1]
            attendance = dirty_attendance[1:]
 
            try:
                playoff_part_one = tree.xpath('//div[@id="info_box"]/p[5]/text()')[1]
            except IndexError:
                playoff_part_one = None
 
            try:
                playoff_opp = tree.xpath('//div[@id="info_box"]/p[5]/a[1]/text()')[0]
            except IndexError:
                playoff_opp = None
 
            if playoff_part_one and playoff_opp:
                playoffs = playoff_part_one + playoff_opp
            else:
                playoffs = None
 
            if other_coach and playoffs:
                msg = str("%s: %s | %s (%s) | %s\nHead Coaches: %s, %s | PTS/G: %s | Opp PTS/G: %s | Arena: %s | Attendance: %s" % (nick, team_season, record, standing, playoffs, coach, other_coach, ppg, oppg, arena, attendance))
            elif other_coach and not playoffs:
                msg = str("%s: %s | %s (%s) | Did not reach the playoffs\nHead Coaches: %s, %s | PTS/G: %s | Opp PTS/G: %s | Arena: %s | Attendance: %s" % (nick, team_season, record, standing, coach, other_coach, ppg, oppg, arena, attendance))
            elif not other_coach and playoffs:
                msg = str("%s: %s | %s (%s) | %s\nHead Coach: %s | PTS/G: %s | Opp PTS/G: %s | Arena: %s | Attendance: %s" % (nick, team_season, record, standing, playoffs, coach, ppg, oppg, arena, attendance))
            else:
                msg = str("%s: %s | %s (%s) | Did not reach the playoffs\nHead Coach: %s | PTS/G: %s | Opp PTS/G: %s | Arena: %s | Attendance: %s" % (nick, team_season, record, standing, coach, ppg, oppg, arena, attendance))
 
            self.msg(channel, msg)
 
        if msg.startswith('.leaders'):
            parts = msg.split('.leaders ')
            data = parts[1]
            relevant_data = data.split(' ')
            category = str(relevant_data[0]).lower()
            try:
                year = relevant_data[1]
            except Exception:
                year = "2015"
 
            url = 'http://www.basketball-reference.com/leagues/NBA_' + year + '_leaders.html'
            try:
                page = requests.get(url, proxies = proxies)
            except Exception:
                self.msg(channel, "Not a valid year.")
            tree = html.fromstring(page.text)
 
            rank_list = []
            player_list = []
            stat_list = []
 
            try:
                cat = tree.xpath('//span[text() = "%s"]/../../table/tr' % category_dict[category])
            except Exception:
                self.msg(channel, "Categories available:\nFG%, 3P%, FT%, MPG, PPG, RPG, APG, SPG, BPG, PER, TS%, USG%, ORTG, DRTG, WS, WS/48")
 
            # table = cat.xpath('//../../table')
            # i = 1
 
            for row in cat:
                rank_list.append(row.xpath('td[1]/text()'))
                player_list.append(row.xpath('td[2]/a/text()'))
                stat_list.append(row.xpath('td[3]/text()'))
                # i = i + 1
 
            # full_rank = []
 
            for j in range(len(rank_list)):
                try:
                    float(rank_list[j][0][0])
                except Exception:
                    rank_list[j] = rank_list[j - 1]
 
            msg = category_dict[category] + " Leaders " + year + ": "
            self.msg(channel, msg)
            msg = ""
 
            for k in range(len(rank_list)):
                msg = msg + str(rank_list[k][0]) + " " + str(player_list[k][0]) + " " + str(stat_list[k][0]) + " | "
           
            self.msg(channel, msg)
 
        # if msg.startswith('.nbastandings'):
        #     parts = msg.split('.nbastandings ')
        #     data = parts[1]
        #     relevant_data = data.split(' ')
        #     divcon = str(relevant_data[0]).lower()
        #     try:
        #         year = relevant_data[1]
        #     except Exception:
        #         year = "2015"
 
        #     url = 'http://www.basketball-reference.com/leagues/NBA_' + year + '_standings.html'
        #     try:
        #         page = requests.get(url, proxies = proxies)
        #     except Exception:
        #         self.msg(channel, "Not a valid year.")
        #     tree = html.fromstring(page.text)
 
        #     try:
        #         cat = tree.xpath('//span[text() = "%s"]/../../table/tr' % category_dict[category])
        #     except Exception:
        #         self.msg(channel, "Categories available:\nFG%, 3P%, FT%, MPG, PPG, RPG, APG, SPG, BPG, PER, TS%, USG%, ORTG, DRTG, WS, WS/48")
 
        #     # table = cat.xpath('//../../table')
        #     # i = 1
 
        #     for row in cat:
        #         rank_list.append(row.xpath('td[1]/text()'))
        #         player_list.append(row.xpath('td[2]/a/text()'))
        #         stat_list.append(row.xpath('td[3]/text()'))
        #         # i = i + 1
 
        #     # full_rank = []
 
        #     for j in range(len(rank_list)):
        #         try:
        #             float(rank_list[j][0][0])
        #         except Exception:
        #             rank_list[j] = rank_list[j - 1]
 
        #     msg = category_dict[category] + " Leaders " + year + ": "
        #     self.msg(channel, msg)
        #     msg = ""
 
        #     for k in range(len(rank_list)):
        #         msg = msg + str(rank_list[k][0]) + " " + str(player_list[k][0]) + " " + str(stat_list[k][0]) + " | "
           
        #     self.msg(channel, msg)
 
 
 
class BotFactory(protocol.ClientFactory):
    protocol = Bot
 
    def __init__(self, channel, nickname='statbot'):
        self.channel = channel
        self.nickname = nickname
 
    def clientConnectionLost(self, connector, reason):
        print "Connection lost. Reason: %s" % reason
        connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason
        reactor.stop()
 
if __name__ == "__main__":
    chan = sys.argv[1]
    reactor.connectTCP('irc.freenode.net', 6667, BotFactory('#' + chan))
    reactor.run()