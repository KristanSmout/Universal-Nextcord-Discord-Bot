#Global Imports
import sys,os,time,re,random,nextcord
#Specific Imports
from nextcord.ext import commands,application_checks
from nextcord import Interaction,ClientCog,PartialEmoji
from nextcord.ext.application_checks import *

from dotenv import load_dotenv
from colorama import Fore, Back, Style
#Local Imports
from  Internal import console,database,utilities,permissions

load_dotenv()



class emojirole(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Commands    
    @nextcord.slash_command(name="createemojirole",description="Create a emoji role ")
    async def delete_voice_channel(self, interaction: nextcord.Interaction, identifier: str, channelid: str,messageid: str, emoji: str, role: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            await create_emojirole_rule(interaction,identifier,channelid,messageid,emoji,role)
            await interaction.send(f"Created",ephemeral=True)
            interaction.channel_id
    
    @nextcord.slash_command(name="deleteemojirole",description="delete a emoji role ")
    async def delete_voice_channel(self, interaction: nextcord.Interaction, identifier: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            await delete_emojirole_rule(interaction,identifier)
            await interaction.send(f"Deleted",ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(locals,payload):
        await assign_emoji_role(locals,payload)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(locals,payload):
        await console.print_message_async("Emoji was removed")


def setup(client):
    client.add_cog(emojirole(client))
    




#Functions
async def create_table(interaction):
    await database.CreateTable("EmojiRole","Identifier VARCHAR(255) NOT NULL PRIMARY KEY, ChannelID VARCHAR(255) NOT NULL ,MessageID VARCHAR(255) NOT NULL, EmojiID VARCHAR(255) NOT NULL, RoleIDs VARCHAR(255) NOT NULL",f"{str(interaction.guild.id)}_Discord")

async def add_role(interaction,emoji_role,role_id):
    pass

async def create_emojirole_rule(interaction,identifer,channel_id,message_id, emoji_id, role_id):
    await create_table(interaction)
    #Check if ID Exists
    try:
        entry = await database.ReadTable(f"SELECT COUNT(*) FROM EmojiRole WHERE Identifier = '{identifer}'",database=f"{str(interaction.guild.id)}_Discord")
        count = entry[0][0]
        if(count != 0):
            await interaction.send(f"Entry already exists, please modify instead",ephemeral=True)
        else:
            await database.WriteTable(f"INSERT INTO EmojiRole (Identifier, ChannelID ,MessageID, EmojiID,RoleIDs) VALUES ('{identifer}', '{str(channel_id)}' ,'{str(message_id)}', '{str(emoji_id)}','{str(role_id)}')",f"{interaction.guild_id}_Discord")
            await add_emoji(interaction,channel_id,message_id,emoji_id)

    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def delete_emojirole_rule(interaction,identifer):
    #Check if ID Exists
    try:
        entry = await database.ReadTable(f"SELECT COUNT(*) FROM EmojiRole WHERE Identifier = '{identifer}'",database=f"{str(interaction.guild.id)}_Discord")
        count = entry[0][0]
        if(count == 0):
            await interaction.send(f"No Entry Exists!",ephemeral=True)
        else:
            entry = await database.ReadTable(f"SELECT * FROM EmojiRole WHERE Identifier = '{identifer}' ",f"{interaction.guild_id}_Discord")
            await remove_emoji(interaction,entry[0][1],entry[0][2],entry[0][3])
            entry = await database.WriteTable(f"DELETE FROM EmojiRole WHERE Identifier = '{identifer}' ",f"{interaction.guild_id}_Discord")
            

    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def add_emoji(interaction,channel_id,message_id,emoji_id):
    guild = interaction.guild
    channel = await guild.fetch_channel(f"{int(channel_id)}") 
    message = channel.get_partial_message(f"{int(message_id)}")
    await message.add_reaction(f"{emoji_id}")

async def remove_emoji(interaction,channel_id,message_id,emoji_id):
    try:
        guild = interaction.guild
        channel = await guild.fetch_channel(f"{int(channel_id)}") 
        message = channel.get_partial_message(f"{int(message_id)}")
        await message.clear_reaction(f"{emoji_id}")
    except Exception as e:
        await console.print_error_async(f"Error: {e}")

async def assign_emoji_role(locals,payload):
    entry = await database.ReadTable(f"SELECT COUNT(*) FROM EmojiRole WHERE ChannelID = '{payload.channel_id}' AND MessageID = '{payload.message_id}' AND EmojiID = '{payload.emoji.name}'",database=f"{str(payload.guild_id)}_Discord")
    if(entry[0][0] != 0):
        guild = await locals.client.fetch_guild(payload.guild_id)
        identifier = await database.ReadTable(f"SELECT Identifier FROM EmojiRole WHERE ChannelID = '{payload.channel_id}' AND MessageID = '{payload.message_id}' AND EmojiID = '{payload.emoji.name}'",database=f"{str(payload.guild_id)}_Discord")
        sqlroles = await database.ReadTable(f"SELECT RoleIDs FROM EmojiRole WHERE ChannelID = '{payload.channel_id}' AND MessageID = '{payload.message_id}' AND EmojiID = '{payload.emoji.name}'",database=f"{str(payload.guild_id)}_Discord")
        all_roles = sqlroles[0][0].split(',')
        roles = []
        for role in all_roles:
            id = int(utilities.process_mention(role))
            temp = id
            localrole = guild.get_role(id)
            roles.append(localrole)
            #await payload.member.add_roles(localrole,reason=f"EmojiRole: {identifier[0][0]}")
        await payload.member.add_roles(*roles,reason=f"EmojiRole: {identifier[0][0]}")