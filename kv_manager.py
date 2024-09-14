# kv_manager.py

import os
import redis
from pydantic import BaseModel

# Constants
MAX_GUESSES = 6

class Puzzle(BaseModel):
    date: str
    word_length: int
    word_type: str
    synonym: str
    definition: str
    pronunciation: str # Should be file
    solution: str

class UserProgress(BaseModel):
    guesses: int = 0
    completed: bool = False
    won: bool = False

class KV:
    def __init__(self, url: str = None):
        self.url = os.getenv("KV_URL", "redis://localhost:6379")
        if url:
            self.url = url
        self.rc = redis.from_url(url=self.url) # redis client

    def set_puzzle(self, date: str, puzzle: Puzzle) -> bool:
        return self.rc.hset("puzzle", key=date, value=puzzle.model_dump_json())

    def get_puzzle(self, date: str) -> Puzzle:
        result = self.rc.hget(name="puzzle", key=date)
        if not result:
            raise Exception(f"Puzzle: {date} not found!")
        return Puzzle.model_validate_json(result)

    def set_puzzles(self, puzzles: dict[str, Puzzle]) -> bool:
        for date, puzzle in puzzles.items():
            self.set_puzzle(date=date, puzzle=puzzle)

    def get_puzzles(self) -> dict[str, Puzzle]:
        result = self.rc.hgetall("puzzle")
        return {k.decode(): Puzzle.model_validate_json(v) for k, v in result.items()}

    def set_user_progress(self, uid: str, date: str, progress: UserProgress) -> bool:
        return self.rc.hset(f"user:{uid}:puzzle", key=date, value=progress.model_dump_json())

    def get_user_progress(self, uid: str, date: str) -> UserProgress:
        result: UserProgress = self.rc.hget(f"user:{uid}:puzzle", key=date)
        return UserProgress.model_validate_json(result) if result else UserProgress()
    
    def get_user_puzzles(self, uid: str) -> dict[str, UserProgress]:
        result = self.rc.hgetall(f"user:{uid}:puzzle")
        return {k.decode(): UserProgress.model_validate_json(v) for k, v in result.items()}
    
    def guess(self, date: str, uid: str, guess: str) -> bool:
        # Get existing data
        progress = self.get_user_progress(uid, date)
        puzzle = self.get_puzzle(date)
        solution = puzzle.solution
        
        # Determine new user data
        guesses = progress.guesses + 1
        completed = guess == solution or guesses >= MAX_GUESSES
        won = guess == solution
        progress = UserProgress(guesses=guesses, completed=completed, won=won)

        # Set new user data
        return self.set_user_progress(uid, date, progress)

    def get_user_stats(self, uid: str) -> dict:
        puzzle_data = self.get_user_puzzles(uid)

        stats = {str(i): 0 for i in range(1, MAX_GUESSES + 1)}
        stats["More"] = 0

        for puzzle in puzzle_data.values():
            if not puzzle.completed:
                continue
            
            guesses = puzzle.guesses
            if guesses <= MAX_GUESSES:
                stats[str(guesses)] += 1
            else:
                stats["More"] += 1
        
        return stats