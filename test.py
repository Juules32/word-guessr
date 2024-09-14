# test.py

from dotenv import load_dotenv
from game_manager import GameManager
from kv_manager import KeyValueManager
from data import *

load_dotenv()
kv = KeyValueManager()
gm = GameManager(kv)

# Set and get puzzle
kv.set_puzzles(puzzles=puzzles)

userid = "user_1"
userid2 = "user_2"

gm.guess(date1, userid, "calm")

print(kv.get_user_progress(userid, date1))
print(kv.get_user_puzzles(userid))
print(kv.get_puzzle(date1))
print(gm.get_user_stats(userid))
