import discord
from os import getenv
from os import remove
from os import _exit

class member_tracker():

    def __init__(self: object):
        self.bot_client = self.get_client()
        self.discord_client_list = None
        self.client_list = self.get_client_list()
    
    def get_discord_client_list(self: object) -> list[str]:
        """Returns the actual clients present in the server in the form of a list.
    
        Args:
           self(object): It needs the client object details to get the server specific members.
    
        Returns:
            list[str]: str = the unique ID of ever server member on the server side.
    
        Raises:
            N/A.
    
        Examples:
            >>> get_discord_client_list(member_tracker_bot)
            [1449210899964366960,
            172033503926419458,
            282161774265106432]
        """
        
        discord_client_list = []

        for guild in self.bot_client.guilds:
            for member in guild.members:
                discord_client_list.append(str(member.id))

        return discord_client_list

    def get_client_list(self: object) -> list[str | None]:
        """Returns the clients that the bot has on record for server side comparison.
    
        Args:
           self(object)
    
        Returns:
            list[str]: str = the unique ID of ever server member on record.
    
        Raises:
            FileNotFoundError: If there are no users on record, like when the bot is being initialised.
    
        Examples:
            >>> get_client_list(member_tracker_bot)
            [1449210899964366960,
            172033503926419458,
            282161774265106432]
            >>> get_client_list(member_tracker_bot_2)
            []
        """

        try:
            client_file = open("client_file.txt", "r")
            client_list =  client_file.readlines()
        
            for x in range(len(client_list)):
                client_list[x] = client_list[x].strip('\n')

            return client_list

        except FileNotFoundError:
            return []
    
    def create_client_list(self: object):
        """Creates a new on record client list from the information on the server side.
    
        Args:
            self(object): It needs the client object details to get the server specific members.
    
        Returns:
            N/A
    
        Raises:
            N/A
    
        Examples:
            >>> create_client_list(member_tracker_bot)
        """

        new_client_file = open("client_file.txt", "a")
        for client in self.discord_client_list:
            print(client, file = new_client_file)
    
    
    def write_to_client_list(self: object, new_client: str):
        """Writes a new client to the record.
    
        Args:
            self(object)
            new_client(str): The unique ID of the new client to be amended to the file.
    
        Returns:
            N/A
    
        Raises:
            N/A
    
        Examples:
            >>> write_to_client_list(member_tracker_bot, "1449210899964366960")
        """

        client_file = open("client_file.txt", "a")
        print(new_client, file = client_file)
    
    def delete_client_list(self: object):
        """Deletes the existing record of IDs.
    
        Args:
            self(object)
    
        Returns:
            N/A
    
        Raises:
            N/A
    
        Examples:
            >>> delete_client_list()
        """
        remove("client_file.txt")
    
    def get_client(self: object) -> object:
        """Gets a running Discord client via the API.
    
        Args:
            self(object)
    
        Returns:
            N/A
    
        Raises:
            N/A
    
        Examples:
            >>> get_client(member_tracker_bot)
        """

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        client = discord.Client(intents=intents)
        return client


def check_array_match(array_one: list[str], array_two: list[str]) -> list[str]:
    """A generic function to see which elements in array one aren't present in array two.
    
        Args:
            array_one(list[str])
            array_two(list[str])
    
        Returns:
            list[str]: the elements present in array one that aren't in array two.
    
        Raises:
            N/A
    
        Examples:
            >>> check_array_match([1,2,3],[1,2])
            [3]
    """
    
    missing_elements = []

    for asset in array_one:
        found = False

        for asset_two in array_two:

            if asset == asset_two:
                found = True
            
        if found == False:
            missing_elements.append(asset)
    
    return missing_elements

member_tracker_bot = member_tracker()

@member_tracker_bot.bot_client.event
async def on_ready():
    member_tracker_bot.discord_client_list = member_tracker_bot.get_discord_client_list()

    if member_tracker_bot.client_list == []:
        member_tracker_bot.client_list = member_tracker_bot.discord_client_list
        member_tracker_bot.create_client_list()
        member_tracker_bot.client_list = member_tracker_bot.get_client_list()

    new_clients = check_array_match(member_tracker_bot.discord_client_list, member_tracker_bot.client_list)
    for member in new_clients:
        member_tracker_bot.write_to_client_list(member)
    member_tracker_bot.client_list = member_tracker_bot.get_client_list()

    missing_clients = check_array_match(member_tracker_bot.client_list, member_tracker_bot.discord_client_list)
    if len(missing_clients) != 0:
        channel = await member_tracker_bot.bot_client.fetch_channel(getenv('CHANNEL_ID'))
        for member in missing_clients:
            user = await member_tracker_bot.bot_client.fetch_user(member)
            username = user.global_name or user.name
            await channel.send(f"{username} has left the server!")

        member_tracker_bot.delete_client_list()
        member_tracker_bot.create_client_list()
        member_tracker_bot.client_list = member_tracker_bot.get_client_list()

    _exit(1)

member_tracker_bot.bot_client.run(getenv("DISCORD_TOKEN"))