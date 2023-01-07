import re,inspect
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