# kv_manager.py

import os
from typing import Optional
import redis
from model import Puzzle, UserProgress

class KeyValueManager:
    def __init__(self, url: str = None):
        self.url = os.getenv("KV_URL", "redis://localhost:6379")
        if url:
            self.url = url
        self.rc = redis.from_url(url=self.url) # redis client

    def set_puzzle(self, date: str, puzzle: Puzzle) -> bool:
        return self.rc.hset("puzzle", key=date, value=puzzle.model_dump_json())

    def get_puzzle(self, date: str) -> Optional[Puzzle]:
        result = self.rc.hget(name="puzzle", key=date)
        if not result:
            return None
        return Puzzle.model_validate_json(result)

    def set_puzzles(self, puzzles: dict[str, Puzzle]) -> bool:
        for date, puzzle in puzzles.items():
            self.set_puzzle(date=date, puzzle=puzzle)

    def get_puzzles(self) -> dict[str, Puzzle]:
        result = self.rc.hgetall("puzzle")
        return {k.decode(): Puzzle.model_validate_json(v) for k, v in result.items()}

    def set_user_progress(self, userid: str, date: str, progress: UserProgress) -> bool:
        return self.rc.hset(f"user:{userid}:puzzle", key=date, value=progress.model_dump_json())

    def get_user_progress(self, userid: str, date: str) -> UserProgress:
        result: UserProgress = self.rc.hget(f"user:{userid}:puzzle", key=date)
        return UserProgress.model_validate_json(result) if result else UserProgress()
    
    def get_user_puzzles(self, userid: str) -> dict[str, UserProgress]:
        result = self.rc.hgetall(f"user:{userid}:puzzle")
        return {k.decode(): UserProgress.model_validate_json(v) for k, v in result.items()}
