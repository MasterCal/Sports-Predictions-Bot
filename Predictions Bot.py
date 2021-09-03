#predictionsbot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import logging
import GlobalVars
import Multiplayer
from keep_alive import keep_alive
import datetime
import pytz
from replit import db

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="picks ")

def updateDatabase():
  db["numMatches"] = GlobalVars.numMatches
  db["homeTeams"] = GlobalVars.homeTeams
  db["roadTeams"] = GlobalVars.roadTeams
  db["gameResults"] = GlobalVars.gameResults
  db["canMakePicks"] = GlobalVars.canMakePicks
  db["canEdit"] = GlobalVars.canEdit
  db["ongoingEvent"] = GlobalVars.ongoingEvent
  db["gameDays"] = GlobalVars.gameDays
  db["gameHours"] = GlobalVars.gameHours
  db["gameMinutes"] = GlobalVars.gameMinutes
  db["playerList"] = Multiplayer.playerList
  db["playerCount"] = Multiplayer.playerCount

def channelcheck(): # commands used only in proper channels
    async def predicate(ctx):
        return ctx.channel.id in [873684361910812713, 570670688310919228, 880591215697997824]
    return commands.check(predicate)

def playercheck(ctx):
    for i in range(0, Multiplayer.playerCount):
        if(ctx.author.id == Multiplayer.playerList[i].playerID):
            return True
    return False

def getPlayerNumber(ctx):
    for i in range(0, Multiplayer.playerCount):
        if (Multiplayer.playerList[i].playerID == ctx.message.author.id):
            return i

def picksTimeCheck():
  timeZone = pytz.timezone("US/Pacific")
  currentTime = datetime.datetime.now(timeZone)
  dayOfWeek = datetime.date.today().weekday()
  print(currentTime)

  if(dayOfWeek >= GlobalVars.gameDays[0]):
    if(currentTime.hour > GlobalVars.gameHours[0] - 1):
      return False
    elif(currentTime.hour == GlobalVars.gameHours[0] - 1):
      if(currentTime.minute >= GlobalVars.gameMinutes[0]):
        return False
      else:
        return True
    else:
      return True
  else:
    return True
  return True

def editTimeCheck(num):
  timeZone = pytz.timezone("US/Pacific")
  currentTime = datetime.datetime.now(timeZone)
  dayOfWeek = datetime.date.today().weekday()

  if(dayOfWeek >= GlobalVars.gameDays[num]):
    if(currentTime.hour > GlobalVars.gameHours[num] - 1):
      return False
    elif(currentTime.hour == GlobalVars.gameHours[num] - 1):
      if(currentTime.minute >= GlobalVars.gameMinutes[num]):
        return False
      else:
        return True
    else:
      return True
  else:
    return True
  return True

@bot.command(name="hello")
@channelcheck()
async def testhello(ctx):
    response = "Hello, yourself"
    await ctx.send(response)

@bot.command(name="start")
@channelcheck()
@commands.has_any_role("General Manager")
async def startEvent(ctx):
    if(GlobalVars.ongoingEvent == True):
        await ctx.send("An event is already in progress")
        return
    else:
        Multiplayer.playerList.append(Multiplayer.Multiplayer(ctx))
        Multiplayer.playerCount += 1
        await ctx.send("An event has been started in this channel.")
        GlobalVars.ongoingEvent = True
        updateDatabase()
        
@bot.command(name="signup")
@channelcheck()
@commands.max_concurrency(1, wait=True)
async def signup(ctx):
    if (GlobalVars.ongoingEvent == False):
        await ctx.send("No event is going on at this time.")
        return
    else:
        for i in range(0, Multiplayer.playerCount):
            if(ctx.author.id == Multiplayer.playerList[i].playerID):
                await ctx.send("You have already signed up for this event.")
                return 

    Multiplayer.playerList.append(Multiplayer.Multiplayer(ctx))
    Multiplayer.playerCount += 1
    await ctx.send("Successfully signed up!")
    for i in range(0, Multiplayer.playerCount):
        await ctx.send("{}".format(Multiplayer.playerList[i].username))

    if(GlobalVars.canMakePicks == True):
      Multiplayer.playerList[Multiplayer.playerCount-1].canMakePicks = True
    
    updateDatabase()

