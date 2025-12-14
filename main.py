import discord
from os import getenv
from os import remove

def write_to_client_list(new_client):
    client_file = open("client_file.txt", "a")
    client_file.write(new_client, '\n')

def remove_client(client_list):
    remove("client_file.txt")
    create_client_list()

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

client_list = get_client_list()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    if client_list == []:
        for guild in client.guilds:
            for member in guild.members:
                client_list.append(member.name)
        create_client_list(client_list)
    print(client_list)

client.run(getenv("DISCORD_TOKEN"))