from colorama import Fore,Style
from datetime import datetime
from . import utilities

debug=False

debug = f"{Fore.GREEN}[Debug]{Style.RESET_ALL}"
log = f"{Fore.WHITE}[Log]{Style.RESET_ALL}"
warning = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL}"
error = f"{Fore.RED}[ERROR]{Style.RESET_ALL}"

end_reset="\r"

def set_debug(value):
    debug = utilities.str_to_bool(value)

def print_debug(message,overwrite=False):
    if(debug == True):
        # Get the current datetime
        now = datetime.now()

        # Format the datetime according to the desired format
        timestamp = f"{now:%Y-%m-%d %H:%M:%S}]"

        # Print the timestamped message to the console
        if not overwrite:
            print(f'{timestamp} {debug} {message} {Style.RESET_ALL}')
        else:
            print(f'{timestamp} {debug} {message} {Style.RESET_ALL}',end=end_reset)

def print_message(message,overwrite=False):
    # Get the current datetime
    now = datetime.now()

    # Format the datetime according to the desired format
    timestamp = f"{now:%Y-%m-%d %H:%M:%S}]"

    # Print the timestamped message to the console
    if not overwrite:
        print(f'{timestamp} {log} {message} {Style.RESET_ALL}')
    else:
        print(f'{timestamp} {log} {message} {Style.RESET_ALL}',end=end_reset)

def print_warning(message,overwrite=False):
    # Get the current datetime
    now = datetime.now()

    # Format the datetime according to the desired format
    timestamp = f"{now:%Y-%m-%d %H:%M:%S}]"

    # Print the timestamped message to the console
    if not overwrite:
        print(f'{timestamp} {warning} {message} {Style.RESET_ALL}')
    else:
        print(f'{timestamp} {warning} {message} {Style.RESET_ALL}',end=end_reset)

def print_error(message,overwrite=False):
    # Get the current datetime
    now = datetime.now()

    # Format the datetime according to the desired format
    timestamp = f"{now:%Y-%m-%d %H:%M:%S}]"

    # Print the timestamped message to the console
    if not overwrite:
        print(f'{timestamp} {error} {message} {Style.RESET_ALL}')
    else:
        print(f'{timestamp} {error} {message} {Style.RESET_ALL}',end=end_reset)
