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
# from urbandictionary_top import udtop

# TODO New Commands
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
1: Add a level system for the bot and reset the current level system.
2. Create a prompt for when people join the discord.
3. Create a working database of the pb's of people.
4. Quicklinks
5. Release to the public
6. Add the wca database
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_json(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp)

def get_time():
    # Decides if startup is during AM or PM ours (yea damn 'murica time)
    if datetime.datetime.now().hour > 13:
        cur_hour = datetime.datetime.now().hour - 12
        am_or_pm = "PM"
    else:
        cur_hour = datetime.datetime.now().hour
        am_or_pm = "AM"

    # Puts "0" in front of number time
    if datetime.datetime.now().minute < 10:
        cur_min = "0{}".format(datetime.datetime.now().minute)
    else:
        cur_min = datetime.datetime.now().minute

    if datetime.datetime.now().second < 10:
        cur_sec = "0{}".format(datetime.datetime.now().second)
    else:
        cur_sec = datetime.datetime.now().second

    return "{0}:{1}:{2} {3}".format(cur_hour, cur_min, cur_sec, am_or_pm)


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
    print("                          _ ____        __ ")
    print(" _      ______  ____  _  (_) __ )____  / /_")
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
        await client.send_message(message.channel, 'Do `.bot` for all possible commands. ')
        await client.send_message(message.channel, 'Do `.info` for information about the server.')
        await client.send_message(message.channel, 'Do `.ping` responds with PONG')
        await client.send_message(message.channel, 'Do `.xp` to see the amount of xp you currently have.')
        await client.send_message(message.channel, 'Do `.guess` to play a guessing game with the bot.')

#State game
    elif message.content.startswith(".test"):

        print("{0}: {1} requested '.test'".format(get_time(), user_name))

        def get_answer(answer_number):

            if answer_number == 1:

                return "QUESTION ONE"

            elif answer_number == 2:

                return "QUESTION TWO"

            elif answer_number == 3:

                return "3"

            elif answer_number == 4:

                return "4"

            elif answer_number == 5:

                return "5"

            elif answer_number == 6:

                return "6"

            elif answer_number == 7:

                return "7"

            elif answer_number == 8:

                return "8"

            elif answer_number == 9:

                return "9"

        r = random.randint(2, 2)

        question = get_answer(r)

        await client.send_message(message.channel, question)

        if r == 1:
            answer = await client.wait_for_message(channel=message.channel, author=message.author)
            if answer.content == "Alabama":
                await client.send_message(message.channel, "You're correct! :tada:")
            user_add_xp(user_id, 1)
        elif r == 2:
            answer = await client.wait_for_message(channel=message.channel, author=message.author)
            if answer.content == "Alaska":
                    await client.send_message(message.channel, "You're correct! :tada:")
        else:
            return

    elif message.content.startswith('.andrew'):
        await client.send_message(message.channel, 'Guess a number between 1 to 10')

        def andrew_check(m):
            return m.content.isdigit()

        andrew = await client.wait_for_message(timeout=5.0, author=message.author, check=andrew_check)
        answer = random.randint(1, 10)
        if andrew is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(andrew.content) == answer:
            await client.send_message(message.channel, 'You are right!')
            user_add_xp(user_id, 5)
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

    if message.content.lower().startswith(".xp"):
        await client.send_message(message.channel, "You have {} XP!".format(get_xp(message.author.id)))


def user_add_xp(user_id: int, xp: int):
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


client.run(token)