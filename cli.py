#!/usr/bin/env python3
"""
Command-line interface for the Bible reference standardizer.

This script provides a user-friendly command-line interface for standardizing
Bible references in Word documents or text strings.
"""

import sys
import argparse
import os
import glob
import logging
from pathlib import Path
from standardize_bible_scripture_format import BibleReferenceStandardizer, process_any_file

def main():
    """Main entry point for the CLI."""
    
    parser = argparse.ArgumentParser(
        description="Standardize Bible references in Word documents or text",
        epilog="""
Examples:
  python cli.py document.docx                    # Process document (creates backup)
  python cli.py document.docx -o output.docx     # Process with specific output
  python cli.py --text "jn 3:16 and gen 1.1"    # Process text string
  python cli.py document.docx --no-backup        # Process without backup
  python cli.py document.docx --csv custom.csv   # Use custom CSV file
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main argument group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "path",
        nargs="?",
        help="Path to Word document or directory to process"
    )
    group.add_argument(
        "--text",
        help="Process a text string directly"
    )
    
    # Optional arguments
    parser.add_argument(
        "-o", "--output",
        help="Output path for processed document (if not specified, overwrites original)"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating backup of original document"
    )
    
    parser.add_argument(
        "--csv",
        help="Path to custom CSV file with Bible book abbreviations"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Display detailed processing information"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making actual changes"
    )
    
    args = parser.parse_args()
    
    try:
        # Set logging level based on verbose flag
        if args.verbose:
            logging.getLogger('standardize_bible_scripture_format').setLevel(logging.INFO)
            logging.getLogger('pdf_text_cleaner').setLevel(logging.INFO)
            print("Initializing Bible reference standardizer...")
        
        standardizer = BibleReferenceStandardizer(args.csv)
        
        if args.verbose:
            print(f"✓ Loaded {len(standardizer.bible_books)} Bible books")
            print(f"✓ Loaded {len(standardizer.book_variations)} book variations")
            print()
        
        # Process text string
        if args.text:
            result, changed = standardizer.process_text(args.text)
            
            print("Original text:")
            print(f"  {args.text}")
            print()
            print("Standardized text:")
            print(f"  {result}")
            print()
            
            if changed:
                print("✓ Changes were made to the text")
            else:
                print("ℹ No changes were needed")
            
            return 0
        
        # Process document or directory
        if args.path:
            path = Path(args.path)

            if not path.exists():
                print(f"✗ Error: Path not found: {path}")
                return 1

            # Handle directories
            if path.is_dir():
                # Get all files in the directory
                all_files = [f for f in os.listdir(args.path) if os.path.isfile(os.path.join(args.path, f))]
                
                # Separate supported and unsupported files
                supported_extensions = ['.docx', '.doc', '.html', '.htm', '.pdf', '.txt']
                supported_files = []
                unsupported_files = []
                
                for filename in all_files:
                    file_ext = os.path.splitext(filename)[1].lower()
                    full_path = os.path.join(args.path, filename)
                    
                    if file_ext in supported_extensions:
                        supported_files.append(full_path)
                    elif file_ext:  # Only warn about files with extensions
                        unsupported_files.append((full_path, file_ext))
                
                # Report on what was found
                if unsupported_files:
                    print(f"⚠ Found {len(unsupported_files)} unsupported file(s), will skip:")
                    for file_path, ext in unsupported_files:
                        filename = os.path.basename(file_path)
                        print(f"  - {filename} ({ext} - unsupported)")
                    print()
                
                if not supported_files:
                    print("✗ No supported files found in the directory.")
                    print("   Supported formats: .docx, .doc, .html, .htm, .pdf, .txt")
                    if unsupported_files:
                        print(f"   ({len(unsupported_files)} unsupported files were skipped)")
                    return 1

                print(f"Found {len(supported_files)} supported file(s) to process...")
                if args.verbose:
                    for file in supported_files:
                        file_ext = os.path.splitext(file)[1].lower()
                        print(f"  - {file} ({file_ext})")
                    print()
                
                files = supported_files

                for file in files:
                    document_path = Path(file)
                    print(f"Processing: {document_path}")
                    
                    # Optionally adjust output path for each document
                    output_path = args.output
                    if args.output:
                        output_path = os.path.join(args.output, document_path.name)

                    result = process_any_file(
                        str(document_path),
                        args.csv,
                        output_path,
                        not args.no_backup
                    )

                    if result['success']:
                        print(f"✓ {document_path} processed successfully")
                        if result.get('backup_path') and not args.no_backup:
                            print(f"✓ Backup created: {result['backup_path']}")

                        if result['changes_made']:
                            # Handle different result key names for different file types
                            if 'paragraphs_changed' in result:
                                print(f"✓ Changes made to {result['paragraphs_changed']} out of {result['paragraphs_processed']} paragraphs")
                            elif 'lines_changed' in result:
                                print(f"✓ Changes made to {result['lines_changed']} out of {result['lines_processed']} lines")
                            elif 'elements_changed' in result:
                                print(f"✓ Changes made to {result['elements_changed']} out of {result['elements_processed']} elements")
                            elif 'pages_changed' in result:
                                print(f"✓ Changes made to {result['pages_changed']} out of {result['pages_processed']} pages")
                            
                            # Special handling for PDF files
                            file_ext = os.path.splitext(document_path)[1].lower()
                            if file_ext == '.pdf':
                                if 'conversion_method' in result:
                                    print(f"✓ PDF converted to DOCX using {result['conversion_method']}")
                                print(f"✓ DOCX file saved to: {result['output_path']}")
                                print(f"✓ Original PDF backed up as: {result['backup_path']}")
                            else:
                                if output_path:
                                    print(f"✓ Output saved to: {output_path}")
                                else:
                                    print(f"✓ Original file updated: {document_path}")
                                
                            # Show any warnings
                            if 'warning' in result:
                                print(f"⚠ {result['warning']}")
                        else:
                            print("ℹ No Bible references found to standardize")

                        if args.verbose:
                            print(f"✓ Processing completed in {result['processing_time']:.2f} seconds")
                    else:
                        print(f"✗ Error processing {document_path}: {result['error']}")
                    print()  # Add spacing between files

            # Handle single files - auto-detect file type
            else:
                file_path = path
                file_ext = path.suffix.lower()
                
                # Check if file type is supported
                supported_extensions = ['.docx', '.doc', '.html', '.htm', '.pdf', '.txt']
                if file_ext not in supported_extensions:
                    print(f"✗ Warning: Unsupported file type '{file_ext}', skipping...")
                    return 0

                if args.dry_run:
                    print("DRY RUN MODE - No changes will be made")
                    print(f"File type detected: {file_ext}")
                    print()
                    return 0

                print(f"Processing: {file_path} (detected as {file_ext})")

                result = process_any_file(
                    str(file_path),
                    args.csv,
                    args.output,
                    not args.no_backup
                )

                if result['success']:
                    print(f"✓ {file_path} processed successfully")

                    if result.get('backup_path') and not args.no_backup:
                        print(f"✓ Backup created: {result['backup_path']}")

                    if result['changes_made']:
                        # Handle different result key names for different file types
                        if 'paragraphs_changed' in result:
                            print(f"✓ Changes made to {result['paragraphs_changed']} out of {result['paragraphs_processed']} paragraphs")
                        elif 'lines_changed' in result:
                            print(f"✓ Changes made to {result['lines_changed']} out of {result['lines_processed']} lines")
                        elif 'elements_changed' in result:
                            print(f"✓ Changes made to {result['elements_changed']} out of {result['elements_processed']} elements")
                        elif 'pages_changed' in result:
                            print(f"✓ Changes made to {result['pages_changed']} out of {result['pages_processed']} pages")
                        
                        # Special handling for PDF files
                        file_ext = path.suffix.lower()
                        if file_ext == '.pdf':
                            if 'conversion_method' in result:
                                print(f"✓ PDF converted to DOCX using {result['conversion_method']}")
                            print(f"✓ DOCX file saved to: {result['output_path']}")
                        else:
                            if args.output:
                                print(f"✓ Output saved to: {args.output}")
                            else:
                                print(f"✓ Original file updated: {file_path}")
                        
                        # Show any warnings
                        if 'warning' in result:
                            print(f"⚠ {result['warning']}")
                    else:
                        print("ℹ No Bible references found to standardize")

                    if args.verbose:
                        print(f"✓ Processing completed in {result['processing_time']:.2f} seconds")
                else:
                    print(f"✗ Error: {result['error']}")
                    return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n✗ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
