from pydantic import BaseModel

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
