# Admin inputs the matches performed each week

# global variables

numMatches = 16 # int number of NFL macthes in a given week
homeTeams = [] # str list containing the home teams for each matchup
roadTeams = [] # str list conntaining the road teams for each matchup
playerPredictions = [] # int list containing a player's picks for each matchup
gameResults = [] # int list containing the results of each matchup
weeklyScore = 0 # how many matchups a player picked correctly each week
totalScore = 0 # self-explanatory

def inputMatches():
  numMatches = int(input("Enter the number of matches for this week: "))
  
  for i in range(0, numMatches):
    homeTeams[i] = input("Enter the home team for matchup " + str(i+1) + ": ")
    roadTeams[i] = input("Enter the road team for matchup " + str(i+1) + ": ")
    
  print(homeTeams)
  print(roadTeams)
