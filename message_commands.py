"""
    Message Commands
        Functionality when a message is prefixed with <prefix>
        
    Notes:
        (a) Functions prefixed with "h_" are "helpers" and should only be called by functions in this file. This is only a 
            function naming convention, as we don't really restrict function scopes in python.
        (b) Groups of functions that make up a feature (Like Simple Notes) should be organized between comments as follows:
            (i) # [START] <name of feature> (Indicates the start of a group of functions, or a feature)
            (ii) # [DESC] <description> (Optional description of the feature)
            (iii) # [TODO] <todo description> (What needs to be done in the future for the feature)
            (iv) # [END] <name of feature> (Indicates the end of a feature)
            
    Currently:
        (i) Simple Discord Notepad
        (ii) Admin Tools
        (iii) Miscellaneous

"""
import discord
import json
import re
from typing import Dict, List, Union, Optional, Callable
from functools import partial
import numpy as np

MessageCommandArgType = Union[str,discord.Client]
MessageCommandKwargType = Union[str,discord.Client]

"""
    message_command decorator:
"""
def message_command(usage_str: str):
    def h_message_command(func: Callable):
        def w_message_command(*args, **kwargs):
            kwargs['usage'] = usage_str
            return func(*args, **kwargs)
        return w_message_command
    return h_message_command
        

# [START] Simple Discord Notepad
# [DESC] For things like mc coordinates, important dates, etc.

"""
    Set note
"""
async def set_note(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    if len(args) != 2:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                description="Not enough or too many arguments given (You can use quotations marks for *note_text*): set_note [name_of_note] [note_text]", color=0xb33737)], 
                                   delete_after=5)
        return
    
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        notes[args[0]] = args[1]
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'Note "{args[0]}" set to "{args[1]}"', color=0x37b337)], 
                                   delete_after=5)
    except FileNotFoundError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="An error occurred, maybe try again in a bit!", color=0xb33737)], 
                                   delete_after=5)

"""
    Read note
"""
async def read_note(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    if len(args) != 1:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Not enough or too many arguments given: read_note [name_of_note]", color=0xb33737)], 
                                   delete_after=5)
        return
    
    with open("notes.json","r+") as f:
        notes = json.load(f)
    try:
        await message.channel.send(embeds=[discord.Embed(title=f'Notes: "{args[0]}"', 
                                                   description=f'"{notes[args[0]]}"', color=0x37b337)], 
                                   delete_after=5)
    except KeyError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'"{args[0]}" not found in the notes. You can see which notes are available with the command "list_notes"', color=0xb33737)], 
                                   delete_after=5)

"""
    Delete note
"""
async def delete_note(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    if len(args) != 1:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Not enough or too many arguments given: delete_note [name_of_note]", color=0xb33737)], 
                                   delete_after=5)
        return
    
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        del notes[args[0]]
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'Note "{args[0]}" deleted.', color=0x37b337)], 
                                   delete_after=5)
    except FileNotFoundError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="An error occurred, maybe try again in a bit!", color=0xb33737)], 
                                   delete_after=5)
    except KeyError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'"{args[0]}" not found in the notes. You can see which notes are available with the command "list_notes"', color=0xb33737)], 
                                   delete_after=5)

"""
    List notes
"""
async def list_notes(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    if len(args) != 0:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Too many arguments given: list_notes", color=0xb33737)], 
                                   delete_after=5)
        return
    
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        
        embed = discord.Embed(title="Notes", description="Your note pad:", color=0x37b337)
        alpha_notes = sorted(notes.items(), key=lambda x:x[0])
        for k, v in alpha_notes:
            if k == "_": continue
            embed.add_field(name=f'"{k}"', value=f'"{v}"', inline=True)
        
        await message.channel.send(embeds=[embed])
    except FileNotFoundError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="An error occurred, maybe try again in a bit!", color=0xb33737)], 
                                   delete_after=5)
        
# [END] Simple Discord Notepad

