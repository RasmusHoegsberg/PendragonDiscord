# bot.py
import os
import re
import discord
from dotenv import load_dotenv
from random import seed
from random import randint

#Loads enviroment variables from file
load_dotenv()
#Loads bot token
TOKEN = os.getenv('DISCORD_TOKEN')

#New discord client
client = discord.Client()

#On python script load
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
#On new message
async def on_message(message):
        #return if author of message is bot to prevent recursion
        if message.author == client.user:
            return
        
        #If first 3 characters of message is '/rs'
        if message.content[0:3] == '/rs':
            #Removes whitespaces and first 3 characters
            msg = message.content[3:].replace(' ', '')
    
            #Message format should be /rs skill ± modifier
            
            #Removes numbers to keep a + or - depending on modifier
            operation = list(filter(lambda c: not c.isdigit(), msg))
            
            #Splits msg in [skill], [modifier]
            msg = msg.replace('-', '+').split('+')
            
            #If there are any modifiers
            if len(operation):
                #If positive modifier
                if operation[0] is '+':
                    #Add modifier to skill
                    skill = int(msg[0]) + int(msg[1])
                #if modifier is negative
                elif operation[0] is '-':
                    #Subtract modifier from skill
                    skill = int(msg[0]) - int(msg[1])
            #If no modifiers
            else:
                #Use skill
                skill = int(msg[0])
            
            #If skill > 20 then skill-20 need to be added to roll and skill set to 20
            bonus = 0
            if skill > 20:
                bonus = skill - 20
                skill = 20
            
            #1d20 roll + bonus for skill > 20. If skill < 20 then 0 is used.
            dieroll = randint(1, 20) + bonus
            
            #response = bots response to message. Here @message.author is added.
            response = '<@' + str(message.author.id) + '>'
            #If 1d20 = 20 and a skill < 20 = FUMBLE
            if dieroll is 20 and skill < 20:
                #Result and (Roll vs Skill) added to response
                response = response + ': FUMBLE (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
            #Else if 1d20 > skill ) Failure
            elif dieroll > skill
                #Result and (Roll vs Skill) added to response
                response = response + ': Failure (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
            #Else if 1d20 < skill = Success
            elif dieroll < skill:
                 #Result and (Roll vs Skill) added to response
                 response = response + ': Success (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
            #Else must be 1d20 = skill or (1d20 + bonus) > 20 
            else:
                #Result and (Roll vs Skill) added to response
                response = response + ': Critical success (Roll: ' + str(dieroll) + ' vs skill ' + str(skill) + ')'
             
            #Bot sends response
            await message.channel.send(response)
            
client.run(TOKEN)

