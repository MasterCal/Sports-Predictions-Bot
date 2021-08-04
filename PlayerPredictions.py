# player makes their predictions
import GlobalVars

def playerPredictions():
  i = 0 # counter variable
  dataString = "Your Picks/n/n" # final message to be sent

  print("/nMake your selections, one by one, as the bot presents them. If you make a mistake, you can make changes later./n")

  while(i < GlobalVars.numMatches):
     print("Who do you think will win between " + GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + "?")

     GlobalVars.playerPicks.append(int(input("Enter 1 for the first team and 2 for the second team: ")))

     if (GlobalVars.playerPicks[i] == 1):
       print("You predicted " + GlobalVars.homeTeams[i])
       dataString += str(i) + ". " + GlobalVars.homeTeams[i] + "/n"
     elif (GlobalVars.playerPicks[i] == 2):
       print("You predicted " + GlobalVars.roadTeams[i])
       dataString += str(i) + ". " + GlobalVars.roadTeams[i] + "/n"
     else:
       while(GlobalVars.playerPicks[i] != 1 or GlobalVars.playerPicks[i] != 2):
          GlobalVars.playerPicks[i] = input("Invalid input, please type 1 or 2: ")
   
     i += 1
    
  print(dataString)
  print("If you wish to make any changes, use picks edit")

 
    
