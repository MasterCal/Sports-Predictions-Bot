playerList = []
playerCount = 0

class Multiplayer:
  def __init__(self, ctx):
       self.playerID = ctx.author.id
       self.username = str(ctx.author).split('#')[0]
       self.playerPicks = []
       self.weeklyScore = 0
       self.totalScore = 0
       self.canMakePicks = False
       self.canEdit = False
        
