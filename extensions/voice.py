#Global Imports
import sys,os,time,re,random,nextcord
#Specific Imports
from nextcord.ext import commands,application_checks
from nextcord import Interaction,ClientCog
from nextcord.ext.application_checks import *

from dotenv import load_dotenv
from colorama import Fore, Back, Style
#Local Imports
from  Internal import console,database,utilities,permissions

load_dotenv()

max_bitrate = int(os.environ['VOICE_BITRATE']) * 1000

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Commands    
    @nextcord.slash_command(name="deletevoice",description="Delete a temporary voice channel")
    async def delete_voice_channel(self, interaction: nextcord.Interaction, maxusers: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            await delete_voice(interaction,str(maxusers))
    
    @nextcord.slash_command(name="createvoice",description="Create a temporary voice channel")
    async def create_temp_voice_channel(self, interaction: nextcord.Interaction, maxusers: int):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            if(maxusers > int(os.environ['MAX_CHANNEL_SIZE'])):
                maxusers = int(os.environ['MAX_CHANNEL_SIZE'])
            # Get the user who sent the command
            user = interaction.user
            # Get the user's current voice channel
            current_channel = interaction.channel
            # Get the category that the current voice channel is in
            category = current_channel.category
            # Create a new voice channel with a limit
            temp_channel = await category.create_voice_channel(name=f"{user.display_name}", user_limit=maxusers, bitrate=max_bitrate)
            # Move the user to the new voice channel
            await store_voice(interaction,temp_channel)
            try:
                await user.move_to(temp_channel)
                await interaction.send(f"Channel Created, Join Here <#{str(temp_channel.id)}>",ephemeral=True)
            except:
                await interaction.send(f"Channel Created, Join Here <#{str(temp_channel.id)}>",ephemeral=True)
        
    

    
    
                


def setup(client):
    client.add_cog(Voice(client))
    

#Functions
async def store_voice(interaction,voice_channel):
    await database.CreateTable("Voice"," VoiceID VARCHAR(255) NOT NULL PRIMARY KEY, OwnerID VARCHAR(255) NOT NULL, CreatedDateTime VARCHAR(255) NOT NULL",database=f"{str(interaction.guild_id)}_Discord")
    exists = await database.ReadTable(f"SELECT COUNT(*) FROM Voice WHERE OwnerID = {interaction.user.id};",database=f"{str(interaction.guild_id)}_Discord")
    if(exists[0][0] == 0):
        test = f"INSERT INTO Voice (OwnerID, VoiceID, CreatedDateTime) VALUES ('{interaction.user.id}', '{voice_channel.id}', '{utilities.generate_sql_datetime()}') ON DUPLICATE KEY UPDATE VoiceID = '{voice_channel.id}', CreatedDateTime = {utilities.generate_sql_datetime()};"
        await database.WriteTable(f"INSERT INTO Voice (OwnerID, VoiceID, CreatedDateTime) VALUES ('{interaction.user.id}', '{voice_channel.id}', '{utilities.generate_sql_datetime()}') ON DUPLICATE KEY UPDATE VoiceID = '{voice_channel.id}', CreatedDateTime = '{utilities.generate_sql_datetime()}';",database=f"{str(interaction.guild_id)}_Discord")
    else:
        old_id = await database.ReadTable(f"select VoiceID from Voice where OwnerID = {interaction.user.id}",database=f"{str(interaction.guild_id)}_Discord")
        await delete_voice(interaction,old_id[0][0],reason="User requested a new channel to be created.")
        await database.WriteTable(f"INSERT INTO Voice (OwnerID, VoiceID, CreatedDateTime) VALUES ('{interaction.user.id}', '{voice_channel.id}', '{utilities.generate_sql_datetime()}') ON DUPLICATE KEY UPDATE VoiceID = '{voice_channel.id}', CreatedDateTime = '{utilities.generate_sql_datetime()}';",database=f"{str(interaction.guild_id)}_Discord")


async def delete_voice(interaction,voice_channel_id,reason="Not Provided"):
    try:
        channel = await utilities.get_voice_channel(interaction,voice_channel_id)
        await channel.delete(reason=f"{reason}")
        await database.WriteTable(f"DELETE FROM Voice WHERE VoiceID = {voice_channel_id};",database=f"{str(interaction.guild_id)}_Discord")
    except Exception as e:
        console.print_error(f"Unable to delete voice channel: {voice_channel_id} due to \n {e}")