@bot.command(name="input")
@channelcheck()
@commands.has_any_role("General Manager")
async def inputGames(ctx):
    await ctx.send("Enter the number of matches for this week.")

    def check(message):
        return message.channel.id == ctx.channel.id and message.author.id == ctx.author.id
    try:
        message = await bot.wait_for("message", timeout=30, check=check)
    except asyncio.TimeoutError:
        return
    GlobalVars.numMatches = int(message.content)
  
    for i in range(0, GlobalVars.numMatches):
      await ctx.send("Enter the home team for matchup " + str(i + 1))
      try:
          message = await bot.wait_for("message", timeout=30, check=check)
      except asyncio.TimeoutError:
          return
      GlobalVars.homeTeams.append(message.content)

      await ctx.send("Enter the road team for matchup " + str(i + 1))
      try:
          message = await bot.wait_for("message", timeout=30, check=check)
      except asyncio.TimeoutError:
          return
      GlobalVars.roadTeams.append(message.content)

      await ctx.send("Enter the day of this matchup (0-Monday)")
      try:
        message = await bot.wait_for("message", timeout=30, check=check)
      except asyncio.TimeoutError:
        return
      GlobalVars.gameDays.append(int(message.content))

      await ctx.send("Enter the hour of this matchup (24-hr)")
      try:
        message = await bot.wait_for("message", timeout=30, check=check)
      except asyncio.TimeoutError:
        return
      GlobalVars.gameHours.append(int(message.content))

      await ctx.send("Enter the minute of this matchup")
      try:
        message = await bot.wait_for("message", timeout=30, check=check)
      except asyncio.TimeoutError:
        return
      GlobalVars.gameMinutes.append(int(message.content))


    GlobalVars.canMakePicks = True

    for i in range(0, Multiplayer.playerCount):
        Multiplayer.playerList[i].canMakePicks = True
        
    updateDatabase()

    await ctx.send("Picks can be made now.")

@bot.command(name="make")
@channelcheck()
@commands.max_concurrency(1, wait=False)
async def playerPredictions(ctx):
    isPlayer = playercheck(ctx)
    if(isPlayer == False):
        if(GlobalVars.ongoingEvent == True):
           await ctx.send("You are not signed up for this event")
           return
        else:
            await ctx.send("No event is going on at this time")
            return

    playerNum = getPlayerNumber(ctx)

    if (GlobalVars.canMakePicks == False):
        await ctx.send("Picks cannot be made at this time, wait for an admin to input them, or you are too late.")
        return

    if(Multiplayer.playerList[playerNum].canMakePicks == False):
        await ctx.send("You have already made picks for this week. You can edit them using `picks edit`.")
        return

    timeCheck = picksTimeCheck()
    if(timeCheck == False):
      await ctx.send("You are too late to make picks")
      GlobalVars.canMakePicks = False
      return

    dataString = str(Multiplayer.playerList[playerNum].username) + "'s Picks\n\n"

    def check(message):
        return message.channel.id == ctx.channel.id and message.author.id == ctx.author.id

    await ctx.send("Make your picks, one by one, as the bot presents them. If you make a mistake, you can make changes later.")
    for i in range(0, GlobalVars.numMatches):
      await ctx.send("Who do you think will win between " + GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + "? (Enter 1 for the first team and 2 for the second team)")
      while True:
        try:
          message = await bot.wait_for("message", timeout=30, check=check)
          if message.content != '1' and message.content != '2':
            raise Exception
        except asyncio.TimeoutError:
          return
        except Exception:
          await ctx.send("Please type 1 or 2") 
        else:
          Multiplayer.playerList[playerNum].playerPicks.append(int(message.content))
          if (Multiplayer.playerList[playerNum].playerPicks[i] == 1):
            await ctx.send("You predicted " + GlobalVars.homeTeams[i])
            dataString += str(i+1) + ". " + GlobalVars.homeTeams[i] + "\n"
          elif (Multiplayer.playerList[playerNum].playerPicks[i] == 2):
            await ctx.send("You predicted " + GlobalVars.roadTeams[i])
            dataString += str(i+1) + ". " + GlobalVars.roadTeams[i] + "\n"
          break

    await ctx.send(dataString)
    
    Multiplayer.playerList[playerNum].canMakePicks = False
    Multiplayer.playerList[playerNum].canEdit = True
    updateDatabase()
    
    await ctx.send("If you wish to make any changes, use `picks edit`")

