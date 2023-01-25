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



class RoleAssignment(commands.Cog):
    def __init__(self, client):
        self.client = client



    @nextcord.slash_command(name="roleall",description="Give default roles to everyone")
    async def roleall_defaultroles_command(self, interaction: nextcord.Interaction):
        if(await  permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await create_table(interaction)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)
    
    @nextcord.slash_command(name="createdefaultroles",description="Give default roles to everyone")
    async def create_defaultroles_command(self, interaction: nextcord.Interaction, baserole: str, roles: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await create_table(interaction)
                await create_utilityrole_rule(interaction,baserole,roles)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)
    
    @nextcord.slash_command(name="adddefaultroles",description="Give default roles to everyone")
    async def add_defaultroles_command(self, interaction: nextcord.Interaction, baserole: str, roles: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await create_table(interaction)
                await add_utilityrole_rule(interaction,baserole,roles)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)
    
    @nextcord.slash_command(name="removedefaultroles",description="Give default roles to everyone")
    async def remove_defaultroles_command(self, interaction: nextcord.Interaction, baserole: str, roles: str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await create_table(interaction)
                await remove_utilityrole_rule(interaction,baserole,roles)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)

    @nextcord.slash_command(name="listdefaultroles",description="Give default roles to everyone")
    async def list_defaultroles_command(self, interaction: nextcord.Interaction, role = None):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                if role is None:
                    await create_table(interaction)
                    data = await getall_utilityrole_rules(interaction)
                    data = data
                    strbuilder = ''
                    for entry in data:
                        roles = []
                        currentroles = entry[1].split(',')
                        for role in currentroles:
                            roles.append(utilities.group_id_to_mention(interaction,role))
                        roles = utilities.roles_to_string(roles)
                        strbuilder += f'The {utilities.group_id_to_mention(interaction,entry[0])} provides the following roles {roles} \n\n'
                    await interaction.send(f'{strbuilder}',ephemeral=True)
                else:
                    await create_table(interaction)
                    data = await get_utilityrole_rules(interaction,role)
                    baserole = utilities.group_id_to_mention(interaction,data[0][0])
                    roles = []
                    for role in (data[0][1].split(',')):
                        roles.append(utilities.group_id_to_mention(interaction,role))
                    roles = utilities.roles_to_string(roles)
                    await interaction.send(f'The {baserole} provides the following roles \n{roles} ',ephemeral=True)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)

    @nextcord.slash_command(name="assignroles",description="Give default roles to everyone")
    async def forceroles_command(self, interaction: nextcord.Interaction, role = None):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await create_table(interaction)
                await assign_utilityrole(interaction,role)
                await interaction.send(f"Done!",ephemeral=True)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)

    @nextcord.slash_command(name="deleterole",description="Give default roles to everyone")
    async def deleterole_command(self, interaction: nextcord.Interaction, role : str):
        if(await permissions.can_run_command(self,interaction,utilities.get_current_function())):
            try:
                await create_table(interaction)
                await delete_utilityrole(interaction,role)
            except Exception as e:
                await interaction.send(f'Error: {e}',ephemeral=True)

def setup(client):
    client.add_cog(RoleAssignment(client))
    




#Functions
async def create_table(interaction):
    await database.CreateTable("UtilityRanks","RequiredRole VARCHAR(255) NOT NULL PRIMARY KEY, RoleIDs VARCHAR(255) NOT NULL",f"{str(interaction.guild.id)}_Discord")

