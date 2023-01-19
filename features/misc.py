"""
    Feature: Miscellaneous Features
"""
import discord
import json
import numpy as np
from typing import Dict, List, Union, Optional, Callable
from features.core import *
from obj_types import *
            
"""
    ping
"""
@verify_sm
async def ping(interaction: Optional[discord.Interaction] = None,
               message: Optional[discord.Message] = None):
    await sm_message(interaction,message).channel.send('pong' if np.random.uniform(0,1) > 0.01 else 'ping me again, I dare you..', 
                               delete_after=5)

"""
    eastereggs:
        winder
"""
@verify_sm
async def easteregg(interaction: Optional[discord.Interaction] = None,
                    message: Optional[discord.Message] = None,
                    egg=""):
    if egg == "winder":
        await message.channel.send(["Nope, not gonna happen", 
                                    "stop it. get some help", 
                                    "Ew. take a good look in the mirror.",
                                    "Meow for me! My kitten.",
                                    "Drink some water you thirsty boy"][np.random.randint(0,4)], 
                                delete_after=5)

"""
    capitalize
"""
@verify_sm
async def capitalize(interaction: Optional[discord.Interaction] = None,
                    message: Optional[discord.Message] = None):
    temp = None
    skip = False
    async for msg in sm_channel(interaction,message).history(limit=5):
        if not skip:
            skip = True
            continue
        temp = msg
        break
    if temp is None: return
    await send_message[interaction is not None](sm_switch(interaction, message), h_capitalize(msg.content), None)
    await sm_message(interaction,message).delete()

def h_capitalize(msg: Union[str, None]):
    return "".join([msg[i].upper() for i in range(len(msg))])

"""
    sPoNgEcAp
"""
@verify_sm
async def spongecap(interaction: Optional[discord.Interaction] = None,
                    message: Optional[discord.Message] = None):
    temp = None
    skip = False
    async for msg in sm_channel(interaction,message).history(limit=5):
        if not skip:
            skip = True
            continue
        temp = msg
        break
    if temp is None: return
    await send_message[interaction is not None](sm_switch(interaction, message), h_spongecap(msg.content), None)
    await sm_message(interaction,message).delete()

def h_spongecap(msg: Union[str, None]):
    return "".join([msg[i].lower() if i % 2 == 0 else msg[i].upper() for i in range(len(msg))])