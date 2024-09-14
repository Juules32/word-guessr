# kv_manager.py

import os
import redis
from dotenv import load_dotenv

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

class KV:
    def __init__(self, url: str = None):
        self.url = os.getenv("KV_URL", "redis://localhost:6379")
        if url:
            self.url = url
        self.max_guesses = 6
        self.rc = redis.from_url(url=self.url) # redis client

    def set_puzzle(self, date: str, puzzle_data: dict) -> bool:
        return self.rc.hset("puzzle", key=date, value=str(puzzle_data))

    def get_puzzle(self, date: str) -> dict:
        result = self.rc.hget(name="puzzle", key=date)
        if not result:
            raise Exception(f"Puzzle: {date} not found!")
        return eval(result)

    def get_puzzles(self) -> dict:
        result = self.rc.hgetall("puzzle")
        return {k.decode(): eval(v) for k, v in result.items()}

    def set_user_progress(self, uid: str, date: str, progress: dict) -> bool:
        return self.rc.hset(f"user:{uid}:puzzle", key=date, value=str(progress))

    def get_user_progress(self, uid: str, date: str) -> dict:
        result = self.rc.hget(f"user:{uid}:puzzle", key=date)
        return eval(result) if result else {"guesses": 0, "completed": False, "won": False}
    
    def get_user_puzzles(self, uid: str) -> dict:
        result = self.rc.hgetall(f"user:{uid}:puzzle")
        return {k.decode(): eval(v) for k, v in result.items()}
    
    def guess(self, date: str, uid: str, guess: str) -> None:
        # Get existing data
        progress = self.get_user_progress(uid, date)
        puzzle = self.get_puzzle(date)
        solution = puzzle.get("solution")
        
        # Determine new user data
        guesses = progress["guesses"] + 1
        completed = True if guess == solution or guesses >= self.max_guesses else False
        won = True if guess == solution else False
        progress = {"guesses": guesses, "completed": completed, "won": won}

        # Set new user data
        return self.set_user_progress(uid, date, progress)