async def create_utilityrole_rule(interaction,requiredrole,roles):
    await create_table(interaction)
    #Check if ID Exists
    try:
        entry = await database.ReadTable(f"SELECT COUNT(*) FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
        count = entry[0][0]
        if(count != 0):
            await interaction.send(f"Entry already exists, please modify instead",ephemeral=True)
        else:
            await database.WriteTable(f"INSERT INTO UtilityRanks (RequiredRole, RoleIDs) VALUES ('{str(utilities.process_mention(requiredrole))}', '{utilities.roles_to_string(utilities.process_role_to_array(roles))}')",f"{interaction.guild_id}_Discord")
            await interaction.send(f"Created",ephemeral=True)
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def add_utilityrole_rule(interaction,requiredrole,roles):
    await create_table(interaction)
    #Check if ID Exists
    try:
        entry = await database.ReadTable(f"SELECT COUNT(*) FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
        count = entry[0][0]
        if(count == 0):
            await interaction.send(f"Entry does not exist, please create",ephemeral=True)
        else:
            try:
                currentroles = await database.ReadTable(f"SELECT RoleIDs FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}' LIMIT 1",database=f"{str(interaction.guild.id)}_Discord")
                currentroles = currentroles[0][0]
                #Convert currentroles to list
                currentroles = currentroles.split(',')
                roles = utilities.process_role_to_array(roles)

                newroles = utilities.roles_to_string(list(set(currentroles+roles)))

                await database.WriteTable(f"UPDATE UtilityRanks SET RoleIDs = '{newroles}' WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
                await interaction.send(f"Added!",ephemeral=True)
            except Exception as e:
                 await interaction.send(f"Error: {e}",ephemeral=True)
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def remove_utilityrole_rule(interaction,requiredrole,roles):
    await create_table(interaction)
    #Check if ID Exists
    try:
        entry = await database.ReadTable(f"SELECT COUNT(*) FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
        count = entry[0][0]
        if(count == 0):
            await interaction.send(f"Entry does not exist, please create",ephemeral=True)
        else:
            try:
                currentroles = await database.ReadTable(f"SELECT RoleIDs FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}' LIMIT 1",database=f"{str(interaction.guild.id)}_Discord")
                currentroles = currentroles[0][0]
                #Convert currentroles to list
                currentroles = utilities.process_role_to_array(currentroles)
                roles = utilities.process_role_to_array(roles)
                #newroles = currentroles - roles
                newroles = list(set(currentroles)-set(roles))



                newroles = utilities.roles_to_string(list(set(currentroles)-set(roles)))

                await database.WriteTable(f"UPDATE UtilityRanks SET RoleIDs = '{newroles}' WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
                await interaction.send(f"Removed!",ephemeral=True)
            except Exception as e:
                 await interaction.send(f"Error: {e}",ephemeral=True)
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def get_utilityrole_rules(interaction,role):
    await create_table(interaction)
    try:
        test = utilities.process_mention(role)
        entry = await database.ReadTable(f"SELECT * FROM UtilityRanks WHERE RequiredRole = '{utilities.process_mention(role)}'",database=f"{str(interaction.guild.id)}_Discord")
        return entry
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def getall_utilityrole_rules(interaction):
    await create_table(interaction)
    try:
        entry = await database.ReadTable(f"SELECT * FROM UtilityRanks",database=f"{str(interaction.guild.id)}_Discord")
        return entry
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def delete_utilityrole(interaction,requiredrole):
    await create_table(interaction)
    try:
        entry = await database.ReadTable(f"SELECT COUNT(*) FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
        count = entry[0][0]
        if(count == 0):
            await interaction.send(f"Entry does not exist, please create",ephemeral=True)
        else:
            try:
                await database.WriteTable(f"DELETE FROM UtilityRanks WHERE RequiredRole = '{str(utilities.process_mention(requiredrole))}'",database=f"{str(interaction.guild.id)}_Discord")
                await interaction.send(f"Deleted!",ephemeral=True)
            except Exception as e:
                 await interaction.send(f"Error: {e}",ephemeral=True)
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)

async def assign_utilityrole(interaction,role):
    await create_table(interaction)
    try:
        if role == None:
            rules = await database.ReadTable(f"SELECT RequiredRole FROM UtilityRanks",database=f"{str(interaction.guild.id)}_Discord")
            #rules = utilities.roles_to_string(rules)
            cleanedrules = []
            for rule in rules:
                rule = ''.join(filter(str.isdigit, rule))
                cleanedrules.append(int(rule))
            for rule in cleanedrules:
                entry = await database.ReadTable(f"SELECT RoleIDs FROM UtilityRanks WHERE RequiredRole = '{rule}'",database=f"{str(interaction.guild.id)}_Discord")
                if(len(entry) != 0):
                    roles = utilities.process_role_to_array(entry[0][0])
                    for role in roles:
                        role = interaction.guild.get_role(int(role))
                        for member in role.members:
                                await member.add_roles(role)
                                print(f"Added {member.name} to {role.name}")
        else:
            ID = utilities.process_mention(role)
            parentrole = interaction.guild.get_role((ID))
            entry = await database.ReadTable(f"SELECT RoleIDs FROM UtilityRanks WHERE RequiredRole = '{parentrole.id}'",database=f"{str(interaction.guild.id)}_Discord")
            
            #roles = utilities.process_role_to_array(entry[0][0])
            
            temp = entry[0][0]
            if ',' in entry[0][0]:
                roles = entry[0][0].split(',')
            else:
                roles=entry[0][0]
            if(len(entry) != 0):
                localguild = interaction.guild
                for role in roles:
                    role = localguild.get_role(int(role))
                    for member in parentrole.members:
                            await member.add_roles(role)
                            print(f"Added {member.name} to {role.name}")
    except Exception as e:
        await interaction.send(f"Error: {e}",ephemeral=True)