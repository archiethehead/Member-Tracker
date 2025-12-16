import discord
from os import getenv
from os import remove
from os import _exit

class member_tracker():

    def __init__(self):
        self.bot_client = self.get_client()
        self.discord_client_list = None
        self.client_list = self.get_client_list()
    
    def get_discord_client_list(self):
        discord_client_list = []

        for guild in self.bot_client.guilds:
            for member in guild.members:
                discord_client_list.append(str(member.id))

        return discord_client_list

    def get_client_list(self):
        
        try:
            client_file = open("client_file.txt", "r")
            client_list =  client_file.readlines()
        
            for x in range(len(client_list)):
                client_list[x] = client_list[x].strip('\n')

            return client_list

        except FileNotFoundError:
            return []
    
    def create_client_list(self):
        new_client_file = open("client_file.txt", "a")
        for client in self.discord_client_list:
            print(client, file = new_client_file)
    
    
    def write_to_client_list(self, new_client):
        client_file = open("client_file.txt", "a")
        print(new_client, file = client_file)
    
    def delete_client_list(self):
        remove("client_file.txt")
    
    def get_client(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        client = discord.Client(intents=intents)
        return client


def check_array_match(array_one, array_two):
    
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