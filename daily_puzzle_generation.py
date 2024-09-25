import os
import random
import string
from typing import Optional
from dotenv import load_dotenv
import httpx
import re
from model.model import Puzzle
from util.date import get_date_str
import base64
from db.kv_manager import KeyValueManager

load_dotenv()

MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 14

def get_valid_words(file_name: str) -> str:
    def is_valid(word: str) -> bool:
        return len(word) >= MIN_WORD_LENGTH and len(word) <= MAX_WORD_LENGTH

    with open(f"data/{file_name}", "r") as word_file:
        word_list = word_file.read().split("\n")
        valid_words = filter(is_valid, word_list)
        return "\n".join(valid_words)

def write_valid_words(file_name: str) -> None:
    valid_words = get_valid_words(file_name)
    with open(f"data/{file_name}", "w") as word_file:
        word_file.write(valid_words)

def get_random_word(file_name: str) -> str:
    with open(f"data/{file_name}", "r") as word_file:
        return random.choice(word_file.read().split("\n"))

def fetch_audio_file(url: str) -> Optional[bytes]:
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            return response.content # Return audio content as bytes
    except Exception as e:
        print(f"Error fetching audio: {e}")
    return None

def get_random_puzzle_data(date: str, is_school: bool = False) -> Puzzle:
    word = get_random_word("all_words.txt")
    if not word:
        print("Could not get random word, aborting...")
        return None
    
    print(f"Getting data for: {word}")

    if is_school:
        response = httpx.get(f"https://dictionaryapi.com/api/v3/references/sd4/json/{word}", params={"key": os.getenv("SCHOOL_DICT_KEY")})
    else:
        response = httpx.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}", params={"key": os.getenv("DICT_KEY")})
    
    if response.status_code == 404:
        print(f"{word} not found in dictionary, restarting...\n")
        return get_random_puzzle_data(date, is_school)

    if response.status_code != 200:
        print("Improper response from dictionary api, aborting...")
        return None

    content: list[dict] = response.json()[0]

    try:
        word_type: str = content["fl"]
    except:
        print(f"{word} didn't have word type, restarting...\n")
        return get_random_puzzle_data(date, is_school)
    
    try:
        definition: str = content["shortdef"][0]
    except:
        print(f"{word} didn't have definition, restarting...\n")
        return get_random_puzzle_data(date, is_school)

    try:
        synonym: str = content["syns"][0]["pt"][0][1]

        # All synonyms, which are in {sc} tags in merriam-webster's api, are found
        merriam_synonyms: list[str] = re.findall(r'\{sc\}(.*?)\{/sc\}', synonym)

        # Note: set comprehension is used to eliminate duplicates
        unique_synonyms = {synonym.capitalize() for synonym in merriam_synonyms}
        synonym = ', '.join(unique_synonyms)
    except:
        synonym = "None"

    try:
        pronunciation_str: str = content["hwi"]["prs"][0]["sound"]["audio"]
    except:
        print(f"{word} didn't have pronunciation data, restarting...\n")
        return get_random_puzzle_data(date, is_school)
    
    if pronunciation_str.startswith("bix"):
        subdirectory = "bix"
    elif pronunciation_str.startswith("gg"):
        subdirectory = "gg"
    elif pronunciation_str[0].isdigit() or pronunciation_str[0] in string.punctuation:
        subdirectory = "number"
    else:
        subdirectory = pronunciation_str[0]

    pronunciation_url = f"https://media.merriam-webster.com/audio/prons/en/us/mp3/{subdirectory}/{pronunciation_str}.mp3"

    try:
        pronunciation_audio = fetch_audio_file(pronunciation_url)
    except:
        print(f"Failed to fetch audio for {word}, aborting...")
        return None

    pronunciation_base64 = base64.b64encode(pronunciation_audio).decode('utf-8')
    
    # Hides instances of the solution
    insensitive_instance = re.compile(re.escape(word), re.IGNORECASE)
    synonym = insensitive_instance.sub("_" * len(word), synonym)
    definition = insensitive_instance.sub("_" * len(word), definition)

    new_puzzle = Puzzle(
        date=date,
        word_length=len(word),
        word_type=capitalize_first_letter(word_type),
        synonym=capitalize_first_letter(synonym),
        definition=capitalize_first_letter(definition),
        pronunciation_base64=pronunciation_base64,
        solution=word.capitalize()
    )

    print(f"Success! Returning puzzle data for: {word}\n")
    return new_puzzle

def capitalize_first_letter(input: str) -> str:
    return input[0].upper() + input[1:]

def generate_tomorrows_puzzle() -> None:
    kv = KeyValueManager()
    tomorrow = get_date_str(1)
    new_puzzle = get_random_puzzle_data(date=tomorrow)
    if new_puzzle:
        kv.set_puzzle(tomorrow, new_puzzle)

def generate_10_puzzles() -> None:
    kv = KeyValueManager()
    for i in range(10):
        date = get_date_str(-i)
        new_puzzle =  get_random_puzzle_data(date=date)
        if new_puzzle:
            kv.set_puzzle(date, new_puzzle)
