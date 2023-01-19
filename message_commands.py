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
from obj_types import MessageCommandKwargType, MessageCommandArgType

import features.simplenotes as simplenotes
import features.admin as admin
import features.misc as misc
from features.core import verify_message_args, verify_user_id, verify_positive_number
from features.logic import *

# [START] Simple Discord Notepad
# [DESC] For things like mc coordinates, important dates, etc.

"""
    Set note
"""
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) == 2
    ],
    fail_descriptions = [
        "Not enough or too many arguments given (You can use quotations marks for *note_text*): <usage>"
    ],
    usage="set_note [name_of_note] [note_text]"
)
async def m_set_note(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await simplenotes.set(message=message, key=args[0], value=args[1])
    
"""
    Read note
"""
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) == 1,
    ],
    fail_descriptions = [
        "Not enough or too many arguments given (You can use quotations marks for *note_text*): <usage>"
    ],
    usage="read_note [name_of_note]"
)
async def m_read_note(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await simplenotes.read(message=message, key=args[0])

"""
    Delete note
"""
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) == 1,
    ],
    fail_descriptions = [
        "Not enough or too many arguments given: <usage>"
    ],
    usage="delete_note [name_of_note]"
)
async def m_delete_note(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await simplenotes.delete(message=message, key=args[0])
    
    
"""
    List notes
"""
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) == 0,
    ],
    fail_descriptions = [
        "Too many arguments given: <usage>"
    ],
    usage="list_notes"
)
async def m_list_notes(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await simplenotes.list(message=message)
    
# [END] Simple Discord Notepad

# [START] Admin Tools

"""
    Delete all messages from WINBot for a specific channel
        TODO: History Limits
"""
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) in [0,1,2],
        lambda m,a,k : ((verify_user_id(a[0])) if not a[0].isdigit() else True) if len(a) == 1 else True,
        lambda m,a,k : (not a[0].isdigit()) if len(a) == 2 else True,
        lambda m,a,k : (verify_user_id(a[0])) if len(a) == 2 else True,
        lambda m,a,k : (a[1].isdigit()) if len(a) == 2 else True,
        lambda m,a,k : (int_posinf(a[1]) <= 100) if len(a) == 2 else True,
    ],
    fail_descriptions = [
        "Too many arguments given: <usage>",
        "Member not found.",
        "Wrong usage of command: <usage>",
        "Member not found.",
        "Second parameter needs to be an integer <= 100: <usage>",
        "Second parameter needs to be an integer <= 100: <usage>"
    ],
    usage="[admin_flush_channel | aFlushChannel] [@<member> | message limit] [@<member>:message limit]"
)
async def m_flush_channel(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    user_or_limit = ""
    limit = 100
    user_or_limit = args[0]
    if len(args) == 2:
        limit = int(args[1])
        
    await admin.flush_channel(interaction=None,
                              message=message,
                              user_or_limit=user_or_limit,
                              limit=limit)
    
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) in [0,1,2],
        lambda m,a,k : (verify_positive_number(a[1])) if len(a) == 2 else True,
    ],
    fail_descriptions = [
        "Wrong usage of command: <usage>",
        "Repetitions must be a positive number: <usage>",
    ],
    usage="echo [message] [message:repetitions]"
)
async def m_echo(message: discord.Message, 
                 *args: MessageCommandArgType, 
                 **kwargs: MessageCommandKwargType):
    rep = 1
    msg = ""
    if len(args) >= 1:
        msg = args[0]
    if len(args) == 2:
        rep = int(args[1])
    await admin.echo(interaction=None,
                     message=message,
                     msg=msg,
                     rep=rep)
            
"""
    Create Roles
"""
@verify_message_args(
    conds=[
        lambda m,a,k : len(a) == 1,
        lambda m,a,k : (verify_positive_number(a[1])) if len(a) == 2 else True,
    ],
    fail_descriptions = [
        "Wrong usage of command: <usage>",
        "Repetitions must be a positive number: <usage>",
    ],
    usage="echo [message] [message:repetitions]"
)
async def m_create_role(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await admin.create_role(message=message,name=args[0])
# [END] Admin Tools

# [START] Miscellaneous
# [DESC] Other functions (ping, memes, etc..)

"""
    ping
"""
async def m_ping(message: discord.Message, *args: MessageCommandArgType, **kwargs:MessageCommandKwargType):
    await misc.ping(message=message)

"""
    winder
"""
async def m_winder(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await misc.easteregg(message=message,egg="winder")

"""
    capitalize:
"""
async def m_capitalize(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await misc.capitalize(None, message)

"""
    spongecap:
        sPoNgEcAp
"""
async def m_spongecap(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):
    await misc.spongecap(None, message)

# async def spongecap(message: discord.Message, *args: MessageCommandArgType, **kwargs: MessageCommandKwargType):

# [END] Miscellaneous:partying_face: