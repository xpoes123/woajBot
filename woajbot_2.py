#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import datetime
import json
import os.path
import random
import string
import sys
import math
import discord
from discord.ext import commands
from discord.ext.commands import Bot
# from urbandictionary_top import udtop

# TODO New Commands
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* Add a level system for the bot and reset the current level system.
* State guessing game, update and add questions as time goes on.
* Create a .xp @someone system where you can find out the xp of other people
* Create a .xp_rank to find out the leader boards for xp
* Create a prompt for when people join the discord.
* Create a working database of the pb's of people.
* Quicklinks
* Release to the public
* Add the wca database
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

BOT_PREFIX = (".")


def get_json(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp)


acc_name = "main"
jsontoken = 0

if acc_name == "main":
    print("Using TEST account")
    jsontoken = get_json('./token.json')
    token = jsontoken.get("token")

if jsontoken == 0:
    print("WOAJ!!! You need a token to go online.")
    exit(0)

print("Token being used: {0}".format(jsontoken.get("token")))
print("Connecting...")

embed_color = 0x1abc9c

Client = discord.Client()
client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    users = len(set(client.get_all_members()))
    channels = len([c for c in client.get_all_channels()])
    server_list = list(client.servers)

    print("============================================================")
    print("                         _ ____        __ ")
    print(" _      ______  ____ _  (_) __ )____  / /_")
    print("| | /| / / __ \/ __ `/ / / __  / __ \/ __/")
    print("| |/ |/ / /_/ / /_/ / / / /_/ / /_/ / /_ ")
    print("|__/|__/\____/\__,_/_/ /_____/\____/\__/  ")
    print("                  /___/                 ")
    print("• Version:                   {}".format(discord.__version__))
    print("• Client Name:               {}".format(client.user))
    print("• Client ID:                 {}".format(client.user.id))
    print("• Channels:                  {}".format(channels))
    print("• Users:                     {}\n".format(users))
    print("• Connected to " + str(len(client.servers)) + " server(s):")
    for x in range(len(server_list)):
        print("     > " + server_list[x - 1].name)
    print("============================================================")


@client.event
async def on_resumed():
    print("{0}:{1}:{2}: Resumed ".format(datetime.datetime.now().hour, datetime.datetime.now().minute,
                                         datetime.datetime.now().second))


@client.event
async def on_message(message):
    # Message author variables
    user_id = message.author.id
    user_name = message.author

    # xp and karma
    user_add_xp(message.author.id, 2)

    if user_id == client.user:
        return

    print("{0} sent message '{1}' in #{2}".format(message.author.nick, message.content, message.channel))

    # Ping Command
    if message.content.upper().startswith(".PING"):
        await client.send_message(message.channel, "Pong! :ping_pong:")
    elif message.content.startswith('.info'):
        msg = 'We are a cubing Discord channel that is an attempted substitute for the pizza friends group chat. ' \
              'Many people have complained about the lacking features that Facebook messenger gives people as well as' \
              'the lack of privacy Facebook gives its users. This will also help fix clutter in messages, as well as ' \
              'help organize conversations. Although new laws have been passed about privacy Discord is in all ways ' \
              'better then messenger. Many things will be added as time goes on. Stay tuned to see new cool features ' \
              'being added! {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('.bot'):
        msg = 'Do .bot for all possible commands. '
        await client.send_message(message.channel, msg)
        msg = 'Do .info for information about the server.'
        await client.send_message(message.channel, msg)
        msg = 'Do .ping responds with PONG'
        await client.send_message(message.channel, msg)
        msg = 'Do .xp to see the amount of xp you currently have.'
        await client.send_message(message.channel, msg)
        msg = 'Do .guess to play a guessing game with the bot.'
        await client.send_message(message.channel, msg)
        #XP
    elif message.content.lower().startswith(".xp"):
        await client.send_message(message.channel, "You have {} XP!".format(get_xp(message.author.id)))

        #Guessing Game
    elif message.content.startswith('.guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))



async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('$guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))


def user_add_xp(user_id: int, xp: int
                ):
    if os.path.isfile("users.json"):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['xp'] += xp
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['xp'] = xp
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['xp'] = xp
        with open('users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def get_xp(user_id: int):
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        return users[user_id]['xp']
    else:
        return 0


async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('.guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

client = Bot(command_prefix=BOT_PREFIX)


@client.command()
async def state_game():
    possible_responses = [
        'Possible question 1',
        'Possible question2',
        'Possible question 3',
    ]
    await client.say(random.choice(possible_responses))



async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(server, fmt.format(member, server))

client.run(token)
