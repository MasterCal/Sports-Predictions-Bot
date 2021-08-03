# Admin inputs the matches performed each week

# global variables

numMatches # int number of NFL macthes in a given week
homeTeams[16] # str list containing the home teams for each matchup
roadTeams[16] # str list conntaining the road teams for each matchup
playerPredictions[16] # int list containing a player's picks for each matchup
gameResults[16] # int list containing the results of each matchup
weeklyScore # how many matchups a player picked correctly each week
totalScore # self-explanatory

def inputMatches():
  numMatches = int(input("Enter the number of matches for this week: "))
  
  for i in range(0, numMatches):
    homeTeams[i] = input("Enter the home team for matchup " + str(i+1) + ": ")
    roadTeams[i] = input("Enter the road team for matchup " + str(i+1) + ": ")
    
  print(homeTeams)
  print(roadTeams)
