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
    
    #Return if first 3 characters of message is not '/rs'
    if message.content[0:3] != '/rs':
        print ('Message does not start with /rs')
        return
        #Removes whitespaces and first 3 characters
    msg = message.content[3:].replace(' ', '')
    
    #Return if amy characters in msg is anything else than characters in testfor
    testfor = '01234567890+-'
    for char in msg:
        if char not in testfor:
            await message.channel.send('Syntax is: /rs skill ± modifier.... ± modifier\nSkill and modifier can only contain numbers' )
            return
    
    #Return if msg is empty (If you just write '/rs'
    if not msg:
            await message.channel.send('Syntax is: /rs skill ± modifier.... ± modifier\nSkill and modifier can only contain numbers' )
            return
            
    #Removes numbers to keep a list of '+' or '-' depending on modifier
    operation = list(filter(lambda c: not c.isdigit(), msg))
            
    #Splits msg in [skill], [modifier], .... [modifier]
    msg = msg.replace('-', '+').split('+')
    
    #Return if skill is not an integer
    try:
        skill = int(msg[0])
    except:
        await message.channel.send('Syntax is: /rs skill ± modifier ± modifier..... ± modifier\nSkill and modifier can only contain numbers' )
        return
    
    #Return if there is a mismatch between numbers of modifiers lige '/rs 19++1' 
    try:
        for i in range(len(operation)):
            if operation[i] is '+':
                skill = skill + int(msg[i+1])
            elif operation[i] is '-':
                skill = skill - int(msg[i+1])
    except:
        await message.channel.send('Syntax is: /rs skill ± modifier ± modifier..... ± modifier\nSkill and modifier can only contain numbers' )
        return
        
    #If skill > 20 then skill-20 need to be added to roll and skill set to 20
    bonus = 0    
    if skill > 20:
        bonus = skill - 20
        skill = 20
            
    #1d20 roll
    dieroll = randint(1, 20)
            
    #response = bots response to message. Here '@message.author' is added.
    response = '<@' + str(message.author.id) + '>'
    #If 1d20+bonus = 20 and a skill < 20 = FUMBLE
    if dieroll+bonus is 20 and skill < 20:
        #Result and (Roll+bonus vs Skill) added to response
        response = response + ': FUMBLE (Roll: ' + str(dieroll) + '+' + str(bonus) + '=' + str(dieroll+bonus) + ' vs skill ' + str(skill) + ')'
    #Else if 1d20+bonus > skill ) Failure
    elif dieroll+bonus > skill and skill < 20:
        #Result and (Roll+bonus vs Skill) added to response
        response = response + ': Failure (Roll: ' + str(dieroll) + '+' + str(bonus) + '=' + str(dieroll+bonus) + ' vs skill ' + str(skill) + ')'
    #Else if 1d20+bonus < skill = Success
    elif dieroll+bonus < skill:
        #Result and (Roll+bonus vs Skill) added to response
        response = response + ': Success (Roll: ' + str(dieroll) + '+' + str(bonus) + '=' + str(dieroll+bonus) + ' vs skill ' + str(skill) + ')'
    #Else must be 1d20+bonus = skill or (1d20 + bonus) > 20 
    elif dieroll+bonus >= 20:
        #Result and (Roll+bonus vs Skill) added to response
        response = response + ': Critical success (Roll: ' + str(dieroll) + '+' + str(bonus) + '=' + str(dieroll+bonus) + ' vs skill ' + str(skill) + ')'
             
    #Bot sends response
    await message.channel.send(response)
            
client.run(TOKEN)
