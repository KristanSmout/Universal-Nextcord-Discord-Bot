#Global Imports
import os,sys,dotenv,nextcord,asyncio
#Specific Imports
from nextcord.ext import commands
from dotenv import load_dotenv
from colorama import Fore
#Local Imports
from Internal import console,database

version = "0.0.1"
#Bot Init
intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(intents=intents, default_guild_ids=[1025485715993272330])

initial_extensions = []

@client.event
async def on_ready():
    #await sync_modules()
    console.print_message("Online!")
    await client.change_presence(activity=nextcord.Streaming(name="Looking for contributors",url="https://github.com/KristanSmout/Universal-Nextcord-Discord-Bot"))

def version_check():
    console.print_debug("Starting Version Check")
    #VersionCheckHere
    try:
        lastest = "0.0.2"
        if not version != lastest:
            console.print_warning(f"A new version is available | {version} -> {lastest}")
        else:
            console.print_message(f"You are running the latest version")
    except:
        console.print_error("Unable to check for new version")

def load_extensions():
    console.print_message("Find Extensions")
    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            console.print_message(f"Found Module: {Fore.CYAN} {filename[:-3]}")
            initial_extensions.append(f"extensions.{filename[:-3]}")
    
    console.print_message("Loading Extensions")
    for extension in initial_extensions:
        try:
            console.print_message(f"{extension}: {Fore.BLUE}Loading",True)
            client.load_extension(extension)
            console.print_message(f"{extension}: {Fore.GREEN}Loaded")
        except Exception as e:
            console.print_error(f"{extension}: {Fore.RED}{e}")

async def sync_modules():
    await client.sync_application_commands(guild_id=os.environ['SERVER_ID'])
    num_commands = len(client.commands)
    console.print_message(f"Synced {num_commands} command(s)")
    
async def main():
    console.print_message("Application Started")
    version_check()
    database.test_connection()
    load_extensions()
    
    

if __name__ == "__main__":
    load_dotenv()
    os.system("cls")
    
    console.print_message("Application Started")
    version_check()
    database.test_connection()
    load_extensions()
    print(client)

    client.run(os.environ['BOT_TOKEN'])