#!/usr/bin/env python3

"""
URL Replacer Script
A utility script for replacing URLs and other text patterns in files
Usage: python url_replacer.py [options]
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_info(message):
    """Print info message with blue color"""
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")


def print_success(message):
    """Print success message with green color"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")


def print_warning(message):
    """Print warning message with yellow color"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def print_error(message):
    """Print error message with red color"""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")


def create_backup(file_path):
    """Create backup of file with timestamp"""
    if not os.path.isfile(file_path):
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{file_path}.backup.{timestamp}"
    
    try:
        shutil.copy2(file_path, backup_file)
        print_info(f"Backup created: {backup_file}")
    except Exception as e:
        print_error(f"Failed to create backup: {e}")
        sys.exit(1)


def replace_url(old_url, new_url, file_path, create_backup_flag=False):
    """Replace URLs in file"""
    if not os.path.isfile(file_path):
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    
    # Create backup if requested
    if create_backup_flag:
        create_backup(file_path)
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences before replacement
        count_before = content.count(old_url)
        
        if count_before == 0:
            print_warning(f"No occurrences of '{old_url}' found in {file_path}")
            return
        
        print_info(f"Found {count_before} occurrences of '{old_url}'")
        
        # Perform replacement
        new_content = content.replace(old_url, new_url)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Count occurrences after replacement
        count_after = new_content.count(new_url)
        
        print_success("Replacement completed!")
        print_info(f"Replaced {count_before} occurrences")
        print_info(f"Found {count_after} occurrences of new URL")
        
    except Exception as e:
        print_error(f"Error processing file: {e}")
        sys.exit(1)


def count_pattern(pattern, file_path):
    """Count occurrences of a pattern in file"""
    if not os.path.isfile(file_path):
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use regex for more flexible pattern matching
        matches = re.findall(re.escape(pattern), content)
        count = len(matches)
        
        print_info(f"Pattern '{pattern}' found {count} times in {file_path}")
        
    except Exception as e:
        print_error(f"Error reading file: {e}")
        sys.exit(1)


def verify_replacement(old_url, new_url, file_path):
    """Verify replacement results"""
    if not os.path.isfile(file_path):
        print_error(f"File not found: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        old_count = content.count(old_url)
        new_count = content.count(new_url)
        
        print_info("Verification Results:")
        print_info(f"Old URL '{old_url}': {old_count} occurrences")
        print_info(f"New URL '{new_url}': {new_count} occurrences")
        
        if old_count == 0 and new_count > 0:
            print_success("Replacement appears successful!")
        elif old_count > 0:
            print_warning("Some old URLs may still exist")
        else:
            print_warning("No URLs found")
            
    except Exception as e:
        print_error(f"Error reading file: {e}")
        sys.exit(1)


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description="URL Replacer Script - A utility for text replacement operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python url_replacer.py -r old_url new_url file.json
  python url_replacer.py -c 'pattern' file.txt
  python url_replacer.py -b -r old_url new_url file.json
  python url_replacer.py -v old_url new_url file.json
        """
    )
    
    # Operation arguments (mutually exclusive)
    operation_group = parser.add_mutually_exclusive_group(required=True)
    operation_group.add_argument('-r', '--replace-url', action='store_true',
                                help='Replace URLs in a file')
    operation_group.add_argument('-c', '--count', action='store_true',
                                help='Count occurrences of a pattern')
    operation_group.add_argument('-v', '--verify', action='store_true',
                                help='Verify replacement results')
    
    # Optional arguments
    parser.add_argument('-b', '--backup', action='store_true',
                       help='Create backup before replacement')
    
    # Positional arguments
    parser.add_argument('args', nargs='*', help='Arguments for the operation')
    
    args = parser.parse_args()
    
    # Execute based on operation
    if args.replace_url:
        if len(args.args) < 3:
            print_error("Replace operation requires: old_url new_url file")
            parser.print_help()
            sys.exit(1)
        replace_url(args.args[0], args.args[1], args.args[2], args.backup)
        
    elif args.count:
        if len(args.args) < 2:
            print_error("Count operation requires: pattern file")
            parser.print_help()
            sys.exit(1)
        count_pattern(args.args[0], args.args[1])
        
    elif args.verify:
        if len(args.args) < 3:
            print_error("Verify operation requires: old_url new_url file")
            parser.print_help()
            sys.exit(1)
        verify_replacement(args.args[0], args.args[1], args.args[2])


if __name__ == "__main__":
    main() 