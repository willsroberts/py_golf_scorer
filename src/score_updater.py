import gspread
from oauth2client.service_account import ServiceAccountCredentials
import score_builder
import time
import sys
from datetime import date

def get_player_locations(p_list,sheet):
    p_loc = {}
    for player in p_list:
        plz = sheet.findall(player)
        p_loc[player] = (plz[0].row, plz[0].col)
    return p_loc

def update_day_net(p_list,p_locs,scores,sheet,day):
    if day == 3:
        for p in p_list:
            loc = p_locs[p]
            sheet.update_cell(row=loc[0],col=loc[1]+1,val=scores[p]['round_1'])
        print "DAY {} UPDATED: {}".format(day, date.today())
    if day == 4:
        for p in p_list:
            loc = p_locs[p]
            sheet.update_cell(row=loc[0],col=loc[1]+2,val=scores[p]['round_2'])
        print "DAY {} UPDATED: {}".format(day, date.today())
    if day == 5:
        for p in p_list:
            loc = p_locs[p]
            sheet.update_cell(row=loc[0],col=loc[1]+3,val=scores[p]['round_3'])
        print "DAY {} UPDATED: {}".format(day, date.today())
    if day == 6:
        for p in p_list:
            loc = p_locs[p]
            sheet.update_cell(row=loc[0],col=loc[1]+4,val=scores[p]['round_4'])
        print "DAY {} UPDATED: {}".format(day, date.today())

def update_board_net(tourn_name, player_list, parsed_board, book):
    sheet = book.worksheet("Scores")
    p_locs = get_player_locations(player_list, sheet)
    player_scores = score_builder.build_player_scores_net(p_list=player_list,prsed_json=parsed_board)
    update_day_net(p_list=player_list, p_locs=p_locs, scores=player_scores, sheet=sheet, day=date.today().weekday())

def update_board_bball(tourn_name, player_list, parsed_board):
    player_scores = score_builder.build_player_scores_bestball(p_list=player_list,prsed_json=parsed_board)
    update_day_bball(p_list=player_list, scores=player_scores, book=wbook, day=date.today().weekday())

def update_row(sheet,loc,score_list):
    i = loc[1]+1
    for hole in score_list:
        sheet.update_cell(loc[0],i,hole)
        i += 1
    print "ROW UPDATED ON {}".format(sheet)

def update_day_bball(p_list,scores,book,day):
    if day == 3:
        sheet = book.worksheet("First Round")
        p_locs = get_player_locations(p_list,sheet)
        for p in p_list:
            loc = p_locs[p]
            update_row(sheet=sheet,loc=loc,score_list=scores[p]['round_1'])
        print "DAY {} UPDATED: {}".format(day-2, date.today())
    if day == 4:
        sheet = book.worksheet("Second Round")
        p_locs = get_player_locations(p_list,sheet)
        for p in p_list:
            loc = p_locs[p]
            update_row(sheet=sheet,loc=loc,score_list=scores[p]['round_2'])
        print "DAY {} UPDATED: {}".format(day-2, date.today())
    if day == 5:
        sheet = book.worksheet("Third Round")
        p_locs = get_player_locations(p_list,sheet)
        for p in p_list:
            loc = p_locs[p]
            update_row(sheet=sheet,loc=loc,score_list=scores[p]['round_3'])
        print "DAY {} UPDATED: {}".format(day-2, date.today())
    if day == 6:
        sheet = book.worksheet("Final Round")
        p_locs = get_player_locations(p_list,sheet)
        for p in p_list:
            loc = p_locs[p]
            update_row(sheet=sheet,loc=loc,score_list=scores[p]['round_4'])
        print "DAY {} UPDATED: {}".format(day-2, date.today())


def decide_tournament_type(workbook):
    titles = [t.title.lower() for t in workbook.worksheets()]
    if ('first round' in titles) and ('second round' in titles) and ('third round' in titles):
        return "bball"
    else:
        return "net"

def command_line_players():
    try:
        p_list = score_builder.get_player_list(sys.argv[-4:])
    except getopt.GetoptError:
        print "bad arg: python <tourn_name> <play_1,play_2,play_3,play4>"
    else:
        return score_builder.get_player_list(p_list)

if __name__ == "__main__":
    current_milli_time = lambda: int(round(time.time() * 1000))
    htm = "http://www.pgatour.com/data/r/041/2017/leaderboard-v2.json?ts=" + str(current_milli_time())
    parsed_board = score_builder.get_parse_leaderboard(htm)
    player_list = command_line_players()

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('../config/client_secret.json',scope)
    client = gspread.authorize(creds)

    tourn_name = sys.argv[-5]
    wbook = client.open(tourn_name)

    ttype = decide_tournament_type(wbook)

    if ttype == "bball":
        update_board_bball(tourn_name=tourn_name,player_list=player_list,parsed_board=parsed_board)
    elif ttype == "net":
        update_board_net(tourn_name=tourn_name,player_list=player_list,parsed_board=parsed_board,book=wbook)
    else:
        print "CHECK WORK BOOK TABS: {}".format(wbook.worksheets())
