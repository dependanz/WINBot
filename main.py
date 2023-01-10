import discord
import logging
import enum

import json
import numpy as np

"""
    Load config vars (and log handlers)
    TODO: Multiple loggers in the future
"""
class WINBot:
    def __init__(self,config_file="config.json",
                 log_file="bot.log") -> None:
        with open(config_file,"r") as f:
            config = json.load(f)
        self.dev = config["dev"]
        self.token = config["bot_token"]
        self.role_message_id = int(config["role_message_id"])
        
        self.log_handler = logging.FileHandler(filename=log_file,encoding='utf-8',mode='w')
        self.log_level = logging.DEBUG if self.dev else logging.INFO
        
bot = WINBot()

"""
    Client
"""

# class VStatus(enum.Enum):
#     SUCCESS = 1,
#     SOFT_ERROR = 2,
#     ERROR = 3

class WINBotClient(discord.Client):
    
    def __init__(self,bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_message_id = bot.role_message_id
        self.emojimap = {
            "1️⃣" : 1001572018505916578,
            "2️⃣" : 1000808509023199304,
            "p_elf" : 1058954911552917525,
            "marky_carebearstare" : 1058954901578854460,
            "kibby_vintage" : 1041173341609918474,
            "mc_diamond" : 1032863900049350746,
            "bren_AHHHHHH" : 1017199500080730244,
            "josh_swole" : 1058457944695509174,
        }
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.role_message_id:
            return
        
        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return
        
        try:
            role_id = self.emojimap[payload.emoji.name]
        except KeyError:
            return
        
        role = guild.get_role(role_id)
        if role is None:
            logging.log(logging.DEBUG, "Role does not exist")
            return
        
        logging.log(logging.DEBUG, "Got there")
        print("Got there", role)
        try:
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # TODO: Give member a private message to try again or send message to admins
            pass
        
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != self.role_message_id:
            return
        
        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return
        
        try:
            role_id = self.emojimap[payload.emoji.name]
            print(role_id)
        except KeyError:
            return
        
        role = guild.get_role(role_id)
        if role is None:
            logging.log(logging.DEBUG, "Role does not exist")
            return
        
        member = guild.get_member(payload.user_id)
        if member is None:
            return
        
        try:
            await member.remove_roles(role)
        except discord.HTTPException:
            # TODO: Give member a private message to try again or send message to admins
            pass
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$ping'):
            await message.channel.send('pong')
        if message.content.startswith('$WINDER'):
            await message.channel.send(["Nope, not gonna happen", 
                                        "stop it. get some help", 
                                        "Ew. take a good look in the mirror.",
                                        "Drink some water you thirsty boy"][np.random.randint(0,4)])
    

"""
    Start bot
"""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# @client.event
client = WINBotClient(bot, intents=intents)
client.run(bot.token, log_handler=bot.log_handler, log_level=bot.log_level)
