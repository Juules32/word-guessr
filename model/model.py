from pydantic import BaseModel

# Constants
MAX_GUESSES = 6

# Unique information of a daily puzzle
class Puzzle(BaseModel):
    date: str
    word_length: int
    word_type: str
    synonym: str
    definition: str
    pronunciation: str # Should be file
    solution: str

# User progress of a puzzle
class UserProgress(BaseModel):
    guesses: list[str] = []
    completed: bool = False
    won: bool = False

class State(BaseModel):
    puzzle: Puzzle
    user_progress: UserProgress

class PuzzleListItem(BaseModel):
    date: str
    num_guesses: int = 0
    completed: bool = False
    won: bool = False
