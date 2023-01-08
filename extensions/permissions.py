#Global Imports
import sys,os,time,re,random,nextcord
#Specific Imports
from nextcord.ext import commands,application_checks
from nextcord import Interaction,ClientCog
from nextcord.ext.application_checks import *

from dotenv import load_dotenv
from colorama import Fore, Back, Style
#Local Imports
from  Internal import console,database,utilities
from Internal import permissions as perms

load_dotenv()



class Permissions(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Commands
    @nextcord.slash_command(name="addpermission",description="Add a command permission")
    async def add_permission_command(self, interaction: nextcord.Interaction, role: str, command: str , exclusive: bool):
        if(await perms.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await database.WriteTable(f"INSERT INTO Permissions (CommandID, MinimumRole, Exclusive) VALUES ('{command}', '{utilities.process_mention(role)}', '{int(exclusive)}') ON DUPLICATE KEY UPDATE MinimumRole = '{utilities.process_mention(role)}', Exclusive = {int(exclusive)};",f"{interaction.guild_id}_Discord")
                await interaction.send("Permission Added",ephemeral=True)
            except Exception as e:
                console.print_error(e)
                await interaction.send(f'Error: {e}',ephemeral=True)





def setup(client):
    client.add_cog(Permissions(client))
    




#Functions