#Global Imports
import sys,os,time,re,random,nextcord
#Specific Imports
from nextcord.ext import commands,application_checks,tasks
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
        self.channel_cleanup.start()
    
    #Commands    
    @nextcord.slash_command(name="deletevoice",description="Delete a temporary voice channel")
    async def delete_voice_channel(self, interaction: nextcord.Interaction, channelid: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            await delete_voice(interaction,str(channelid))
            await interaction.send(f"Channel Deleted",ephemeral=True)
    
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

    @tasks.loop(seconds=60.0)
    async def channel_cleanup(self):
        console.print_warning("channel_cleanup Starting")
        for guild in self.client.guilds:
            #pass
            await voice_cleanup(guild)
    

    
    
                


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

async def voice_cleanup(guild):
    id = str(guild.id)
    #channel_list = list(await database.ReadTable("SELECT VoiceID FROM Voice WHERE TIMESTAMPDIFF(SECOND, CreatedDateTime, NOW()) > 30;",database=f"{id}_Discord"))
    #exists = await database.ReadTableNow(f"SELECT COUNT(*) FROM Voice",database=f"{str(id)}_Discord")
    channel_list = await database.ReadTableNow("SELECT VoiceID FROM Voice WHERE TIMESTAMPDIFF(SECOND, CreatedDateTime, NOW()) > 30",database=f"{id}_Discord")
    temporary_channels = [x[0] for x in channel_list]
    for channel in guild.voice_channels:
        if(str(channel.id) in temporary_channels):
            if(len(channel.members) < 1):
                try:
                    await channel.delete(reason="Unused Temporary Channel")
                    await console.print_debug_async(f"Deleted {channel.name}")
                    await database.WriteTable(f"DELETE FROM Voice WHERE VoiceID = {channel.id};",database=f"{str(guild.id)}_Discord")
                except:
                    console.print_error_async(f"Unable to delete {channel.name}")
            else:
                await console.print_debug_async(f"Has Members {channel.name}")

    


