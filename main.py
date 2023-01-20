"""
    Main code for WINBot
        Uses discord.py
        I dislike stacked conditionals, so we use maps (map<str,callable>)
        I like typing, please be consistent in typing
    
    Sections:
        (a) WINBot Config Class
        (b) WINBot Main Client Class
        (c) "main"
"""
import discord
import logging
import shlex
from typing import Dict, List, Union
from functools import partial

import json
import numpy as np

from message_commands import *
import slash_commands

from features.core import async_range

"""
    Load config vars (and log handlers)
    TODO: Multiple loggers in the future
"""
class WINBot:
    def __init__(self,config_file:str="config.json",
                 log_file:str="bot.log") -> None:
        with open(config_file,"r") as f:
            config = json.load(f)
        self.dev = config["dev"]
        self.token = config["bot_token"]
        self.guild_id = config["guild_id"]
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
    
    def __init__(self,bot : WINBot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.tree = discord.app_commands.CommandTree(self)
        for k,v in slash_commands.command_map.items():
            @self.tree.command(name=k,description=v[1])
            async def w_slash_command(interaction: discord.Interaction):
                await v[0](interaction)
        
        self.role_message_id = bot.role_message_id
        # TODO: Import from config file
        self.emoji_map = {
            "1️⃣" : 1001572018505916578,
            "2️⃣" : 1000808509023199304,
            "3️⃣" : 1064864830483349564,
            "4️⃣" : 1065422994291294229,
            "5️⃣" : 1065637547788746782,
            "6️⃣" : 1065857416782151800,
            "🥳" : 1062816302911193098,
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
            f"{self.bot.prefix}set_note" : m_set_note,
            f"{self.bot.prefix}sn" : m_set_note,
            f"{self.bot.prefix}read_note" : m_read_note,
            f"{self.bot.prefix}rn" : m_read_note,
            f"{self.bot.prefix}delete_note" : m_delete_note,
            f"{self.bot.prefix}dn" : m_delete_note,
            f"{self.bot.prefix}list_notes" : m_list_notes,
            f"{self.bot.prefix}ln" : m_list_notes,
            
            f"{self.bot.prefix}admin_flush_channel" : m_flush_channel,
            f"{self.bot.prefix}aFlushChannel" : m_flush_channel,
            f"{self.bot.prefix}admin_echo" : m_echo,
            f"{self.bot.prefix}aEcho" : m_echo,
            f"{self.bot.prefix}admin_create_role" : m_create_role,
            f"{self.bot.prefix}aCreateRole" : m_create_role,
            
            f"{self.bot.prefix}ping" : m_ping,
            f"{self.bot.prefix}WINDER" : m_winder,
            f"{self.bot.prefix}capitalize" : m_capitalize,
            f"{self.bot.prefix}spongecap" : m_spongecap,
        }
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.tree.sync()
    
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
            return
        
        try:
            await payload.member.add_roles(role)
        except discord.HTTPException:
            pass
        
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
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
            command_list = list(map(lambda x : x.strip(), message.content.split("&&")))
            command_list = list(map(lambda x : shlex.split(x), command_list))
            async for i in async_range(len(command_list)):
                command = self.message_command_map[command_list[i][0]]
                args = command_list[i][1:]
                try:
                    _ = await command(message, *args, **{'client':self})
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