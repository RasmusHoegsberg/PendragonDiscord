# bot.py
import os
import re
import discord
from dotenv import load_dotenv
from random import seed
from random import randint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD =os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
        if message.author == client.user:
            return

        if message.content[0:3] == '/rs':
            msg = message.content[3:].replace(' ', '')
    
            operation = list(filter(lambda c: not c.isdigit(), msg))
            msg = msg.replace('-', '+').split('+')
            
            if len(operation):
                if operation[0] is '+':
                    skill = int(msg[0]) + int(msg[1])
                elif operation[0] is '-':
                    skill = int(msg[0]) - int(msg[1])
            else:
                skill = int(msg[0])
            
            bonus = 0
            if skill > 20:
                bonus = skill - 20
            
            dieroll = randint(1, 20) + bonus
            
            response = '<@' + str(message.author.id) + '>'              
            if dieroll is 20 and skill < 20:
                response = response + ': FUMBLE (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
            elif dieroll > skill and skill < 20:
                response = response + ': Failure (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
            elif dieroll < skill:
                 response = response + ': Success (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
            else:
                response = response + ': Critical success (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
             
            await message.channel.send(response)
            
client.run(TOKEN)

