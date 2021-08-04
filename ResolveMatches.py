# admin inputs results of the matches, and scores are calculated

def resolvePredictions():
 dataString = "Results/n/n" #cresults of the matches
 leaderboard = "" # weekly and total leaderboards
  
  for i in range(0, GlobalVars.numMatches):
    GlobalVars.gameResults.append(int(input("Who won between " + GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + "? "))) # 1 for home, 2 for away, 0 for a tie
    
    if (GlobalVars.gameResults[i] == 0): # match is a draw
      GlobalVars.weeklyScore += 0.5
      GlobalVars.totalScore += 0.5
      dataString += GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + " tied/n"
    elif (GlobalVars.gameResults[i] == GlobalVars.playerPicks[i]): # correct prediction
      GlobalVars.weeklyScore += 1
      GlobalVars.totalScore += 1
      
    if (GlobalVars.gameResults[i] == 1):
      dataString += GlobalVars.homeTeams[i] + " def. " + GlobalVars.roadTeams[i] + "\n"
    elif (gameResults[i] == 2):
      dataString += GlobalVars.roadTeams[i] + " def. " + GlobalVars.homeTeams[i] + "\n"
      
  print(dataString)
  
  leaderboard += "Weekly Score/n/n" 
  leaderboard += GlobalVars.weeklyScore
  leaderboard += "/n/nTotal Score"
  leaderboard += GlobalVars.totalScore
  
  print(leaderboard)
    
