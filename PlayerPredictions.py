# player makes their predictions

def playerPredictions():
  global numGames
  global homeTeams
  global roadTeams
  global playerPicks
  
  i = 0 # counter variable
  dataString = "Your Picks/n/n" # final message to be sent

  print("Make your selections, one by one, as the bot presents them. If you make a mistake, you can make changes later.")

  while(i < numGames):
     print("Who do you think will win between ", homeTeams[i], " and ", roadTeams[i], "?")

     playerpicks.append(input("Enter 1 for the first team and 2 for the second team: "))

     if (playerPicks[i] == 1):
       print("You predicted " + homeTeams[i])
       dataString += str(i) + ". " + homeTeams[i] + "/n"
     elif (playerPicks[i] == 2):
       print("You predicted " + roadTeams[i])
       dataString += str(i) + ". " + roadTeams[i] + "/n"
     else:
       while(playerPicks[i] != 1 or playerPicks[i] != 2):
          playerPicks[i] = input("Invalid input, please type 1 or 2")
   
     i += 1
    
  print(dataString)
  print("If you wish to make any changes, use ```picks edit```")

 
    
