import discord
import json
import numpy as np

async def ping(message: discord.Message, *args):
    await message.channel.send('pong' if np.random.uniform(0,1) > 0.01 else 'ping me again, I dare you..')

async def winder(message: discord.Message, *args):
    await message.channel.send(["Nope, not gonna happen", 
                          "stop it. get some help", 
                          "Ew. take a good look in the mirror.",
                          "Drink some water you thirsty boy"][np.random.randint(0,4)])

"""
    Simple Discord Notepad
        For things like mc coordinates, important dates, etc.
"""

"""
    Set note
"""
async def set_note(message: discord.Message, *args):
    if len(args) != 2:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Not enough or too many arguments given (You can use quotations marks for *note_text*): set_note [name_of_note] [note_text]", color=0xb33737)])
        return
    
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        notes[args[0]] = args[1]
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'Note "{args[0]}" set to "{args[1]}"', color=0x37b337)])
    except FileNotFoundError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="An error occurred, maybe try again in a bit!", color=0xb33737)])

"""
    Read note
"""
async def read_note(message: discord.Message, *args):
    if len(args) != 1:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Not enough or too many arguments given: read_note [name_of_note]", color=0xb33737)])
        return
    
    with open("notes.json","r+") as f:
        notes = json.load(f)
    try:
        await message.channel.send(embeds=[discord.Embed(title=f'Notes: "{args[0]}"', 
                                                   description=f'"{notes[args[0]]}"', color=0x37b337)])
    except KeyError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'"{args[0]}" not found in the notes. You can see which notes are available with the command "list_notes"', color=0xb33737)])

"""
    Delete note
"""
async def delete_note(message: discord.Message, *args):
    if len(args) != 1:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Not enough or too many arguments given: delete_note [name_of_note]", color=0xb33737)])
        return
    
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        del notes[args[0]]
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'Note "{args[0]}" deleted.', color=0x37b337)])
    except FileNotFoundError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="An error occurred, maybe try again in a bit!", color=0xb33737)])
    except KeyError:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description=f'"{args[0]}" not found in the notes. You can see which notes are available with the command "list_notes"', color=0xb33737)])

"""
    List notes
"""
async def list_notes(message: discord.Message, *args):
    if len(args) != 0:
        await message.channel.send(embeds=[discord.Embed(title="Notes", 
                                                   description="Too many arguments given: list_notes", color=0xb33737)])
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
                                                   description="An error occurred, maybe try again in a bit!", color=0xb33737)])