@bot.command(name="resolve")
@channelcheck()
@commands.has_any_role("General Manager")
async def resolveMatches(ctx):
    dataString = "**__Results__**\n\n"
    leaderboard = "\n**__This Week's Score__**\n\n"

    for i in range(0, GlobalVars.numMatches):
        await ctx.send("Who won between " + GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + "?")

        def check(message):
            return message.channel.id == ctx.channel.id and message.author.id == ctx.author.id

        try:
            message = await bot.wait_for("message", timeout=30, check=check)
            GlobalVars.gameResults.append(int(message.content))
        except asyncio.TimeoutError:
            return
        else:
            for x in range(0, Multiplayer.playerCount):
               if (GlobalVars.gameResults[i] == 0): # match is a draw
                  Multiplayer.playerList[x].weeklyScore += 0.5
                  Multiplayer.playerList[x].totalScore += 0.5
               elif (GlobalVars.gameResults[i] == Multiplayer.playerList[x].playerPicks[i]):
                  Multiplayer.playerList[x].weeklyScore += 1
                  Multiplayer.playerList[x].totalScore += 1

            if (GlobalVars.gameResults[i] == 1):
                 dataString += GlobalVars.homeTeams[i] + " def. " + GlobalVars.roadTeams[i] + "\n"
            elif (GlobalVars.gameResults[i] == 2):
                  dataString += GlobalVars.roadTeams[i] + " def. " + GlobalVars.homeTeams[i] + "\n"
            elif (GlobalVars.gameResults[i] == 0):
                  dataString += GlobalVars.homeTeams[i] + " and " + GlobalVars.roadTeams[i] + " tied.\n"

    await ctx.send(dataString)

    for i in range(0, Multiplayer.playerCount):
        leaderboard += Multiplayer.playerList[i].username + ": " + str(Multiplayer.playerList[i].weeklyScore) + " points\n"

    leaderboard += "\n**__Total Score__**\n\n"

    for i in range(0, Multiplayer.playerCount):
        leaderboard += Multiplayer.playerList[i].username + ": " + str(Multiplayer.playerList[i].totalScore) + " points\n"

    updateDatabase()
    
    await ctx.send(leaderboard)
                
@bot.command(name="edit")
@channelcheck()
@commands.max_concurrency(1, wait=False)
async def editPicks(ctx):
    isPlayer = playercheck(ctx)
    if(isPlayer == False):
        if(GlobalVars.ongoingEvent == True):
           await ctx.send("You are not signed up for this event")
           return
        else:
            await ctx.send("No event is going on at this time")
            return

    playerNum = getPlayerNumber(ctx)

    if(Multiplayer.playerList[playerNum].canEdit == False):
        await ctx.send("You have not made picks for this week. Use `picks make` to make predictions.")
        return

    ans = "" # does player want to edit
    number = 0 # which game does player want to edit
    conf = "" # verify player wants to make the change
    dataString = "Your Picks\n\n" # display updated predictions

    def check(message):
        return message.channel.id == ctx.channel.id and message.author.id == ctx.author.id

    await ctx.send("Do you want to change a pick? Type y for yes or n for no.")
    while True:
       try:
           message = await bot.wait_for("message", timeout=30, check=check)
           ans = message.content
           if (ans.lower() != 'y' and ans.lower() != 'n'):
               raise Exception
       except Exception:
           await ctx.send("Improper input, please type y or n (Non case-sensitive).")
       except asyncio.TimeoutError:
           return
       else:
           break

    if(ans.lower() == 'n'):
        await ctx.send("You have exited the editing process.")
        return
    else:
        while(ans.lower() == 'y'):
            await ctx.send("Which prediction would you like to change? Type in the corresponding number for the game which pick you will change.")
            while True:
                try:
                    message = await bot.wait_for("message", timeout=30, check=check)
                    number = int(message.content)
                    if (int(number) > GlobalVars.numMatches or int(number) < 1):
                        raise Exception # a game that does not exist
                except Exception:
                        await ctx.send("Please enter a valid match number.")
                except asyncio.TimeoutError:
                        return
                else:
                    timecheck = editTimeCheck(number-1)
                    if(timecheck == False):
                      await ctx.send("This game is within an hour of starting or has already started, so your pick can't be changed.")
                      return
                    if(Multiplayer.playerList[playerNum].playerPicks[number-1] == 1):
                        await ctx.send("You will be changing your pick from " + GlobalVars.homeTeams[number-1] + " to " + GlobalVars.roadTeams[number-1] + ".")
                    elif(Multiplayer.playerList[playerNum].playerPicks[number-1] == 2):
                        await ctx.send("You will be changing your pick from " + GlobalVars.roadTeams[number-1] + " to " + GlobalVars.homeTeams[number-1] + ".")

                    break

            await ctx.send("Are you sure you want to make this change? [Y/N]")
            while True:
                try:
                    message = await bot.wait_for("message", timeout=30, check=check)
                    conf = message.content
                    if(conf.lower() != 'y' and conf.lower() != 'n'):
                        raise Exception
                except Exception:
                        await ctx.send("Improper input, please type y or n (Non case-sensitive).")
                except asyncio.TimeoutError:
                        return
                else:
                    if(conf.lower() == 'y'):
                        if(Multiplayer.playerList[playerNum].playerPicks[number-1] == 1):
                            Multiplayer.playerList[playerNum].playerPicks[number-1] = 2
                        elif(Multiplayer.playerList[playerNum].playerPicks[number-1] == 2):
                            Multiplayer.playerList[playerNum].playerPicks[number-1] = 1
                        else:
                            break

                    break

            await ctx.send("Do you wish to change another pick? [y/n]")
            while True:
                try:
                    message = await bot.wait_for("message", timeout=30, check=check)
                    ans = message.content
                    if(ans.lower() != 'y' and ans.lower() != 'n'):
                        raise Exception
                except Exception:
                    await ctx.send("Improper input, please type y or n (Non case-sensitive).")
                except asyncio.TimeoutError:
                    return
                else:
                    if(ans.lower() == 'n'):
                        await ctx.send("You have exited the editing method.")
                        break
                    else:
                        break

    for i in range(0, GlobalVars.numMatches):
        dataString += str(i+1) + ". "
        if(Multiplayer.playerList[playerNum].playerPicks[i] == 1):
            dataString += GlobalVars.homeTeams[i] + "\n"
        elif(Multiplayer.playerList[playerNum].playerPicks[i] == 2):
            dataString += GlobalVars.roadTeams[i] + "\n"

    updateDatabase()
    
    await ctx.send(dataString)

