"""
    Feature: Simple Notes
"""
import discord
import json
from typing import Dict, List, Union, Optional, Callable
from features.core import *

@verify_sm
async def set(interaction: Optional[discord.Interaction] = None,
              message: Optional[discord.Message] = None,
              key: str = "",
              value: str = ""):
    title = "Notes"
    desc  = f'Note "{key}" set to "{value}"'
    color = SUCCESS_COLOR
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        notes[key] = value
        with open("notes.json", "w") as f:
            json.dump(notes, f)
    except FileNotFoundError:
        desc = "An error occurred, maybe try again in a bit!"
        color = FAIL_COLOR
        
    await send_embed[interaction is not None](sm_switch(interaction, message),title,desc,color)
    await sm_message(interaction,message).delete()

@verify_sm
async def read(interaction: Optional[discord.Interaction] = None,
               message: Optional[discord.Message] = None,
               key: str = ""):
    with open("notes.json","r+") as f:
        notes = json.load(f)
    title = f'Notes: "{key}"'
    desc  = f'"{key}" not found in the notes. You can see which notes are available with the command "list_notes"'
    color = FAIL_COLOR
    
    try:
        desc = f'"{notes[key]}""'
        color = SUCCESS_COLOR
    except KeyError:
        pass
        
    await send_embed[interaction is not None](sm_switch(interaction, message),title,desc,color)
    await sm_message(interaction,message).delete()
    
@verify_sm
async def delete(interaction: Optional[discord.Interaction] = None,
                 message: Optional[discord.Message] = None,
                 key: str = ""):
    title = f'Notes:'
    desc  = f'Note "{key}" deleted.'
    color = SUCCESS_COLOR
    try:
        with open("notes.json","r+") as f:
            notes = json.load(f)
        del notes[key]
        with open("notes.json", "w") as f:
            json.dump(notes, f)
    except FileNotFoundError:
        desc = "An error occurred, maybe try again in a bit!"
        color = FAIL_COLOR
    except KeyError:
        desc = f'"{key}" not found in the notes. You can see which notes are available with the command "list_notes"'
        color = FAIL_COLOR
        
    await send_embed[interaction is not None](sm_switch(interaction, message),title,desc,color)
    await sm_message(interaction,message).delete()
    
@verify_sm
async def list(interaction: Optional[discord.Interaction] = None,
               message: Optional[discord.Message] = None):
    try:
        with open("notes.json","r") as f:
            notes = json.load(f)
        
        embed = discord.Embed(title="Notes", description="Your note pad:", color=0x37b337)
        alpha_notes = sorted(notes.items(), key=lambda x:x[0])
        for k, v in alpha_notes:
            if k == "_": continue
            embed.add_field(name=f'"{k}"', value=f'"{v}"', inline=True)
        
        await sm_channel(interaction, message).send(embeds=[embed])
    except FileNotFoundError:
        await send_embed[interaction is not None](sm_switch(interaction, message),"Notes","An error occurred, maybe try again in a bit!",FAIL_COLOR)
        
    await sm_message(interaction,message).delete()