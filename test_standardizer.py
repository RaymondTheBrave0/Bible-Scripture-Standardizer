#!/usr/bin/env python3
"""
Test script for the Bible reference standardizer.

This script tests various Bible reference formats to ensure they are properly
standardized according to the CSV file mappings.
"""

import sys
import os
from standardize_bible_scripture_format import BibleReferenceStandardizer, process_text

def test_text_processing():
    """Test text processing with various Bible reference formats."""
    
    # Initialize the standardizer
    try:
        standardizer = BibleReferenceStandardizer()
        print(f"✓ Successfully loaded {len(standardizer.bible_books)} Bible books")
        print(f"✓ Loaded {len(standardizer.book_variations)} book variations")
        print()
    except Exception as e:
        print(f"✗ Error initializing standardizer: {e}")
        return False
    
    # Test cases with various formats
    test_cases = [
        # Standard formats
        ("John 3:16", "John 3:16"),
        ("jn 3:16", "John 3:16"),
        ("Mt 5:3-12", "Matthew 5:3-12"),
        ("matt 6:9", "Matthew 6:9"),
        
        # Period format
        ("John 3.16", "John 3:16"),
        ("Rom 8.28", "Romans 8:28"),
        
        # Space format
        ("John 3 16", "John 3:16"),
        ("Gen 1 1", "Genesis 1:1"),
        
        # Chapter-verse format
        ("John chapter 3 verse 16", "John 3:16"),
        ("Genesis chapter 1 verse 1", "Genesis 1:1"),
        
        # Standalone chapter references
        ("Psalm 23", "Psalms 23:1"),
        ("John 3", "John 3:1"),
        
        # Verse ranges
        ("John 3:16-18", "John 3:16-18"),
        ("Matt 5:3,5", "Matthew 5:3,5"),
        
        # Cross-chapter ranges
        ("John 3:16-4:2", "John 3:16-4:2"),
        
        # Multiple abbreviations
        ("1 Cor 13:4", "1 Corinthians 13:4"),
        ("2 Tim 3:16", "2 Timothy 3:16"),
        ("Rev 21:4", "Revelation 21:4"),
        
        # Different abbreviation styles from CSV
        ("Gen 1:1", "Genesis 1:1"),
        ("Ge 1:1", "Genesis 1:1"),
        ("Gn 1:1", "Genesis 1:1"),
        ("Exod 20:3", "Exodus 20:3"),
        ("Ex 20:3", "Exodus 20:3"),
        ("Ps 23:1", "Psalms 23:1"),
        ("Pss 23:1", "Psalms 23:1"),
    ]
    
    print("Testing Bible reference standardization:")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for input_text, expected_output in test_cases:
        try:
            result, changed = standardizer.process_text(input_text)
            
            if result.strip() == expected_output:
                print(f"✓ '{input_text}' → '{result}'")
                passed += 1
            else:
                print(f"✗ '{input_text}' → '{result}' (expected: '{expected_output}')")
                failed += 1
                
        except Exception as e:
            print(f"✗ Error processing '{input_text}': {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    return failed == 0

def test_complex_text():
    """Test processing of complex text with multiple references."""
    
    standardizer = BibleReferenceStandardizer()
    
    test_text = """
    In the beginning (Gen 1.1), God created the heavens and the earth. 
    Jesus said in jn 3:16 that God so loved the world. The Psalms tell us 
    in Ps 23 about the Lord being our shepherd. Paul writes in rom 8.28 
    that all things work together for good. In Matt 5:3-12, we find the 
    beatitudes, and 1 cor 13:4 describes love.
    """
    
    print("\nTesting complex text processing:")
    print("=" * 60)
    print("Original text:")
    print(test_text)
    
    result, changed = standardizer.process_text(test_text)
    
    print("\nProcessed text:")
    print(result)
    print(f"\nChanges made: {changed}")
    
    return True

def test_csv_loading():
    """Test that the CSV file is properly loaded."""
    
    print("\nTesting CSV file loading:")
    print("=" * 60)
    
    try:
        standardizer = BibleReferenceStandardizer()
        
        # Check some expected mappings
        expected_books = [
            ('genesis', 'Genesis'),
            ('gen', 'Genesis'),
            ('ge', 'Genesis'),
            ('gn', 'Genesis'),
            ('john', 'John'),
            ('jn', 'John'),
            ('psalms', 'Psalms'),
            ('ps', 'Psalms'),
            ('1 corinthians', '1 Corinthians'),
            ('1 cor', '1 Corinthians'),
        ]
        
        all_good = True
        for abbr, expected_name in expected_books:
            actual_name = standardizer.book_variations.get(abbr.lower())
            if actual_name == expected_name:
                print(f"✓ '{abbr}' → '{actual_name}'")
            else:
                print(f"✗ '{abbr}' → '{actual_name}' (expected: '{expected_name}')")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return False

def main():
    """Run all tests."""
    
    print("Bible Reference Standardizer Test Suite")
    print("=" * 60)
    
    # Test CSV loading
    if not test_csv_loading():
        print("✗ CSV loading tests failed")
        return 1
    
    # Test text processing
    if not test_text_processing():
        print("✗ Text processing tests failed")
        return 1
    
    # Test complex text
    if not test_complex_text():
        print("✗ Complex text tests failed")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ All tests passed! The standardizer is ready for production use.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
