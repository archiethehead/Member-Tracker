import discord
from os import getenv
from os import remove

def write_to_client_list(new_client):
    client_file = open("client_file.txt", "a")
    print(new_client, file = client_file)

def remove_client():
    remove("client_file.txt")

def create_client_list(client_list):
    new_client_file = open("client_file.txt", "a")
    for client in client_list:
        print(client, file = new_client_file)

def get_client_list():

    try:
        client_file = open("client_file.txt", "r")
        client_list =  client_file.readlines()
        
        for x in range(len(client_list)):
            client_list[x] = client_list[x].strip('\n')

        return client_list

    except FileNotFoundError:
        return []

def check_match(discord_client_list, client_list):

    missing_clients = []
    for member in client_list:
        found = False

        for discord_member in discord_client_list:
            if member == discord_member:
                found = True

        if found == False:
            missing_clients.append(member)
    
    return missing_clients

def check_new_clients(discord_client_list, client_list):

    missing_clients = []

    for discord_member in discord_client_list:
        found = False

        for member in client_list:
            if discord_member == member:
                found = True

        if found == False:
            missing_clients.append(discord_member)
    
    return missing_clients

def get_discord_list():
    discord_client_list = []
    for guild in client.guilds:
        channel = discord.utils.get(guild.text_channels, name="general")
        for member in guild.members:
            discord_client_list.append(str(member.id))
    return channel, discord_client_list

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    client_list = get_client_list()
    channel, discord_client_list = get_discord_list()

    if client_list == []:
        client_list = discord_client_list
        create_client_list(client_list)
        client_list = get_client_list()
    
    new_clients = check_new_clients(discord_client_list, client_list)
    if (len(new_clients) != 0):
        for member in new_clients:
            write_to_client_list(member)
        client_list = get_client_list()

    missing_clients = check_match(discord_client_list, client_list)
    if (len(missing_clients) != 0):

        if channel:
            for member in missing_clients:
                user = await client.fetch_user(member)
                username = user.global_name or user.name
                string = (str(username) + " has left the server!")
                await channel.send(string)

        remove_client()
        create_client_list(discord_client_list)
        client_list = get_client_list()

client.run(getenv("DISCORD_TOKEN"))