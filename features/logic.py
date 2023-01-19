import re
import discord
import json
import math
from typing import Dict, List, Union, Optional, Callable

def int_posinf(x: int):
    if not str(x).isdigit():
        return math.inf
    return int(x)

def int_neginf(x: int):
    if not str(x).isdigit():
        return -math.inf
    return int(x)

ak_true = lambda a,k : True

"""
    ifnode
"""
def ifnode(c1: Callable[[],bool] = ak_true,
           c2: Callable[[],bool] = ak_true,
           c1_args: List = [],
           c2_args: List = [],
           c1_kwargs: Dict = {},
           c2_kwargs: Dict = {},):
    if not c1(c1_args,c1_kwargs):
        return False
    return c2(c2_args,c2_kwargs)