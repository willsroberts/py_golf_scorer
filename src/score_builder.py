from bs4 import BeautifulSoup
from datetime import date
import numpy as np
import json
import requests
import sys
import time


def get_parse_leaderboard(html):
    p = requests.get(html)
    return json.loads(p.text)

def get_player_list(p_list=[]):
    if not p_list:
        i = 0
        while i < 4:
            player = raw_input("Player List: ")
            p_list.append(player)
            i += 1
        return p_list
    else:
        return p_list

def build_player_scores_bestball(p_list, prsed_json):
    player_scores = {}
    for plyer in prsed_json['leaderboard']['players']:
        player_nm = plyer['player_bio']['first_name'] + " " + plyer['player_bio']['last_name']
        if player_nm in p_list:
            player_scores[player_nm] = {'round_1':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 'round_2':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 'round_3':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 'round_4':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}

            day = date.today().weekday()
            if day == 3:
                i = 0
                for hole in plyer['holes']:
                    player_scores[player_nm]['round_1'][i] = hole['strokes']
                    i += 1
            if day == 4:
                i = 0
                for hole in plyer['holes']:
                    player_scores[player_nm]['round_2'][i] = hole['strokes']
                    i += 1
            if day == 5:
                i = 0
                for hole in plyer['holes']:
                    player_scores[player_nm]['round_3'][i] = hole['strokes']
                    i += 1
            if day == 6:
                i = 0
                for hole in plyer['holes']:
                    player_scores[player_nm]['round_4'][i] = hole['strokes']
                    i += 1
    return player_scores

def build_course_par(prsed_json):
    course_par = []
    for hole in prsed_json['leaderboard']['players'][0]['holes']:
        course_par.append(hole['par'])
    return course_par

def build_player_scores_net(p_list, prsed_json):
    strokes = build_player_scores_bestball(p_list=p_list,prsed_json=prsed_json)
    player_scores_net = {}

    course = np.array(build_course_par(prsed_json))
    '''
    Scores{Player:{round:[]}}
    '''

    for plyer in prsed_json['leaderboard']['players']:
        player_nm = plyer['player_bio']['first_name'] + " " + plyer['player_bio']['last_name']
        if player_nm in p_list:
             player_scores_net[player_nm] = {'round_1':0, 'round_2':0, 'round_3':0, 'round_4':0}
             for k,v in strokes[player_nm].iteritems():
                 sumd = 0
                 for a,b in zip(v,course):
                     if a != None and a != 0:
                         sumd += a - b
                 player_scores_net[player_nm][k] = sumd

    return player_scores_net
