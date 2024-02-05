import os
import config 
os.system('clear')

print(f"BOT VERSION [{config.version}]")
print("Initializing User Commands...")
from .set_up import *
from .profile import profile
from .inventory import *
from .claim import *
from .daily import *
from .datack import *
from .shop import *
from .farm_shop import *
from .farm_shop_sell import *
from .farm_shop_buy import *
from .home import *
from .prestige import *
from .mining import *
from .settings import *
from .leadboard import *
from .texttonum import *
from .datack import *
from .activecommand import *
from .title import *
from .sell import *
from .buy import *
from .minefinish import *
from .trivia import *
from .switch_pickaxe import *
from .fixlvl import *
from .find_user_id import *