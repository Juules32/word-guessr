# main.py

from kv_manager import KV

kv = KV()

# Example usage
date = "2024-09-15"
date2 = "2024-09-17"
date3 = "2024-09-18"
puzzle_data = {
    "date": "...",
    "length of word": 6,
    "word type": "noun",
    "synonym(s)": "synonym",
    "definition": "definition",
    "pronunciation": "file_path",
    "solution": "solution_word"
}

# Set and get puzzle
kv.set_puzzle(date, puzzle_data)
kv.set_puzzle(date2, puzzle_data)
kv.set_puzzle(date3, puzzle_data)

uid = "user_1"
uid2 = "user_2"

kv.guess(date2, uid, "bad_word")
print(kv.get_user_progress(uid, date2))
print(kv.get_user_puzzles(uid))
print(kv.get_puzzles()["2024-09-18"])