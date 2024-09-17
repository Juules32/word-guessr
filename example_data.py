# data.py

from db.kv_manager import Puzzle
from util.date import get_date_str

# Example usage
date1 = get_date_str()
date2 = get_date_str(1)
date3 = get_date_str(2)
date4 = get_date_str(3)
date5 = get_date_str(4)

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

puzzle4 = Puzzle(
    date=date4,
    word_length=9,
    word_type="adjective",
    synonym="debatable",
    definition="subject to two or more interpretations and usually used to mislead or confuse",
    pronunciation="file_path",
    solution="equivocal"
)

puzzle5 = Puzzle(
    date=date5,
    word_length=10,
    word_type="noun",
    synonym="dishonesty",
    definition="lack of honesty or integrity : disposition to defraud or deceive",
    pronunciation="file_path",
    solution="dishonesty"
)

puzzles = {
    date1: puzzle1,
    date2: puzzle2,
    date3: puzzle3,
    date4: puzzle4,
    date5: puzzle5
}
