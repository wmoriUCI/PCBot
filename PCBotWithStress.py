# POE Price Checker main file
# William Mori

import os
import asyncio

import discord
import PCModule
from collections import defaultdict

import time

with open("PCBotToken.txt", "r") as f:
    token = f.read()
f.close()
token = token.strip()

with open("StressTestBotID.txt", "r") as f:
    STRESS_BOT_ID = f.read()
f.close()
STRESS_BOT_ID = STRESS_BOT_ID.strip()
STRESS_BOT_ID = int(STRESS_BOT_ID)  # This could be done in one line, but separate for readability

COMMAND_LIST = '''
Command List
!pc - returns the price of an item in all forms of currency, use syntax "Item Name, Item Base"
!pcp - deletes the price response after 30 seconds
!pcs - puts the price in a spoiler and deletes after 30 seconds -> currently disabled
!pct - puts the price in a txt file and deletes after 30 seconds
!clear - immediately clears all responses to "!pc"
'''

client = discord.Client()

SENT_MESSAGE_DICT = defaultdict(list)
BEGIN = None


async def make_text(txt: str, item_name: str) -> str:
    file_name = item_name + ".txt"
    f = open(file_name, "w")
    f.write(txt)
    f.close()
    return file_name


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if message.author.id == STRESS_BOT_ID and message.content[0] == "!":  # This is StressTestBot's ID
        start = time.time()
        global BEGIN  # Very unhappy about this global usage
        await message.channel.send("Got pc request at time:" + str(round(start - BEGIN, 4)), delete_after=60)
    elif message.author.bot:
        return

    message_list = message.content.split()
    if message_list[0][0] == "!":
        if message_list[0] == "!pc":
            item = " ".join(message_list[1:])
            item = item.split(',')
            ret_send = await PCModule.searchItem(item[0], item[1].strip())
            sent = await message.channel.send(ret_send)
            SENT_MESSAGE_DICT[message.channel].append(sent)

        elif message_list[0] == "!pcp":
            item = " ".join(message_list[1:])
            item = item.split(',')
            ret_send = await PCModule.searchItem(item[0], item[1].strip())
            sent = await message.channel.send(content=ret_send)
            await asyncio.sleep(30)
            await sent.edit(content="Message removed", delete_after=10.0)

        elif message_list[0] == "!pct":
            item = " ".join(message_list[1:])
            item = item.split(',')
            content = "Price info in spoiler, download the txt file\n"
            ret_send = await PCModule.searchItem(item[0], item[1].strip())
            if message.author.id == STRESS_BOT_ID:  # This is StressTestBot's ID
                time_taken = "Time taken to process = " + str(round(time.time() - start, 4)) + "\n"
                content += time_taken
            file_name = await make_text(ret_send, item[0])
            if message.author.id == STRESS_BOT_ID:
                content += "Time taken to send message = " + str(round(time.time() - start, 4)) + "\n"
            sent = await message.channel.send(content=content,
                                              file=discord.File(file_name, spoiler=True))
            os.remove(file_name)
            await asyncio.sleep(30)
            await sent.edit(content="Message removed", delete_after=10.0)

        elif message_list[0] == "!clear":
            for i in SENT_MESSAGE_DICT[message.channel]:
                await i.edit(delete_after=0.0)
            await message.channel.send(content="Price Checks cleared", delete_after=10)

        elif message_list[0] == "!stress":
            BEGIN = time.time()
            await message.channel.send("Start stress test", delete_after=10)

        elif message_list[0] == "!help":
            await message.channel.send(COMMAND_LIST)
        else:
            await message.channel.send("Invalid command, command is either unknown or has improper spacing\n\
Try calling help for a list of commands")


client.run(token)
