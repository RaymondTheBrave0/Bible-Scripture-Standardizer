#!/usr/bin/env python3
"""
simple_bible_standardizer.py - Simplified Bible reference standardizer

This approach:
1. Uses a simple regex to find potential Bible references
2. Looks up book names/abbreviations in the CSV file
3. Standardizes found references to "Book Chapter:Verse" format
4. Reports unmatched references so users can add them to the CSV

Much simpler than complex regex patterns!
"""

import os
import re
import csv
import logging
from typing import Dict, List, Tuple, Set
from docx import Document

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleBibleStandardizer:
    def __init__(self, csv_path: str = None):
        """Initialize with CSV file containing Bible book abbreviations."""
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(__file__), 'Bible-Books-Abbr.csv')
        
        self.book_mapping = {}  # Maps abbreviation -> full book name
        self.unmatched_references = set()  # Track references we couldn't match
        
        self._load_books_from_csv(csv_path)
        logger.info(f"Loaded {len(self.book_mapping)} book abbreviations from CSV")
    
    def _load_books_from_csv(self, csv_path: str):
        """Load book names and abbreviations from CSV file."""
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    book_name = row[0].strip()
                    abbreviations = row[1].strip().strip('"')
                    
                    # Add the full name as a key
                    self.book_mapping[book_name.lower()] = book_name
                    
                    # Parse abbreviations - they can be comma-separated
                    if abbreviations:
                        # Handle special format like "Ps (pl. Pss)"
                        if '(' in abbreviations:
                            # Extract base abbreviation
                            base = abbreviations.split('(')[0].strip()
                            if base:
                                for abbr in base.split(','):
                                    abbr = abbr.strip()
                                    if abbr:
                                        self.book_mapping[abbr.lower()] = book_name
                            
                            # Extract plural form if present
                            if 'pl.' in abbreviations:
                                plural_part = abbreviations[abbreviations.find('(')+1:abbreviations.find(')')]
                                plural_form = plural_part.replace('pl.', '').strip()
                                if plural_form:
                                    self.book_mapping[plural_form.lower()] = book_name
                        else:
                            # Normal comma-separated abbreviations
                            for abbr in abbreviations.split(','):
                                abbr = abbr.strip()
                                if abbr:
                                    self.book_mapping[abbr.lower()] = book_name
    
    def standardize_text(self, text: str) -> Tuple[str, bool, Set[str]]:
        """
        Standardize Bible references in text.
        
        Returns:
            (standardized_text, changes_made, unmatched_references)
        """
        original_text = text
        unmatched_in_text = set()
        
        # Create a pattern based on known book names/abbreviations
        # Sort by length (longest first) to match longer abbreviations first
        book_keys = sorted(self.book_mapping.keys(), key=len, reverse=True)
        book_keys_escaped = [re.escape(book) for book in book_keys]
        book_pattern = '|'.join(book_keys_escaped)
        
        # Pattern for chapter:verse references
        pattern = rf'\b({book_pattern})\.?\s+(\d+)[:\.](\d+)(?:-(\d+))?(?:\s*[,;]\s*(\d+)(?:-(\d+))?)*\b'
        
        def replace_reference(match):
            full_match = match.group(0)
            book_part = match.group(1).strip().lower()
            chapter = match.group(2)
            verse_start = match.group(3)
            verse_end = match.group(4) if match.group(4) else None
            
            # Look up the book name in our mapping
            if book_part in self.book_mapping:
                standard_book = self.book_mapping[book_part]
                
                # Build standardized reference
                result = f"{standard_book} {chapter}:{verse_start}"
                if verse_end:
                    result += f"-{verse_end}"
                
                return result
            else:
                # Book not found - track it for reporting
                unmatched_in_text.add(full_match)
                self.unmatched_references.add(full_match)
                return full_match  # Return unchanged
        
        # Apply the replacement
        new_text = re.sub(pattern, replace_reference, text, flags=re.IGNORECASE)
        
        # Also handle chapter-only references (like "Psalm 23" -> "Psalm 23:1")
        chapter_pattern = rf'\b({book_pattern})\.?\s+(\d+)(?!\s*[:.\d])\b'
        
        def replace_chapter_only(match):
            full_match = match.group(0)
            book_part = match.group(1).strip().lower()
            chapter = match.group(2)
            
            if book_part in self.book_mapping:
                standard_book = self.book_mapping[book_part]
                return f"{standard_book} {chapter}:1"
            else:
                # Might be a Bible reference we don't recognize
                unmatched_in_text.add(full_match)
                self.unmatched_references.add(full_match)
                return full_match
        
        new_text = re.sub(chapter_pattern, replace_chapter_only, new_text, flags=re.IGNORECASE)
        
        changes_made = new_text != original_text
        return new_text, changes_made, unmatched_in_text
    
    def process_document(self, doc_path: str) -> Dict:
        """Process a Word document and return results."""
        result = {
            'success': False,
            'changes_made': False,
            'paragraphs_changed': 0,
            'total_paragraphs': 0,
            'unmatched_references': set(),
            'error': None
        }
        
        try:
            doc = Document(doc_path)
            
            for paragraph in doc.paragraphs:
                result['total_paragraphs'] += 1
                original_text = paragraph.text
                
                if original_text.strip():
                    new_text, changed, unmatched = self.standardize_text(original_text)
                    if changed:
                        # Update the paragraph text while preserving formatting
                        for run in paragraph.runs:
                            run.text = ''
                        paragraph.runs[0].text = new_text if paragraph.runs else paragraph.text
                        if not paragraph.runs:
                            paragraph.text = new_text
                        
                        result['paragraphs_changed'] += 1
                        result['changes_made'] = True
                    
                    result['unmatched_references'].update(unmatched)
            
            # Save the document
            doc.save(doc_path)
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error processing document: {e}")
        
        return result
    
    def get_unmatched_report(self) -> str:
        """Get a report of all unmatched references found."""
        if not self.unmatched_references:
            return "No unmatched Bible references found."
        
        report = "Unmatched Bible References Found:\n"
        report += "=" * 40 + "\n"
        for ref in sorted(self.unmatched_references):
            report += f"  {ref}\n"
        report += "\nThese references were not standardized because the book name/abbreviation\n"
        report += "was not found in the CSV file. You can either:\n"
        report += "1. Edit these references manually in your document, or\n"
        report += "2. Add the abbreviation to your Bible-Books-Abbr.csv file\n"
        return report


def main():
    """Example usage"""
    standardizer = SimpleBibleStandardizer()
    
    # Test with some text
    test_text = "Read Heb. 11:7 and compare with Gen 6:13. Also see 1 Cor. 5:7 and Xyz. 1:1"
    
    result, changed, unmatched = standardizer.standardize_text(test_text)
    
    print("Original:", test_text)
    print("Result:", result)
    print("Changed:", changed)
    print("Unmatched:", unmatched)
    print()
    print(standardizer.get_unmatched_report())


if __name__ == "__main__":
    main()
