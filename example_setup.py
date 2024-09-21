from dotenv import load_dotenv
from daily_puzzle_generation import generate_10_puzzles

load_dotenv(".env.production")

generate_10_puzzles()
