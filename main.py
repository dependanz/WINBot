import discord
import logging
import enum
import shlex

import json
import numpy as np

from message_commands import *

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
        self.prefix = config["prefix"]
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
    
    def __init__(self,bot : WINBot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.role_message_id = bot.role_message_id
        # TODO: Import from config file
        self.emoji_map = {
            "1️⃣" : 1001572018505916578,
            "2️⃣" : 1000808509023199304,
            "p_elf" : 1058954911552917525,
            "marky_carebearstare" : 1058954901578854460,
            "kibby_vintage" : 1041173341609918474,
            "mc_diamond" : 1032863900049350746,
            "bren_AHHHHHH" : 1017199500080730244,
            "josh_swole" : 1058457944695509174,
        }
        # TODO: Make a class for commands instead of having redundancy
        # TODO: Import from config file
        self.message_command_map = {
            f"{self.bot.prefix}ping" : ping,
            f"{self.bot.prefix}WINDER" : winder,
            f"{self.bot.prefix}set_note" : set_note,
            f"{self.bot.prefix}sn" : set_note,
            f"{self.bot.prefix}read_note" : read_note,
            f"{self.bot.prefix}rn" : read_note,
            f"{self.bot.prefix}delete_note" : delete_note,
            f"{self.bot.prefix}dn" : delete_note,
            f"{self.bot.prefix}list_notes" : list_notes,
            f"{self.bot.prefix}ln" : list_notes
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
            role_id = self.emoji_map[payload.emoji.name]
        except KeyError:
            return
        
        role = guild.get_role(role_id)
        if role is None:
            # logging.log(logging.DEBUG, "Role does not exist")
            return
        
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
            role_id = self.emoji_map[payload.emoji.name]
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
    
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        # Prefix message commands
        if message.content.startswith(self.bot.prefix):
            try:
                args = shlex.split(message.content)
                command = self.message_command_map[args[0]]
                await command(message, *args[1:])
            except KeyError:
                pass
            
        
"""
    Start bot
"""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = WINBotClient(bot, intents=intents)
client.run(bot.token, log_handler=bot.log_handler, log_level=bot.log_level)
