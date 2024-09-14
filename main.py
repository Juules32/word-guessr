# main.py

from dotenv import load_dotenv
from game_manager import GameManager
from fastapi import FastAPI
from kv_manager import KeyValueManager

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

gm = GameManager(kv=KeyValueManager())

app = FastAPI()

@app.get("/{date}/{userid}")
def get_puzzle(date: str, userid: str):
    return gm.get_puzzle(date, userid)
