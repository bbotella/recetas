#!/usr/bin/env python3
"""
Manual compilation script for Flask-Babel .mo files.
Used as fallback when pybabel is not available.
"""

import os
import struct
from pathlib import Path


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
        output.append(b"\x00")

    # Values
    for value in values:
        output.append(value.encode("utf-8"))
        output.append(b"\x00")

    # Write to file
    os.makedirs(os.path.dirname(mo_file_path), exist_ok=True)
    with open(mo_file_path, "wb") as f:
        for chunk in output:
            f.write(chunk)

    print(f"✅ Created .mo file with {len(translations)} translations")


def compile_all_translations():
    """Compile all translation files to .mo format."""
    translations_dir = Path("translations")
    compiled_count = 0

    for lang_dir in translations_dir.iterdir():
        if lang_dir.is_dir():
            po_file = lang_dir / "LC_MESSAGES" / "messages.po"
            mo_file = lang_dir / "LC_MESSAGES" / "messages.mo"

            if po_file.exists():
                try:
                    create_mo_file(str(po_file), str(mo_file))
                    compiled_count += 1
                except Exception as e:
                    print(f"❌ Error compiling {lang_dir.name}: {e}")

    return compiled_count


if __name__ == "__main__":
    print("Manual Translation Compiler")
    print("=" * 40)
    count = compile_all_translations()
    print(f"✅ Compiled {count} language files")
