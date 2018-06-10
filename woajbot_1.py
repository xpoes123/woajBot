#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import datetime
import json
import os
import random
import string
import sys
import math
import discord
from discord.ext import commands
# from urbandictionary_top import udtop

# TODO New Commands
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
1: Do this!

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


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
    print("WOAJ!!! You need a token to go online. Use 'Main' or 'Test")
    exit(0)

print("Token being used: {}".format(jsontoken.get("token")))
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
    if user_id == client.user:
        return

    # Ping Command
    if message.content.upper().startswith(".PING"):
        await client.send_message(message.channel, "Pong! :ping_pong:")

client.run(token)
