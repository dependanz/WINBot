"""
    Slash Commands
        Functionality for slash commands '/'
        
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
from discord.ext import commands

import json
import re
from typing import Dict, List, Union, Optional, Callable, Tuple
from functools import partial
import numpy as np
from obj_types import SlashCommandKwargType, SlashCommandArgType

"""
    Command Map
"""
_c = 0
command_pairs: List[Tuple[str,str]] = [
    ("ping", 'test ping; expected output: "pong"')
]
command_map: Dict[str, Tuple[Callable, str]] = dict()

# [START] Simple Discord Notepad
# [DESC] For things like mc coordinates, important dates, etc.

# [END] Simple Discord Notepad

# [START] Miscellaneous
# [DESC] 

async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('pong' if np.random.uniform(0,1) > 0.01 else 'ping me again, I dare you..', 
                                            delete_after=5)
command_map[command_pairs[_c][0]] = [ping, command_pairs[_c][1]]
_c += 1

# [END] Simple Discord Notepad

assert _c == len(command_pairs), "ERROR: Not enough functions defined"