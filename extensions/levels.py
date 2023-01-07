#Global Imports
import sys,os,time,re,random,nextcord,inspect
#Specific Imports
from nextcord.ext import commands,application_checks
from nextcord import Interaction,ClientCog
from nextcord.ext.application_checks import *

from dotenv import load_dotenv
from colorama import Fore, Back, Style
from  Internal import database,console,utilities,permissions

load_dotenv()

LevelXP = 1000
WordXP = 10
MinimumLevel = 1



class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Commands
    @nextcord.slash_command(name="level",description="Show your level data")
    async def LevelCheck(self, interaction: nextcord.Interaction):
        xplevel = await DoesUserHaveDBEntry(interaction.user.id,interaction.guild.id)
        try:
            xp = int(xplevel[0][0])
            level = int(xplevel[0][1])
        except:
            xp = 0
            level = MinimumLevel
        try:
            await interaction.response.send_message(f"Your Level is {str(level)}, you have {str(xp)}/{str(LevelXP * level)} XP of the required XP to level up!",ephemeral=True)
        except Exception as e:
            console.print_error(e)
            await interaction.response.send_message(f"Your Level is {str(level)}, you have {str(xp)}/{str(LevelXP * level)} XP of the required XP to level up!",ephemeral=True)

    @nextcord.slash_command(name="addxp",description="Add XP to a user")
    async def add_xp_command(self, interaction: nextcord.Interaction, mention: str, xp: int):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            user_id = utilities.process_mention(mention)
            if user_id:
                user = await utilities.mention_user(self,user_id,interaction.guild.id)
                await interaction.send(f'{user.mention} is getting {xp} xp added!')
                await AwardXP(self,user_id,interaction.guild_id,xp,interaction)
            else:
                await interaction.send('Invalid mention',ephemeral=True)
        else:
            await interaction.send('You do not have permission to use this command',ephemeral=True)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await AwardWordXP(message)




def setup(client):
    client.add_cog(Levels(client))




#Functions
async def DoesUserHaveDBEntry(UserID,GuildID):
    try:
        xplevel = await database.ReadTable(query=f"SELECT XP,Level FROM Levels WHERE UserID = {UserID}",database=f"{GuildID}_Discord")
    except:
        console.print_warning(f"Creating new Database {GuildID}_Discord ")
        await database.createdatabase(f"{GuildID}_Discord")
        console.print_warning(f"Creating new Table Levels")
        await database.CreateTable(f"Levels","UserID VARCHAR(255), Level VARCHAR(255), XP VARCHAR(255)",database=f"{GuildID}_Discord")
    finally:
        console.print_debug("IS CONTINUE")
        xplevel = await database.ReadTable(query=f"SELECT XP,Level FROM Levels WHERE UserID = {UserID}",database=f"{GuildID}_Discord")
    if(len(xplevel) == 0):
        xp = 0
        level = {MinimumLevel}
        await database.WriteTable(f"INSERT INTO Levels (UserID, Level, XP) VALUES ({UserID},{MinimumLevel},0)",database=f"{GuildID}_Discord")
    else:
        xplevel = await database.ReadTable(query=f"SELECT XP,Level FROM Levels WHERE UserID = {UserID}",database=f"{GuildID}_Discord")
    return xplevel

async def AwardWordXP(message):
    # Split the message into a list of words
    words = re.findall(r'\b[a-zA-Z]*[aeiouAEIOU][a-zA-Z]*\b', message.content) 
    # Check if the list is not empty
    if words:
        # Award XP to the user based on the number of valid words
        xp_awarded = len(words) * WordXP
        xplevel = await DoesUserHaveDBEntry(message.author.id,message.guild.id)
        try:
            xp = int(xplevel[0][0])
            level = int(xplevel[0][1])
        except:
            xp = 0
            level = {MinimumLevel}
        
        xp += xp_awarded
        if(xp >= LevelXP * level):
            level += 1
            xp = xp - LevelXP
            await message.channel.send(f"{message.author.mention} has just reached level **{level}**!")
        await database.WriteTable(f"UPDATE Levels SET XP = {xp}, Level = {level} WHERE UserID = {message.author.id}",f"{message.guild.id}_Discord")

async def AwardXP(self,UserID,GuildID,XP,Interaction=None):
        xplevel = await DoesUserHaveDBEntry(UserID,GuildID)
        try:
            xp = int(xplevel[0][0])
            level = int(xplevel[0][1])
            if not xp:
                await database.WriteTable(f"INSERT INTO Levels (UserID, Level, XP) VALUES ({UserID},{str(MinimumLevel)},0",f"{GuildID}_Discord")
                await AwardXP(UserID,GuildID,XP)
        except TypeError:
            xp = 0
            level = {MinimumLevel}
        
        xp = xp + XP
        while(xp >= (LevelXP * level)):
            xp = xp - (LevelXP * level)
            level += 1
            if(Interaction != None):
                user = await utilities.mention_user(self,UserID,Interaction.guild.id)
                await Interaction.channel.send(f"{user.mention} has just reached level **{level}**!")
        await database.WriteTable(f"UPDATE Levels SET XP = {xp}, Level = {level} WHERE UserID = {UserID}",f"{GuildID}_Discord")
