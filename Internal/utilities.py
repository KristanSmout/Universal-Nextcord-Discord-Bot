import re,inspect,datetime
from . import console

def str_to_bool(message):
    if message.lower() in ['true', '1']:
        return True
    elif message.lower() in ['false', '0']:
        return False
    else:
        console.error(f"Invalid str_to_bool input '{message}'")
        raise ValueError("Cannot convert string to boolean")

async def mention_user(self,user_id,guild_id):
    guild = self.client.get_guild(guild_id)
    member = guild.get_member(user_id)
    return member

def process_mention(mention):
    mention_pattern = re.compile(r'<@(?:&|!?)(?P<id>\d+)>')
    match = mention_pattern.match(mention)
    if match:
        user_id = int(match.group('id'))
        return user_id
    else:
        return None

def get_current_function():
    return inspect.stack()[1][3]

def generate_sql_datetime(dt=None):
    try:
        if(dt == None):
            now = datetime.datetime.now()
            sql_datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
            return sql_datetime_str
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        console.print_error(f"Error Parsing Datetime: {e}")

async def get_text_channel(interaction,channel_id):
    for channel in interaction.guild.text_channels:
        if(channel.id == int(channel_id)):
            return channel
    return None

async def get_voice_channel(interaction,channel_id):
    for channel in interaction.guild.voice_channels:
        if(channel.id == int(channel_id)):
            return channel
    return None