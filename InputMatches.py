# Admin inputs the matches performed each week

def inputMatches():
  numMatches = int(input("Enter the number of matches for this week: "))
  
  for i in range(0, numMatches):
    homeTeams.append(input("Enter the home team for matchup " + str(i+1) + ": "))
    roadTeams.append(input("Enter the road team for matchup " + str(i+1) + ": "))
    
  print(homeTeams)
  print(roadTeams)