@bot.command(name="clear")
@channelcheck()
@commands.has_any_role("General Manager")
async def clear(ctx):
    GlobalVars.numMatches = 0
    GlobalVars.homeTeams = []
    GlobalVars.roadTeams = []
    GlobalVars.gameResults = []

    for i in range(0, Multiplayer.playerCount):
        Multiplayer.playerList[i].playerPicks = []
        Multiplayer.playerList[i].weeklyScore = 0
        Multiplayer.playerList[i].canEdit = False

    GlobalVars.canMakePicks = False

    await ctx.send("Data successfully cleared")
    
    updateDatabase()

@bot.command(name="delete")
@channelcheck()
@commands.has_any_role("General Manager")
async def delete(ctx):
    GlobalVars.ongoingEvent = False
    GlobalVars.numMatches = 0
    GlobalVars.homeTeams = []
    GlobalVars.roadTeams = []
    Multiplayer.playerList = []
    Multiplayer.playerCount = 0
    GlobalVars.gameResults = []
    GlobalVars.canMakePicks = False
    GlobalVars.canEdit = False
    
    updateDatabase()

    await ctx.send("Event successfully ended, all data has been deleted")

@bot.command(name="playerlist")
@channelcheck()
async def showPlayerList(ctx):
    players = ""
    
    if(GlobalVars.ongoingEvent == True):
        for i in range(0, Multiplayer.playerCount):
            players += Multiplayer.playerList[i].username

        await ctx.send(players)
    else:
        await ctx.send("No event is going on at this time")

@bot.command(name="mypicks")
@channelcheck()
async def showMyPicks(ctx):
    if(GlobalVars.ongoingEvent == False):
        await ctx.send("No event is going on at this time.")
        return
    else:
        isPlayer = playercheck(ctx)
        if(isPlayer == False):
           await ctx.send("You are not signed up for this event")
           return
        
        playerNum = getPlayerNumber(ctx)

        picks = str(Multiplayer.playerList[playerNum].username) + "'s Picks\n\n"

        try:
            if(Multiplayer.playerList[playerNum].playerPicks[0] == 1 or Multiplayer.playerList[playerNum].playerPicks[0] == 2):
               picks = str(Multiplayer.playerList[playerNum].username) + "'s Picks\n\n"
        except Exception:
            await ctx.send("You have not made any picks yet. Use `picks make` to make your picks.")
            return

        for i in range(0, GlobalVars.numMatches):
            if(Multiplayer.playerList[playerNum].playerPicks[i] == 1):
                picks += str(i+1) + ". " + GlobalVars.homeTeams[i] + "\n"
            else:
                picks += str(i+1) + ". " + GlobalVars.roadTeams[i] + "\n"

        await ctx.send(picks)
        
@bot.command(name="refresh")
@channelcheck()
@commands.has_any_role("General Manager")
async def refreshData(ctx):
  GlobalVars.numMatches = db["numMatches"]
  GlobalVars.homeTeams = db["homeTeams"]
  GlobalVars.roadTeams = db["roadTeams"]
  GlobalVars.gameResults = db["gameResults"]
  GlobalVars.canMakePicks = db["canMakePicks"]
  GlobalVars.canEdit = db["canEdit"]
  GlobalVars.ongoingEvent = db["ongoingEvent"]
  GlobalVars.gameDays = db["gameDays"]
  GlobalVars.gameHours = db["gameHours"]
  GlobalVars.gameMinutes = db["gameMinutes"]
  Multiplayer.playerList = db["playerList"]
  Multiplayer.playerCount = db["playerCount"]
  
  await ctx.send("Data successfully refreshed")
           
keep_alive()

bot.run(TOKEN)
