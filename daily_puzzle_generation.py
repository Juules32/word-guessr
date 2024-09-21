import random
from typing import Optional
import httpx
import re
from model.model import Puzzle
from util.date import get_date_str
import base64
from db.kv_manager import KeyValueManager

MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 14

def is_valid(word: str) -> bool:
    return len(word) >= MIN_WORD_LENGTH and len(word) <= MAX_WORD_LENGTH

def get_valid_words() -> str:
    with open("data/common_words.txt", "r") as word_file:
        word_list = word_file.read().split("\n")
        valid_words = filter(is_valid, word_list)
        return "\n".join(valid_words)

def write_valid_words() -> None:
    valid_words = get_valid_words()
    with open("data/common_words.txt", "w") as word_file:
        word_file.write(valid_words)

def get_random_word() -> str:
    with open("data/common_words.txt", "r") as word_file:
        return random.choice(word_file.read().split("\n"))

def fetch_audio_file(url: str) -> Optional[bytes]:
    try:
        r = httpx.get(url)
        if r.status_code == 200:
            return r.content # Return audio content as bytes
    except Exception as e:
        print(f"Error fetching audio: {e}")
    return None

def get_random_puzzle_data(date: str) -> Puzzle:
    word = get_random_word()
    if not word:
        print("Could not get random word, aborting...")
        return None
    
    print(f"Getting data for: {word}")

    r = httpx.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if r.status_code != 200:
        print("Improper response from dictionary api, aborting...")
        return None

    content: list[dict] = r.json()

    meaning: dict = content[0]["meanings"][0]
    if not meaning:
        print(f"{word.capitalize()} didn't have meaning, restarting...\n")
        return get_random_puzzle_data(date)
    
    word_type: str = meaning.get("partOfSpeech")
    if not word_type:
        print(f"{word.capitalize()} didn't have word type, restarting...\n")
        return get_random_puzzle_data(date)
    
    definitions: str = meaning.get("definitions")
    if not definitions:
        print(f"{word.capitalize()} didn't have definitions, restarting...\n")
        return get_random_puzzle_data(date)

    definition: str = definitions[0].get("definition")
    if not definition:
        print(f"{word.capitalize()} didn't have definition, restarting...\n")
        return get_random_puzzle_data(date)

    synonyms = meaning.get("synonyms")
    if not synonyms:
        print(f"{word.capitalize()} didn't have synonyms, restarting...\n")
        return get_random_puzzle_data(date)

    synonym = synonyms[0]

    phonetics: list[dict] = content[0].get("phonetics")
    if not phonetics:
        print(f"{word.capitalize()} didn't have phonetics, restarting...\n")
        return get_random_puzzle_data(date)

    pronunciation_url = phonetics[0].get("audio")
    if not pronunciation_url:
        print(f"{word.capitalize()} didn't have pronunciation url, restarting...\n")
        return get_random_puzzle_data(date)
    
    pronunciation_audio = fetch_audio_file(pronunciation_url)
    if not pronunciation_audio:
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
        word_type=word_type.capitalize(),
        synonym=synonym.capitalize(),
        definition=definition,
        pronunciation_base64=pronunciation_base64,
        solution=word.capitalize()
    )

    print(f"Success! Returning puzzle data for: {word}")
    return new_puzzle

kv = KeyValueManager()

def generate_tomorrows_puzzle() -> None:
    tomorrow = get_date_str(1)
    new_puzzle = get_random_puzzle_data(tomorrow)
    kv.set_puzzle(tomorrow, new_puzzle)

def generate_10_puzzles() -> None:
    for i in range(10):
        date = get_date_str(i)
        new_puzzle =  get_random_puzzle_data(date=date)
        kv.set_puzzle(date, new_puzzle)
