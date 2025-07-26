#!/usr/bin/env python3
"""
Script to automatically split long lines in Python files to conform to linting standards.
"""

import os
import re

def split_long_line(line, max_length=120):
    """Split a long line into multiple lines."""
    if len(line) <= max_length:
        return [line]
    
    # Check if this is a dictionary entry with a long string
    dict_match = re.match(r'(\s*\d+:\s*)"([^"]+)"(.*)', line)
    if dict_match:
        indent = dict_match.group(1)
        content = dict_match.group(2)
        suffix = dict_match.group(3)
        
        # Split the content into chunks
        words = content.split(' ')
        chunks = []
        current_chunk = ""
        
        for word in words:
            if len(current_chunk + word + " ") <= max_length - 20:  # Leave room for quotes and formatting
                current_chunk += word + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = word + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Format as multi-line string
        lines = [f"{indent}("]
        for i, chunk in enumerate(chunks):
            if i == len(chunks) - 1:
                lines.append(f'        "{chunk}"')
            else:
                lines.append(f'        "{chunk} "')
        lines.append(f"    ){suffix}")
        
        return lines
    
    return [line]

def process_file(filepath):
    """Process a single file to split long lines."""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    
    for line in lines:
        if len(line.rstrip()) > 120:
            split_lines = split_long_line(line.rstrip())
            new_lines.extend([l + '\n' for l in split_lines])
            if len(split_lines) > 1:
                modified = True
        else:
            new_lines.append(line)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"  ✅ Modified {filepath}")
    else:
        print(f"  ⏭️  No changes needed for {filepath}")

def main():
    """Main function to process all Python files."""
    # Files with translation content that need line splitting
    translation_files = [
        "update_translations.py",
        "update_descriptions.py", 
        "update_all_remaining_descriptions.py",
        "update_remaining_descriptions.py",
        "add_all_valencian_translations.py",
        "add_valencian_translations_part1.py"
    ]
    
    for filename in translation_files:
        if os.path.exists(filename):
            process_file(filename)
        else:
            print(f"⚠️  File not found: {filename}")

if __name__ == "__main__":
    main()