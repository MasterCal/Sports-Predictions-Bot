# Admin inputs the matches performed each week
import GlobalVars

def inputMatches():
  GlobalVars.numMatches = int(input("Enter the number of matches for this week: "))
  
  for i in range(0, GlobalVars.numMatches):
    GlobalVars.homeTeams.append(input("Enter the home team for matchup " + str(i+1) + ": "))
    GlobalVars.roadTeams.append(input("Enter the road team for matchup " + str(i+1) + ": "))
    
  print(GlobalVars.homeTeams)
  print(GlobalVars.roadTeams)
