"""
    Feature: Admin Controls
"""
import discord
import json
import requests
import numpy as np
from typing import Dict, List, Union, Optional, Callable
from features.core import *
from obj_types import *

"""
    Flush channel: Delete a bunch of messages
"""
@verify_sm
async def flush_channel(interaction: Optional[discord.Interaction] = None,
                        message: Optional[discord.Message] = None,
                        user_or_limit: str = "",
                        limit: int = 100):

    title = "Admin"
    desc  = f'Flushing output for channel: #{sm_channel(interaction,message).name}'
    color = SUCCESS_COLOR
    
    limit = limit
    user = None
    
    if user_or_limit.isdigit():
        limit = int(user_or_limit)
    else:
        user_search = re.findall(r"@(\d+)",user_or_limit)
        user = sm_message(interaction,message).guild.get_member(int(user_search[0]))
    
    role = discord.utils.find(lambda r: r.name == 'friend', sm_message(interaction,message).guild.roles)
    if role not in sm_message(interaction,message).author.roles:
        color = FAIL_COLOR
        desc = "Member is not an admin. Can't use this command!"
        await send_embed[interaction is not None](sm_switch(interaction, message),title,desc,color)
    else:
        color = SUCCESS_COLOR
        whitelist = [sm_message(interaction,message)]
        await send_embed[interaction is not None](sm_switch(interaction, message),title,desc,color)
        await h_flush(sm_channel(interaction,message), user, whitelist, limit + len(whitelist) + 1)
    
    await sm_message(interaction,message).delete()

"""
    Flush Helper
"""
async def h_flush(channel: discord.TextChannel,
                  user: Optional[discord.User], 
                  whitelist: List[discord.Message],
                  limit: int = 100):
    cond = (lambda u1, u2 : True) if user is None else (lambda u1,u2 : u1 == u2)
    skip = False
    async for msg in channel.history(limit=limit):
        if not skip:
            skip = True
            continue
        if cond(msg.author, user) and msg not in whitelist:
            await msg.delete()
            
"""
    echo
"""
@verify_sm
async def echo(interaction: Optional[discord.Interaction] = None,
               message: Optional[discord.Message] = None,
               msg: str = "",
               rep: int = 1):

    title = "Admin"
    desc  = f'Echoing: "{msg}" {rep} times'
    color = SUCCESS_COLOR
    
    await send_embed[interaction is not None](sm_switch(interaction,message), title, desc, color)
    for i in range(rep):
        await send_message[interaction is not None](sm_switch(interaction, message), msg, None)
    await sm_message(interaction,message).delete()
    
"""
    Create Role
        TODO: Check if role exists first
"""
@verify_sm
async def create_role(interaction: Optional[discord.Interaction] = None,
                    message: Optional[discord.Message] = None,
                    name: str = ""):
    
    await message.guild.create_role(name=name,
                                    colour=discord.Colour(np.random.randint(0,2**24)))
    await send_embed[interaction is not None](sm_switch(interaction,message), 
                                              'Admin', 
                                              f'Created role: {name}', 
                                              SUCCESS_COLOR)
    await sm_message(interaction,message).delete()
    
"""
    Create Github Issue
"""
@verify_sm
async def create_git_issue(interaction: Optional[discord.Interaction] = None,
                        message: Optional[discord.Message] = None,
                        auth_token="",
                        repo_owner="dependanz",
                        title="", 
                        body="", 
                        assignee=None, 
                        milestone=None, 
                        labels=[]):

    url = f'https://api.github.com/repos/{repo_owner}/WINBot/issues'
    issue = {'title': title,
            'body': body,
            'labels': labels}
    if assignee is not None:
        issue['assignee'] = assignee
    if milestone is not None:
        issue['milestone'] = milestone
        
    r = requests.post(
        url=url,
        headers = {'Authorization': 'Bearer ' + auth_token},
        data=json.dumps(issue)
    )
    
    if r.status_code == 201:
        await send_embed[interaction is not None](sm_switch(interaction, message), 
                                                  "Admin: Git", 
                                                  f'Successfully created issue "**{title}**"', 
                                                  SUCCESS_COLOR, 
                                                  5)
    else:
        await send_embed[interaction is not None](sm_switch(interaction, message), 
                                                  "Admin: Git", 
                                                  f'Error creating issue "**{title}**"', 
                                                  FAIL_COLOR, 
                                                  5)