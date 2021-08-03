# player makes their predictions

def playerPredictions():
  i = 0 # counter variable
  dataString = "Your Picks/n/n" # final message to be sent

  print("Make your selections, one by one, as the bot presents them. If you make a mistake, you can make changes later.")

  while(i < numGames):
     print("Who do you think will win between ", homeTeam[i], " and ", roadTeam[i], "?")

     playerpicks[i] = input("Enter 1 for the first team and 2 for the second team: ")

     if (playerPicks[i] == 1):
       print("You predicted " + homeTeam[i])
       dataString += str(i + 1) + ". " + homeTeam[i] + "/n")
     elif (playerPicks[i] == 2):
       print("You predicted " + roadTeam[i])
       dataString += str(i + 1) + ". " + roadTeam[i] + "/n")
     else:
       while(playerPicks[i] != 1 or playerPicks[i] != 2):
          playerpicks[i] = input("Invalid input, please type 1 or 2")
   
     i += 1
    
   print(dataString)
   print("If you wish to make any changes, use ```picks edit```")

 
    
