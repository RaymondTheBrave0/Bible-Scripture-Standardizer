# Multi-Format Bible Reference Standardizer

## ✅ **PRODUCTION-READY SYSTEM**

Your Bible Reference Standardizer now automatically detects and processes multiple file formats without any manual specification needed!

## **Supported File Formats**

### **Fully Supported Formats:**
- **`.docx`** - Microsoft Word (2007+) - Full formatting preservation
- **`.txt`** - Plain text files - Line-by-line processing
- **`.html`, `.htm`** - HTML web pages - Preserves HTML structure
- **`.doc`** - Legacy Word documents - Extracts text (saves as .txt)
- **`.pdf`** - PDF documents - Extracts text (saves as .txt)

## **Key Features**

### **🔍 Automatic File Type Detection**
- No need to specify file format
- System automatically detects based on file extension
- Graceful error handling for unsupported formats

### **📁 Directory Processing**
- Process entire directories with mixed file types
- Automatically finds and processes all supported files
- Batch processing with individual progress reporting

### **🔄 Format-Specific Processing**
- **DOCX**: Full document processing with formatting preservation
- **TXT**: Line-by-line text processing
- **HTML**: Element-wise processing while preserving HTML structure  
- **DOC**: Text extraction with processed output saved as `.txt`
- **PDF**: Text extraction with processed output saved as `.txt`

### **🛡️ Safety Features**
- Automatic backup creation for all file types
- Timestamped backups prevent overwriting
- Dry-run mode to preview changes
- Comprehensive error handling

## **Usage Examples**

### **Single File Processing (Auto-Detection)**
```bash
# Process any supported file type
python cli.py document.docx     # Word document
python cli.py notes.txt         # Text file
python cli.py webpage.html      # HTML file
python cli.py legacy.doc        # Legacy Word document
python cli.py research.pdf      # PDF document
```

### **Directory Processing (Mixed File Types)**
```bash
# Process all supported files in a directory
python cli.py /path/to/documents/

# With verbose output
python cli.py /path/to/documents/ -v

# Skip backup creation
python cli.py /path/to/documents/ --no-backup
```

### **Advanced Options**
```bash
# Dry run to preview changes
python cli.py document.docx --dry-run

# Use custom CSV file
python cli.py document.docx --csv custom-books.csv

# Specify output location
python cli.py document.docx -o processed-document.docx
```

## **Processing Results by File Type**

### **DOCX Files**
- **Input**: Microsoft Word document
- **Output**: Processed Word document (same format)
- **Preserves**: All formatting, styles, tables, images
- **Metrics**: Paragraphs processed/changed

### **TXT Files**
- **Input**: Plain text file
- **Output**: Processed text file (same format)
- **Preserves**: Text structure and line breaks
- **Metrics**: Lines processed/changed

### **HTML Files**
- **Input**: HTML web page
- **Output**: Processed HTML file (same format)
- **Preserves**: HTML structure, tags, attributes
- **Metrics**: Text elements processed/changed

### **DOC Files (Legacy)**
- **Input**: Legacy Word document (.doc)
- **Output**: Processed text file (.txt)
- **Note**: Formatting cannot be preserved due to format limitations
- **Metrics**: Content blocks processed/changed

### **PDF Files**
- **Input**: PDF document
- **Output**: Processed text file (.txt)
- **Note**: Text-only extraction, formatting not preserved
- **Metrics**: Pages processed/changed

## **Installation Requirements**

### **Core Package (Required)**
```bash
pip install python-docx
```

### **Additional Format Support**
```bash
# For all format support
pip install beautifulsoup4 PyPDF2 docx2txt

# Or install all at once
pip install -r requirements.txt
```

## **Example Test Run**

```bash
# Create test files
python create_multi_format_tests.py

# Process entire directory with auto-detection
python cli.py multi_format_tests/ -v
```

**Sample Output:**
```
Found 4 supported file(s) to process...
  - bible_study.docx (.docx)
  - bible_study.html (.html)
  - bible_study.txt (.txt)
  - sermon_notes.txt (.txt)

Processing: bible_study.docx (detected as .docx)
✓ Changes made to 9 out of 12 paragraphs
✓ Backup created: bible_study_backup_20231226_143022.docx

Processing: bible_study.html (detected as .html)
✓ Changes made to 9 out of 38 elements
✓ Backup created: bible_study_backup_20231226_143022.html

Processing: bible_study.txt (detected as .txt)
✓ Changes made to 9 out of 16 lines
✓ Backup created: bible_study_backup_20231226_143022.txt
```

## **Bible Reference Transformations**

All file types process the same reference formats:

### **Input Formats → Standardized Output**
- `gen 1.1` → `Genesis 1:1`
- `jn 3:16` → `John 3:16`
- `ps 23` → `Psalms 23:1`
- `1 cor 13:4-8` → `1 Corinthians 13:4-8`
- `rom 8.28` → `Romans 8:28`
- `matt 5:3-12` → `Matthew 5:3-12`
- `isa chapter 53 verse 5` → `Isaiah 53:5`
- `heb 11 1` → `Hebrews 11:1`

## **Error Handling**

### **Unsupported File Types**
```bash
$ python cli.py document.xyz
✗ Error: Unsupported file type '.xyz'
   Supported formats: .docx, .doc, .html, .htm, .pdf, .txt
```

### **Missing Dependencies**
```bash
$ python cli.py document.pdf
✗ Error: PyPDF2 not installed. Install with: pip install PyPDF2
```

### **File Not Found**
```bash
$ python cli.py nonexistent.txt
✗ Error: Path not found: nonexistent.txt
```

## **Production Deployment**

### **For Individual Use**
```bash
# Simple processing
python cli.py /path/to/documents/

# Regular backup and processing
python cli.py /home/user/Documents/Bible_Studies/ -v
```

### **For Batch Processing**
```bash
# Process multiple directories
for dir in /path/to/*/documents; do
    python cli.py "$dir" -v
done
```

### **For Server Deployment**
```bash
# Install system-wide
sudo pip install python-docx beautifulsoup4 PyPDF2 docx2txt

# Create processing script
python cli.py /var/documents/ --no-backup -v
```

## **CSV Customization**

The system uses `Bible-Books-Abbr.csv` for book mappings. You can:

1. **Add new books**: Add rows to the CSV
2. **Add abbreviations**: Extend the abbreviation lists  
3. **Use custom CSV**: `--csv custom-books.csv`

**CSV Format:**
```csv
Genesis,"Gen, Ge, Gn"
Exodus,"Exod, Ex"
```

## **Summary**

✅ **Auto-detects** all supported file types  
✅ **Processes directories** with mixed formats  
✅ **Creates backups** automatically  
✅ **Preserves formatting** when possible  
✅ **Handles errors** gracefully  
✅ **Production ready** with comprehensive logging  

Your Bible Reference Standardizer is now a complete, multi-format processing system that requires **no manual file type specification** and can handle any combination of supported documents!
