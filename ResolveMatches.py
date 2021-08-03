# admin inputs results of the matches, and scores are calculated

def resolvePredictions():
  dataString = "Results/n/n" #cresults of the matches
  leaderboard = "" # weekly and total leaderboards
  
  for i in range(0, numMatches):
    gameResults.append(int(input("Who won between " + homeTeam[i] + " and " + roadTeam[i] + "? "))) # 1 for home, 2 for away, 0 for a tie
    
    if (gameResults[i] == 0): # match is a draw
      weeklyScore += 0.5
      totalScore += 0.5
      dataString += homeTeam[i] + " and " + roadTeam[i] + " tied/n"
    elif (gameResults[i] == playerPicks[i]): # correct prediction
      weeklyScore += 1
      totalScore += 1
      
    if (gameResults[i] == 1):
      dataString += homeTeam[i] + " def. " + roadTeam[i] + "\n"
    elif (gameResults[i] == 2):
      dataString += roadTeam[i] + " def. " + homeTeam[i] + "\n"
      
  print(dataString)
  
  leaderboard += "Weekly Score/n/n" 
  leaderboard += weeklyScore
  leaderboard += "/n/nTotal Score"
  leaderboard += totalScore
  
  print(leaderboard)
    
