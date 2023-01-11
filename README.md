# Discord Bot

A Discord bot created using Python and the Nextcord library.

## File Structure

- `main.py`: the main Python file that runs the Discord bot
- `README.md`: the README file for the project
- `requirements.txt`: a text file that lists the required Python packages for the project
- `extensions`: a directory that contains Python files for additional functionality for the bot
- `template`: a template file within the `extensions` directory that contains the extension template to add custom functionality
- `Internal`: a directory that contains Python files for internal functionality for the bot, these are required for functionality

## Prerequisites

- Python 3.7+
- The following Python packages:
  - aiomysql==0.1.1
  - colorama==0.4.6
  - discord.py==2.1.0
  - mysql_connector_repackaged==0.3.1
  - nextcord==2.3.2
  - python-dotenv==0.21.0
- A Discord bot account

## Installation

1. Clone this repository.
2. Install the required libraries by running `pip install -r requirements.txt`.
3. Create a file called `.env` and fill in the necessary environment variables (see below).
4. Run the bot using `python main.py`.

## Environment Variables

The following environment variables should be set in the `.env` file:

- `DISCORD_TOKEN`: the Discord bot token
- `PREFIX`: the desired command prefix for the bot (e.g. `!`)
- `DEBUG`: a Boolean value indicating whether debug mode should be enabled
- `GUILD_ID`: the ID of the Discord server
- `APPLICATION_ID`: the ID of the Discord application
- `PUBLIC_KEY`: the public key for the Discord application
- `CLIENT_ID`: the client ID for the Discord application
- `CLIENT_SECRET`: the client secret for the Discord application
- `BOT_TOKEN`: the bot token for the Discord application
- `INVITE_URL`: the URL to use to invite the bot to a server
- `SERVER_ID`: the ID of the Discord server
- `SQL_IP`: the IP address of the SQL server
- `SQL_DB`: the name of the SQL database
- `SQL_Username`: the username to use when connecting to the SQL database
- `SQL_Password`: the password to use when connecting to the SQL database

## Usage

To use the bot, simply launch the program and invite it to your discord server, or invite the public one with [Future URL HERE]

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
