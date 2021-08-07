# reset weekly picks so admin can enter the next week's matchups

import GlobalVars

def clear():
    GlobalVars.homeTeams = []
    GlobalVars.roadTeams = []
    GlobalVars.playerPicks = []
    GlobalVars.gameResults = []
    GlobalVars.weeklyScore = 0