# [START] Admin Tools

"""
    Delete all messages from WINBot for a specific channel
        TODO: History Limits
        TODO: So many redundant conditionals... 
"""
@message_command("[admin_flush_channel | aFlushChannel] [@<member> | message limit] [@<member>:message limit]")
async def flush_channel(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    limit = 100
    user = None
    if len(args) == 1:
        if args[0].isdigit():
            limit = int(args[0])
        else:
            user_search = re.findall(r"@(\d+)",args[0])
            if user_search == []:
                await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                    description="Member not found.", color=0xb33737)], 
                                    delete_after=5)
                return
            elif not user_search[0].isdigit():
                await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                    description="Member not found.", color=0xb33737)], 
                                    delete_after=5)
                return
            user = message.guild.get_member(int(user_search[0]))
                
    elif len(args) == 2:
        if args[0].isdigit():
            await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                   description=f"Wrong usage of command: {kwargs['usage']}", color=0xb33737)], 
                                   delete_after=5)
            return
        else:
            user_search = re.findall(r"@(\d+)",args[0])
            if user_search == []:
                await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                    description="Member not found.", color=0xb33737)], 
                                    delete_after=5)
                return
            elif not user_search[0].isdigit():
                await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                    description="Member not found.", color=0xb33737)], 
                                    delete_after=5)
                return
            user = message.guild.get_member(int(user_search[0]))
            if not args[1].isdigit():
                await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                   description=f"Second parameter needs to be an integer <= 100: {kwargs['usage']}", color=0xb33737)], 
                                   delete_after=5)
                return
            elif int(args[1]) > 100:
                await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                   description=f"Second parameter needs to be an integer <= 100: {kwargs['usage']}", color=0xb33737)], 
                                   delete_after=5)
                return
            else:
                limit = int(args[1])
                if limit <= 0:
                    return
    else:
        await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                   description=f"Too many arguments given: {kwargs['usage']}", color=0xb33737)], 
                                   delete_after=5)
        return
    
    role = discord.utils.find(lambda r: r.name == 'friend', message.guild.roles)
    if role not in message.author.roles:
        await message.channel.send(embeds=[discord.Embed(title="Admin", 
                                                   description="Member is not an admin. Can't use this command!", color=0xb33737)], 
                                   delete_after=5)
        return
    whitelist = [message,
                 await message.channel.send(embeds=[discord.Embed(title=f'Admin', 
                                            description=f'Flushing output for channel: #{message.channel.name}', color=0x37b337)], 
                                            delete_after=5)]
    
    await h_flush(message, user, whitelist, limit + len(whitelist), *args, **kwargs)
    await message.delete()

"""
    Flush Helper
"""
async def h_flush(message: discord.Message, 
                  user: Optional[discord.User], 
                  whitelist: List[discord.Message],
                  limit: int = 100,
                  *args: MessageCommandArgType, 
                  **kwargs: MessageCommandKwargType):
    cond = (lambda u1, u2 : True) if user is None else (lambda u1,u2 : u1 == u2)
    
    async for msg in message.channel.history(limit=limit):
        if cond(msg.author, user) and msg not in whitelist:
            await msg.delete()

# [END] Admin Tools

# [START] Miscellaneous
# [DESC] Other functions (ping, memes, etc..)

"""
    ping
"""
@message_command("ping")
async def ping(message: discord.Message, *args: MessageCommandArgType, **kwargs:MessageCommandKwargType):
    print(kwargs)
    await message.channel.send('pong' if np.random.uniform(0,1) > 0.01 else 'ping me again, I dare you..', 
                               delete_after=5)

"""
    winder
"""
async def winder(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await message.channel.send(["Nope, not gonna happen", 
                                "stop it. get some help", 
                                "Ew. take a good look in the mirror.",
                                "Drink some water you thirsty boy"][np.random.randint(0,4)], 
                               delete_after=5)

# [END] Miscellaneous