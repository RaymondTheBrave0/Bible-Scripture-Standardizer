# Bible Reference Standardizer - Setup Guide

## System Requirements

### Python Version
- **Python 3.6 or higher** (recommended: Python 3.8+)

### Operating Systems
- ✅ **Linux** (Ubuntu, CentOS, RHEL, etc.)
- ✅ **Windows** (10, 11)
- ✅ **macOS** (10.14+)

## Required Packages

### Essential Package (Must Install)
```bash
pip install python-docx
```

### Standard Library Modules (Usually Included)
The following modules are part of Python's standard library and should be available by default:
- `os` - File and directory operations
- `re` - Regular expressions
- `csv` - CSV file reading
- `logging` - Logging functionality
- `shutil` - File copying/moving
- `datetime` - Date and time handling
- `sys` - System-specific parameters
- `argparse` - Command-line argument parsing
- `glob` - Filename pattern matching
- `pathlib` - Object-oriented filesystem paths
- `typing` - Type hints (Python 3.5+)

### Optional (for older Python versions)
If you're using Python < 3.8, you might need:
```bash
pip install typing-extensions
```

## Installation Methods

### Method 1: Using pip (Recommended)
```bash
# Install the main dependency
pip install python-docx

# Or install from requirements file
pip install -r requirements.txt
```

### Method 2: Using conda
```bash
conda install python-docx
```

### Method 3: Using system package manager (Linux)

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install python-docx
```

#### CentOS/RHEL:
```bash
sudo yum install python3-pip
# or for newer versions:
sudo dnf install python3-pip
pip3 install python-docx
```

## Verification

### Check Python Version
```bash
python --version
# or
python3 --version
```

### Check if python-docx is installed
```bash
python -c "import docx; print('python-docx is installed successfully')"
```

### Run the test suite
```bash
python test_standardizer.py
```

## Complete Setup Steps

### 1. Download/Clone the Project
Ensure you have these files in your project directory:
```
Bible_Standardizer/
├── standardize_bible_scripture_format.py  # Main module
├── Bible-Books-Abbr.csv                   # Bible book abbreviations
├── cli.py                                 # Command-line interface
├── test_standardizer.py                   # Test suite
├── requirements.txt                       # Dependencies
├── README.md                              # Documentation
└── SETUP.md                               # This file
```

### 2. Install Dependencies
```bash
cd Bible_Standardizer
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
# Run tests
python test_standardizer.py

# Test CLI
python cli.py --help

# Test text processing
python cli.py --text "In jn 3:16, God showed his love"
```

### 4. Create Test Documents (Optional)
```bash
python create_sample_doc.py
python cli.py sample_bible_references.docx --dry-run
```

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'docx'"
**Solution:**
```bash
pip install python-docx
# Note: It's 'python-docx' not 'docx'
```

#### Issue: "Permission denied" when installing packages
**Solution (Linux/Mac):**
```bash
# Use --user flag
pip install --user python-docx

# Or use sudo (not recommended for regular use)
sudo pip install python-docx

# Or use virtual environment (recommended)
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
# or
myenv\Scripts\activate     # Windows
pip install python-docx
```

#### Issue: "python: command not found"
**Solution:**
```bash
# Try python3 instead
python3 cli.py --help

# Or create an alias
alias python=python3
```

#### Issue: CSV file not found
**Solution:**
- Ensure `Bible-Books-Abbr.csv` is in the same directory as the Python scripts
- Or specify a custom path: `python cli.py document.docx --csv /path/to/your/csv`

#### Issue: "TypeError" related to typing
**Solution (for Python < 3.8):**
```bash
pip install typing-extensions
```

### Virtual Environment Setup (Recommended for Development)

#### Create Virtual Environment:
```bash
# Create virtual environment
python -m venv bible_standardizer_env

# Activate it
# On Linux/Mac:
source bible_standardizer_env/bin/activate
# On Windows:
bible_standardizer_env\Scripts\activate

# Install dependencies
pip install python-docx

# When done, deactivate
deactivate
```

## Package Details

### python-docx
- **Purpose**: Reading and writing Microsoft Word documents (.docx)
- **Version**: 1.2.0 or higher
- **Dependencies**: It automatically installs `lxml` (XML processing)
- **Size**: ~250KB (plus dependencies)

### Dependencies of python-docx:
- `lxml` - XML processing library (~5MB)
- `typing-extensions` - Type hints for older Python versions

## Deployment Notes

### For Production Servers:
```bash
# Install system-wide (as root/administrator)
sudo pip install python-docx

# Or use package manager (Ubuntu/Debian)
sudo apt install python3-python-docx
```

### For Containerized Deployments (Docker):
```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "cli.py"]
```

## Testing Your Installation

### Quick Test:
```bash
# Test import
python -c "from standardize_bible_scripture_format import BibleReferenceStandardizer; print('✅ Installation successful')"

# Test basic functionality
python cli.py --text "Test with jn 3:16 and gen 1:1"
```

### Full Test Suite:
```bash
python test_standardizer.py
# Should show: "✅ All tests passed! The standardizer is ready for production use."
```

## Support

If you encounter issues:
1. Check that Python 3.6+ is installed
2. Verify python-docx is installed: `pip list | grep python-docx`
3. Run the test suite to identify specific problems
4. Check file permissions and paths
5. Try using a virtual environment to isolate dependencies
