# player makes their predictions
import GlobalVars

def playerPredictions():
  i = 0 # counter variable
  dataString = "Your Picks\n\n" # final message to be sent

  print("\nMake your selections, one by one, as the bot presents them. If you make a mistake, you can make changes later.\n")
  while(i < GlobalVars.numMatches):
    print("Who do you think will win between " + GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + "?")
    GlobalVars.playerPicks.append(input("Enter 1 for the first team and 2 for the second team: "))
    while True:
      try:
        GlobalVars.playerPicks[i] = int(GlobalVars.playerPicks[i])
        if (GlobalVars.playerPicks[i] != 1 and GlobalVars.playerPicks[i] != 2):
          raise Exception
      except Exception:
        GlobalVars.playerPicks[i] = input("Invalid int input, please type 1 or 2: ")
      except ValueError:
        GlobalVars.playerPicks[i] = input("Invalid value input, please type 1 or 2: ")
      else:
        if (GlobalVars.playerPicks[i] == 1): # print the player's pick
          print("You predicted " + GlobalVars.homeTeams[i])
          dataString += str(i+1) + ". " + GlobalVars.homeTeams[i] + "\n"
        elif (GlobalVars.playerPicks[i] == 2):
          print("You predicted " + GlobalVars.roadTeams[i])
          dataString += str(i+1) + ". " + GlobalVars.roadTeams[i] + "\n"
        break
        
    i += 1
     
  print(dataString)
  print("If you wish to make any changes, use picks edit")
