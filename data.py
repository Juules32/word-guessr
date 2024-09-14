# data.py

from kv_manager import Puzzle
from date import get_date_str

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
