# main.py

from dotenv import load_dotenv
from game_manager import GameManager
from fastapi import FastAPI
from kv_manager import KeyValueManager
from model import State

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

gm = GameManager(kv=KeyValueManager())

app = FastAPI()

@app.get("/{date}/{userid}", response_model=State)
def get_state(date: str, userid: str):
    return gm.get_state(date, userid)

@app.put("/{date}/{userid}/{guess}", response_model=State)
def put_guess(date: str, userid: str, guess: str):
    gm.guess(date, userid, guess)
    return gm.get_state(date, userid)