# main.py
from datetime import datetime, timedelta
from dotenv import load_dotenv
from kv_manager import KV, Puzzle

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

kv = KV()

def get_date_str(delta: int = 0) -> str:
    today = datetime.today()
    date = today + timedelta(days=delta)
    return date.strftime('%Y-%m-%d')

# Example usage
date1 = get_date_str()
date2 = get_date_str(1)
date3 = get_date_str(2)

puzzle1 = Puzzle(
    date=date1, 
    word_length=4,
    word_type="verb",
    synonym="tread",
    definition="to move along on foot : advance by steps",
    pronunciation="file_path",
    solution="walk"
)

puzzle2 = Puzzle(
    date=date2, 
    word_length=4,
    word_type="adjective",
    synonym="tranquil",
    definition="a period or condition of freedom from storms, high winds, or rough activity of water",
    pronunciation="file_path",
    solution="calm"
)

puzzle3 = Puzzle(
    date=date3, 
    word_length=4,
    word_type="noun",
    synonym="tiny",
    definition="an insignificant or tiny person",
    pronunciation="file_path",
    solution="peanut"
)

puzzles = {
    date1: puzzle1,
    date2: puzzle2,
    date3: puzzle3
}

# Set and get puzzle
kv.set_puzzles(puzzles=puzzles)

uid = "user_1"
uid2 = "user_2"

kv.guess(date2, uid, "calm")

print(kv.get_user_progress(uid, date1))
print(kv.get_user_puzzles(uid))
print(kv.get_puzzle(date3))
print(kv.get_user_stats(uid))