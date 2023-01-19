import re
import discord
import json
import asyncio
from typing import Any, Dict, List, Union, Optional, Callable

SUCCESS_COLOR = 0x37b337
FAIL_COLOR = 0xb33737

async def async_range(count):
    for i in range(count):
        yield i
        await asyncio.sleep(0.0)

def verify_user_id(id):
    user_search = re.findall(r"@(\d+)",id)
    if user_search == []:
        return False
    elif not user_search[0].isdigit():
        return False
    return True

def verify_positive_number(x: str,nonnegative=False):
    if(x.isdigit()):
        return int(x) >= 0 if nonnegative else int(x) > 0
    return False

def verify_leq(x: str, a: int):
    if(x.isdigit()):
        return int(x) <= a
    return False

"""
    verify_message_args decorator:
        conds: verification conditions (boolean functions)
        fail_descriptions: on fail, return embed with this description (<usage> is replaced with the usage string)
        usage: usage string
        TODO: Fix this
"""
def verify_message_args(*,
                conds: List[Callable],
                fail_descriptions: List[str],
                usage: str):
    def h_verify_args(func: Callable[[Optional[discord.Message], List, Dict], None]):
        async def w_verify_args(message: discord.Message, *args, **kwargs):
            kwargs['usage'] = usage
            assert len(fail_descriptions) == len(conds), "Not enough fail descriptiions for list of conditions"
            for i, c in enumerate(conds):
                if not c(message,args,kwargs):
                    fail_description = fail_descriptions[i].replace("<usage>",usage)
                    await message.channel.send(embeds=[discord.Embed(title="Error", description=fail_description, color=FAIL_COLOR)], delete_after=10)
                    await message.channel.delete_messages([message])
                    return
            await func(message, *args, **kwargs)
            # await message.channel.delete_messages([message])
        return w_verify_args
    return h_verify_args

def verify_sm(func: Callable[[Optional[discord.Interaction], Optional[discord.Message], List, Dict], None]):
    async def h_verify_sm(interaction: Optional[discord.Interaction] = None, 
                          message: Optional[discord.Message] = None,
                          *args, **kwargs):
        assert (interaction is not None and message is None) or (interaction is None and message is not None), "Either Interaction or Message must not be None, not both."
        await func(interaction, message, *args, **kwargs)
    return h_verify_sm

def sm_switch(interaction: discord.Interaction = None,
              message: discord.Message = None) -> Union[discord.Interaction, discord.Message]:
    if interaction is not None:
        return interaction
    else:
        return message

def sm_channel(interaction: discord.Interaction = None,
               message: discord.Message = None) -> discord.ChannelType:
    if interaction is not None:
        return interaction.message.channel 
    else:
        return message.channel

def sm_message(interaction: discord.Interaction = None,
               message: discord.Message = None) -> discord.Message:
    if interaction is not None:
        return interaction.message
    else:
        return message

"""
    Send Embed
"""
async def s_send_embed(interaction: discord.Interaction,
                       title: str,
                       desc: str,
                       color: int,
                       delete_after: Union[int,None] = 5):
    await interaction.response.send_message(embeds=[discord.Embed(title=title, 
                                            description=desc, 
                                            color=color)], 
                                            delete_after=delete_after)
    
async def m_send_embed(message: discord.Message,
                       title: str,
                       desc: str,
                       color: int,
                       delete_after: Union[int,None] = 5):
    await message.channel.send(embeds=[discord.Embed(title=title, 
                                description=desc, 
                                color=color)], 
                                delete_after=delete_after)
    
send_embed: Dict[bool, Callable[[Union[discord.Interaction, discord.Message],str,str,int,int], None]] = {
    True : s_send_embed,
    False : m_send_embed
}

"""
    Send Message
"""
async def s_send_message(interaction: discord.Interaction,
                         content : Union[Any,None] = "",
                         delete_after: Union[int,None] = 5):
    await interaction.response.send_message(content=content,
                                            delete_after=delete_after)
    
async def m_send_message(message: discord.Message,
                         content : Union[Any,None] = "",
                         delete_after: Union[int,None] = 5):
    await message.channel.send(content=content,
                               delete_after=delete_after)
    
send_message: Dict[bool, Callable[[Union[discord.Interaction, discord.Message],str,int], None]] = {
    True : s_send_message,
    False : m_send_message
}

