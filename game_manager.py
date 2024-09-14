# game_manager.py

from kv_manager import KeyValueManager
from model import Puzzle, UserProgress, State

# Constants
MAX_GUESSES = 6

class GameManager:
    def __init__(self, kv: KeyValueManager = KeyValueManager()):
        self.kv = kv
        
    def guess(self, date: str, userid: str, guess: str) -> bool:
        # Get existing data
        progress = self.kv.get_user_progress(userid, date)
        puzzle = self.kv.get_puzzle(date)
        solution = puzzle.solution

        if progress.won:
            raise Exception("You already won this puzzle!")
        
        if progress.completed:
            raise Exception("You already lost this puzzle!")

        # Determine new user data
        guesses = progress.guesses
        guesses.append(guess)
        completed = guess == solution or len(guesses) >= MAX_GUESSES
        won = guess == solution
        progress = UserProgress(guesses=guesses, completed=completed, won=won)

        # Set new user data
        return self.kv.set_user_progress(userid, date, progress)

    def get_user_stats(self, userid: str) -> dict:
        puzzle_data = self.kv.get_user_puzzles(userid)

        stats = {str(i): 0 for i in range(1, MAX_GUESSES + 1)}
        stats["More"] = 0

        for puzzle in puzzle_data.values():
            if not puzzle.completed:
                continue
            
            guesses = puzzle.guesses
            if len(guesses) <= MAX_GUESSES:
                stats[str(len(guesses))] += 1
            else:
                stats["More"] += 1
        
        return stats
    
    def get_state(self, date: str, userid: str) -> State:
        puzzle_data: Puzzle = self.kv.get_puzzle(date)

        if not puzzle_data:
            return "Error!"

        user_data = self.kv.get_user_progress(userid, date)

        if not user_data.completed:
            num_guesses = len(user_data.guesses)

            hint_priority = {
                "word_length": 0,
                "word_type": 2,
                "synonym": 3,
                "definition": 4,
                "pronunciation": 5,
                "solution": 6
            }

            # The hints to filter away (hide)
            hidden_hints = [k for k, v in hint_priority.items() if v > num_guesses]

            # Resets each hidden hint to its default value
            for hidden_hint in hidden_hints:
                # Default value is obtained by initializing the type class
                default_value = type(puzzle_data.__getattribute__(hidden_hint))()

                # Attribute is updated
                puzzle_data.__setattr__(hidden_hint, default_value)
        
        return State(puzzle=puzzle_data, user_progress=user_data)
