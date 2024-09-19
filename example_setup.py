# test.py

from dotenv import load_dotenv
from core.game_manager import GameManager
from db.kv_manager import KeyValueManager
from example_data import *

load_dotenv()
kv = KeyValueManager()
gm = GameManager(kv)

# Set and get puzzle
def setup():
    kv.set_puzzles(puzzles=puzzles)

setup()

# userid = "user_1"
# userid2 = "user_2"
# 
# gm.guess(date1, userid, "calm")
# 
# print(kv.get_user_progress(userid, date1))
# print(kv.get_user_puzzles(userid))
# print(kv.get_puzzle(date1))
# print(gm.get_user_stats(userid))
