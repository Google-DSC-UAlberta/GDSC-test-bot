import os
import sqlite3
# https://discordpy.readthedocs.io/en/stable/api.html#
import discord

import time
import asyncio
from dotenv import load_dotenv

# load the envionment variables from .env file
load_dotenv()

TOKEN = os.getenv("API_TOKEN")

interval = int(os.getenv("TIMER_INTERVAL"))

class DemoClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.timer_flag = False
        self.valid_messages = {
            "test": "Welcome to UofA GDSC!",
            "code": "```python\n print('showing how python snippets can be displayed on Discord!')```"
        }
        self.connection = sqlite3.connect("test.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            name CHAR(30) PRIMARY KEY,
            password CHAR(30));
        """)
        self.connection.commit()

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')
    
    async def on_message(self, message):
        # a bot message also count as a message, make sure we don't handle bot's messages
        if message.author == self.user:
            return 

        content = message.content
        if content in self.valid_messages:
            await message.reply(self.valid_messages[content])
    
        if content == "timer":
            if self.timer_flag:
                await message.reply("You can only start one timer at a time!")
            else:
                await message.reply(f"Timer have been started! It will display the current time every {interval} seconds!")
                self.timer_flag = True
                while self.timer_flag:
                    await message.channel.send(f"The current time is: {time.ctime()}")
                    # this await on asyncio.sleep() is very important, try take it out and see what happens...
                    # Note: you will get a RuntimeWarning from asyncio without this await keyword below
                    await asyncio.sleep(interval)
        elif content == "stop":
            if self.timer_flag:
                await message.reply("Timer have been stopped!")
                self.timer_flag = False
            else:
                await message.reply("Timer is not started! Enter \"timer\" to start a timer")
        elif content.startswith("create"):
            # create a new table
            msg = content.split(" ")
            self.cursor.execute("""INSERT INTO users(name, password) VALUES(?, ?)""", (msg[1], msg[2]))
            self.connection.commit()
        elif content.startswith("exist"):
            msg = content.split(" ")
            self.cursor.execute("""SELECT * FROM users WHERE name = ?""", (msg[1],))
            result = self.cursor.fetchall()
            if len(result) > 0:
                await message.reply("User exists!")
            else:
                await message.reply("User does not exist!")

client = DemoClient()
client.run(TOKEN)
