# Bible Reference Standardizer

A production-ready Python tool for standardizing Bible references in Word documents and text. This tool automatically converts various Bible reference formats to a consistent "Book Chapter:Verse" format (e.g., "John 3:16").

## Features

- **Comprehensive Format Support**: Handles multiple reference formats:
  - Standard: `John 3:16`, `John 3:16-18`, `John 3:16,18`
  - Period format: `John 3.16` → `John 3:16`
  - Space format: `John 3 16` → `John 3:16`
  - Chapter-verse format: `John chapter 3 verse 16` → `John 3:16`
  - Standalone chapters: `Psalm 23` → `Psalms 23:1`
  - Cross-chapter ranges: `John 3:16-4:2`

- **Extensive Abbreviation Support**: Uses CSV file with 77+ Bible books and 260+ abbreviations
- **Document Processing**: Works with Microsoft Word documents (.docx)
- **Backup Creation**: Automatically creates backups before making changes
- **Table Support**: Processes Bible references in tables as well as paragraphs
- **Production Ready**: Comprehensive error handling, logging, and testing

## Installation

### Requirements
- Python 3.6+
- python-docx library

### Setup
```bash
# Install required dependency
pip install python-docx

# Clone or download the repository
# Ensure you have these files:
# - standardize_bible_scripture_format.py
# - Bible-Books-Abbr.csv
# - cli.py (command-line interface)
```

## Usage

### Command Line Interface

The easiest way to use the tool is through the command-line interface:

#### Process a Word Document
```bash
# Basic usage - processes document and creates backup
python cli.py document.docx

# Specify output file
python cli.py document.docx -o processed_document.docx

# Skip backup creation
python cli.py document.docx --no-backup

# Verbose output with detailed information
python cli.py document.docx -v

# Dry run - see what would be processed without making changes
python cli.py document.docx --dry-run
```

#### Process Text Directly
```bash
# Process a text string
python cli.py --text "In jn 3:16 and gen 1.1, we see God's love."
```

### Python API

You can also use the tool programmatically:

```python
from standardize_bible_scripture_format import BibleReferenceStandardizer

# Initialize the standardizer
standardizer = BibleReferenceStandardizer()

# Process text
text = "Jesus said in jn 3:16 that God so loved the world."
result, changed = standardizer.process_text(text)
print(result)  # "Jesus said in John 3:16 that God so loved the world."

# Process a Word document
result = standardizer.process_document(
    'input.docx',
    'output.docx',
    create_backup=True
)

if result['success']:
    print(f"Processed {result['paragraphs_changed']} paragraphs")
else:
    print(f"Error: {result['error']}")
```

### Convenience Functions

```python
from standardize_bible_scripture_format import process_text, process_document

# Simple text processing
result, changed = process_text("In gen 1:1, God created...")

# Simple document processing
result = process_document('document.docx')
```

## Supported Bible Reference Formats

### Input Formats (automatically converted)
- `John 3:16` (already standard)
- `jn 3:16` (abbreviation)
- `John 3.16` (period separator)
- `John 3 16` (space separator)
- `John chapter 3 verse 16` (verbose format)
- `Psalm 23` (standalone chapter → `Psalms 23:1`)
- `John 3:16-18` (verse range)
- `John 3:16,18` (multiple verses)
- `John 3:16-4:2` (cross-chapter range)

### Output Format
All references are standardized to: `Book Chapter:Verse`
- Examples: `John 3:16`, `Genesis 1:1`, `1 Corinthians 13:4`

## Bible Books and Abbreviations

The tool supports all 66 books of the Protestant Bible plus additional books from Catholic and Orthodox traditions. Abbreviations are loaded from `Bible-Books-Abbr.csv` which includes:

### Old Testament Examples
- Genesis: `Gen`, `Ge`, `Gn`
- Exodus: `Exod`, `Ex`
- Psalms: `Ps`, `Pss` (plural)
- Isaiah: `Isa`, `Is`

### New Testament Examples
- Matthew: `Matt`, `Mat`, `Mt`
- John: `John`, `Jn`, `Jo`
- Romans: `Rom`, `Rm`, `Ro`
- 1 Corinthians: `1 Cor`, `1 Co`, `1C`
- Revelation: `Rev`, `Re`, `Rv`

## File Structure

```
Bible_Standardizer/
├── standardize_bible_scripture_format.py  # Main module
├── Bible-Books-Abbr.csv                   # Bible book abbreviations
├── cli.py                                 # Command-line interface
├── test_standardizer.py                   # Test suite
├── create_sample_doc.py                   # Sample document creator
├── README.md                              # This file
└── sample_bible_references.docx           # Sample test document
```

## Testing

Run the comprehensive test suite:

```bash
python test_standardizer.py
```

Create a sample document for testing:

```bash
python create_sample_doc.py
```

## Configuration

### Custom CSV File
You can provide a custom CSV file with Bible book abbreviations:

```bash
python cli.py document.docx --csv my_custom_books.csv
```

The CSV format should be:
```csv
Full Book Name,"Abbreviation1, Abbreviation2, Abbreviation3"
Genesis,"Gen, Ge, Gn"
Exodus,"Exod, Ex"
```

### Logging
The tool uses Python's logging module. You can adjust the logging level by modifying the logging configuration in the script.

## Error Handling

The tool includes comprehensive error handling:
- File not found errors
- Invalid document formats
- CSV parsing errors
- Backup creation failures
- Document processing errors

All errors are logged and returned in the result dictionary when using the API.

## Production Considerations

### Performance
- Processes documents efficiently using regex patterns
- Handles large documents with tables
- Minimal memory footprint

### Safety
- Always creates backups by default (can be disabled)
- Preserves original document formatting
- Non-destructive processing (original file remains unchanged when using output parameter)

### Reliability
- Comprehensive test suite
- Production-ready error handling
- Detailed logging for debugging

## Examples

### Example 1: Basic Document Processing
```bash
python cli.py sermon_notes.docx
# Creates: sermon_notes_backup_20231226_143022.docx
# Updates: sermon_notes.docx with standardized references
```

### Example 2: Batch Processing with Output Files
```bash
for file in *.docx; do
    python cli.py "$file" -o "standardized_$file"
done
```

### Example 3: Text Processing
```bash
python cli.py --text "Study gen 1:1, ps 23, and jn 3.16 today."
# Output: "Study Genesis 1:1, Psalms 23:1, and John 3:16 today."
```

## License

This tool is provided as-is for standardizing Bible references. Please ensure you have appropriate permissions before modifying documents.

## Support

For issues or questions:
1. Check the test suite for expected behavior
2. Review the CSV file for supported abbreviations
3. Use verbose mode (-v) for detailed processing information
4. Use dry-run mode to preview changes without modification
