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
    
    # Pronunciation audio is stored as a base64 string to:
    # - Be able to store as json
    # - Be able to decode in the browser
    pronunciation_base64: str
    solution: str

class Letter(BaseModel):
    character: str
    color: str

# User progress of a puzzle
class UserProgress(BaseModel):
    guesses: list[list[Letter]] = []
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
