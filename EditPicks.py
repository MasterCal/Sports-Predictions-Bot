# players can make changes to their picks, if they make a mistake, or they change their mind

import GlobalVars

def edit():
  ans = "" # does player want to edit
  number = 0 # which game does player want to edit
  conf = "" # check that player does want to change
  dataString = "Your Picks\n\n" # display updated predictions

  ans = input("Do you want to change a pick? Type y for yes or n for no. ")
  while(ans != 'Y' and ans != 'y' and ans != 'N' and ans != 'n'):
    ans = input("Improper input, please type y or n (Non-case sensitive). ")
  
  while(ans == 'Y' or ans == 'y'):
    number = input("Which prediction would you like to change? Type in the corresponding number.")
    while True:
      try:
        number = int(number)
        if(number > GlobalVars.numMatches):
          raise Exception # try to edit a game that does not exist
      except Exception:
        number = input("Please enter a valid match number")
      else:
        if(GlobalVars.playerPicks[number-1] == 1):
          print("You will be changing your pick from " + GlobalVars.homeTeams[i] + " to " + GlobalVars.roadTeams[i] + ".")
        elif(GlobalVars.playerPicks[number-1] == 2):
          print("You will be changing your pick from " + GlobalVars.roadTeams[i] + " to " + GlobalVars.homeTeams[i] + ".")
          
        conf = input("Are you sure you want to make this change?")
        while(conf != 'Y' and conf != 'y' and conf != 'N' and conf != 'n'):
          conf = input("Improper input, please type y or n (Non-case sensitive). ")
            
        if(conf == 'Y' or conf == 'y'):
          if(GlobalVars.playerPicks[number-1] == 1):
            GlobalVars.playerPicks[number-1] == 2
          elif(GlobalVars.playerPicks[number-1] == 2):
            GlobalVars.playerPicks[number-1] == 1
         else:
          break
          
      break      
          
    ans = input("Do you wish to change another pick? ")  
    
  for i in range(0, GlobalVars.numMatches):
    dataString += str(i+1) + ". "
    if(GlobalVars.playerPicks[i] == 1):
      dataString += GlobalVars.homeTeams[i] + "\n"
    elif(GlobalVars.playerPicks[i] == 2):
      dataString += GlobalVars.homeTeams[i]) + "\n"    
 
 print(dataString)  
