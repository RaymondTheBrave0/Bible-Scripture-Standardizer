"""
bible_references.py - Module for standardizing Bible references with corrected parsing and validation.
"""

import re

BOOK_ABBREVIATIONS = {
    "Gen": "Genesis",
    "Ex": "Exodus",
    "Lev": "Leviticus",
    "Num": "Numbers",
    "Deut": "Deuteronomy",
    "Josh": "Joshua",
    "Judg": "Judges",
    "Ruth": "Ruth",
    "1 Sam": "1 Samuel",
    "2 Sam": "2 Samuel",
    "1 Kings": "1 Kings",
    "2 Kings": "2 Kings",
    "1 Chron": "1 Chronicles",
    "2 Chron": "2 Chronicles",
    "Ezra": "Ezra",
    "Neh": "Nehemiah",
    "Esth": "Esther",
    "Job": "Job",
    "Ps": "Psalms",
    "Prov": "Proverbs",
    "Eccl": "Ecclesiastes",
    "Song": "Song of Solomon",
    "Isa": "Isaiah",
    "Jer": "Jeremiah",
    "Lam": "Lamentations",
    "Ezek": "Ezekiel",
    "Dan": "Daniel",
    "Hos": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obad": "Obadiah",
    "Jonah": "Jonah",
    "Mic": "Micah",
    "Nah": "Nahum",
    "Hab": "Habakkuk",
    "Zeph": "Zephaniah",
    "Hag": "Haggai",
    "Zech": "Zechariah",
    "Mal": "Malachi",
    "Matt": "Matthew",
    "Mark": "Mark",
    "Luke": "Luke",
    "John": "John",
    "Acts": "Acts",
    "Rom": "Romans",
    "1 Cor": "1 Corinthians",
    "2 Cor": "2 Corinthians",
    "Gal": "Galatians",
    "Eph": "Ephesians",
    "Phil": "Philippians",
    "Col": "Colossians",
    "1 Thess": "1 Thessalonians",
    "2 Thess": "2 Thessalonians",
    "1 Tim": "1 Timothy",
    "2 Tim": "2 Timothy",
    "Titus": "Titus",
    "Philem": "Philemon",
    "Heb": "Hebrews",
    "James": "James",
    "1 Pet": "1 Peter",
    "2 Pet": "2 Peter",
    "1 John": "1 John",
    "2 John": "2 John",
    "3 John": "3 John",
    "Jude": "Jude",
    "Rev": "Revelation"
}

def standardize_reference(reference: str) -> str:
    """
    Standardizes all Bible references in a given text, preserving brackets or parentheses.
    Handles both ':' and '.' as separators between chapter and verse.
    Ensures a space is added before the reference if it is missing.
    """
    # Updated regex to handle grouped references and ensure proper spacing
    pattern = r'([\(\[\{]?)(\b[1-3]?\s?[A-Za-z]+)\.?(\s?\d+[:\.]\d+(-\d+)?)([\)\]\}]?)'

    def replace_match(match):
        opening_bracket = match.group(1)  # Capture opening bracket/parenthesis
        book_abbr = match.group(2).strip()  # Capture the book abbreviation
        verse = match.group(3).strip()  # Capture the chapter and verse
        closing_bracket = match.group(5)  # Capture closing bracket/parenthesis
        full_book_name = BOOK_ABBREVIATIONS.get(book_abbr, book_abbr)
        # Ensure a space before the reference and between the book name and the chapter/verse
        return f"{opening_bracket}{full_book_name} {verse}{closing_bracket}".strip()

    # Add a space before the reference if it is directly attached to the preceding word
    reference = re.sub(r'(\w)([\(\[\{]?[1-3]?\s?[A-Za-z]+\.\s?\d+[:\.]\d+(-\d+)?[\)\]\}]?)', r'\1 \2', reference)

    # Debugging: Log matches
    matches = re.findall(pattern, reference)
    print(f"Matches found: {matches}")

    return re.sub(pattern, replace_match, reference)

def process_text(text: str) -> str:
    """
    Processes a block of text to standardize all Bible references.
    """
    return standardize_reference(text)