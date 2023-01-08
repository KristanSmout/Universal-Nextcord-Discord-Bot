from . import database,console

async def can_run_command(self,interaction,command_id):
    try:
        if(interaction.permissions.administrator == True):
            return True
        else:
            await database.CreateTable("Permissions","CommandID VARCHAR(255) NOT NULL PRIMARY KEY, MinimumRole VARCHAR(255) NOT NULL, Exclusive BOOL NOT NULL",f"{str(interaction.guild.id)}_Discord")
            minimum_role_id = await database.ReadTable(f"SELECT * FROM Permissions WHERE CommandID = '{command_id}'",f"{interaction.guild.id}_Discord")
            if(len(minimum_role_id)>0):
                if(minimum_role_id[0][2] == 1):
                    await has_role(self,interaction,minimum_role_id[0][1])
                elif(has_higher_role(self,interaction,minimum_role_id[0] [1])):
                    return True
            await interaction.send('You do not have permission to use this command',ephemeral=True)
            return False
    except Exception as e:
        console.print_error(e)
        await interaction.send('You do not have permission to use this command',ephemeral=True)
        return False

async def has_higher_role(self, interaction, role_id):
    # Get the member object for the user
    member = interaction.user.guild.get_member(interaction.user.id)
    # Get the roles for the member
    member_roles = [role.id for role in member.roles]
    # Check if the user has the specified role or a higher role
    if role_id in member_roles:
        return True
    # Get the position of the specified role
    role = interaction.user.guild.get_role(role_id)
    role_position = role.position
    # Check if the user has a higher role
    for role in member_roles:
        if interaction.user.guild.get_role(role).position >= role_position:
            return True
    return False

async def has_role(self, interaction, role_id):
     # Get the member object for the user
    member = interaction.user.guild.get_member(interaction.user.id)
    # Get the roles for the member
    member_roles = [role.id for role in member.roles]
    if role_id in member_roles:
        return True
    return False