#!/usr/bin/env python3
"""
Script to create Basque .mo compiled translation files manually.
"""

import os
import struct


def create_mo_file(po_file_path, mo_file_path):
    """
    Create a .mo file from a .po file content.
    This is a simplified version that works with our AI translations.
    """
    print(f"Creating .mo file: {mo_file_path}")

    # Read the .po file
    with open(po_file_path, "r", encoding="utf-8") as f:
        po_content = f.read()

    # Parse translations
    translations = {}
    current_msgid = None
    current_msgstr = None

    for line in po_content.split("\n"):
        line = line.strip()
        if line.startswith('msgid "') and line.endswith('"'):
            current_msgid = line[7:-1]  # Remove 'msgid "' and '"'
        elif line.startswith('msgstr "') and line.endswith('"'):
            current_msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
            if current_msgid and current_msgstr:
                translations[current_msgid] = current_msgstr
                current_msgid = None
                current_msgstr = None

    # Create .mo file structure
    keys = sorted(translations.keys())
    values = [translations[k] for k in keys]

    # Calculate offsets
    key_offsets = []
    value_offsets = []
    output = []

    # Start after header
    offset = 7 * 4 + 16 * len(keys)

    for key in keys:
        key_offsets.append((len(key.encode("utf-8")), offset))
        offset += len(key.encode("utf-8")) + 1

    for value in values:
        value_offsets.append((len(value.encode("utf-8")), offset))
        offset += len(value.encode("utf-8")) + 1

    # Create the .mo file
    output = []
    output.append(struct.pack("<I", 0x950412DE))  # Magic number
    output.append(struct.pack("<I", 0))  # Version
    output.append(struct.pack("<I", len(keys)))  # Number of entries
    output.append(struct.pack("<I", 7 * 4))  # Offset of key table
    output.append(struct.pack("<I", 7 * 4 + 8 * len(keys)))  # Offset of value table
    output.append(struct.pack("<I", 0))  # Hash table size
    output.append(struct.pack("<I", 0))  # Hash table offset

    # Key table
    for length, offset in key_offsets:
        output.append(struct.pack("<I", length))
        output.append(struct.pack("<I", offset))

    # Value table
    for length, offset in value_offsets:
        output.append(struct.pack("<I", length))
        output.append(struct.pack("<I", offset))

    # Keys
    for key in keys:
        output.append(key.encode("utf-8"))
        output.append(b"\\0")

    # Values
    for value in values:
        output.append(value.encode("utf-8"))
        output.append(b"\\0")

    # Write to file
    os.makedirs(os.path.dirname(mo_file_path), exist_ok=True)
    with open(mo_file_path, "wb") as f:
        for chunk in output:
            f.write(chunk)

    print(f"✅ Created .mo file with {len(translations)} translations")


def main():
    """
    Main function to create .mo files for Basque.
    """
    print("Creating Basque .mo compilation files...")

    po_file = "translations/eu/LC_MESSAGES/messages.po"
    mo_file = "translations/eu/LC_MESSAGES/messages.mo"

    if os.path.exists(po_file):
        create_mo_file(po_file, mo_file)
        print("✅ Basque translations compiled successfully!")
    else:
        print("❌ .po file not found")


if __name__ == "__main__":
    main()
