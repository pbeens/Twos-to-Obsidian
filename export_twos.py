"""
Twos to Obsidian
----------------
Splits a Twos app archive Markdown file into individual files for Obsidian.
Treats every Level 1 heading as a new file.
Skips entries that contain no content.

Usage:
    python export_twos.py --input path/to/archive.md --output path/to/export_dir
"""

import re
import os
import argparse

# Month mapping for date-based filename conversion
MONTHS = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}

def sanitize_filename(name, max_length=150):
    """Remove invalid filesystem characters and truncate if necessary."""
    # Remove invalid characters
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip()
    # Truncate to avoid path length issues, splitting on last space if possible
    if len(name) > max_length:
        name = name[:max_length].rsplit(' ', 1)[0]
    return name

def ensure_dir(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_filename_from_heading(line):
    """
    Parses a Level 1 heading to determine the output filename.
    Handles Twos' daily note format or falls back to the heading text.
    """
    # Daily Note pattern: # [emoji] [Day], YYYY [Month] [Day] ...
    # Examples:
    # # ⌛️ Wed, 2024 Feb 7 (24/8/15 6:27 am)
    # # Tue, 2026 Feb 24 (26/2/24 9:42 am)
    match = re.search(r'# (?:⌛️ )?\w+, (\d{4}) (\w{3}) (\d{1,2})', line)
    if match:
        year = match.group(1)
        month_name = match.group(2)
        day = match.group(3).zfill(2)
        month = MONTHS.get(month_name, '00')
        return f"{year}-{month}-{day}"
    
    # Otherwise, use the heading text itself
    heading_text = line.replace('# ', '', 1).strip()
    # Strip trailing date info like (25/4/29 10:40 am) if present
    heading_text = re.sub(r'\s*\(\d{2}/\d{1,2}/\d{1,2}.*?\)', '', heading_text)
    return sanitize_filename(heading_text)

def is_empty_content(part):
    """Checks if the content of a split part (excluding heading) is effectively empty."""
    lines = part.strip().split('\n')
    if len(lines) <= 1:
        return True
    # Join everything after the heading and check if it's just whitespace
    remaining_content = "".join(lines[1:]).strip()
    return not remaining_content

def process_archive(input_file, output_dir):
    """Main processing loop to split the archive."""
    ensure_dir(output_dir)
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by Level 1 headings using regex lookahead to keep the delimiter
    parts = re.split(r'^(?=# )', content, flags=re.MULTILINE)

    file_counts = {}
    created_count = 0
    skipped_count = 0

    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Check if entry has actual content besides the heading
        if is_empty_content(part):
            skipped_count += 1
            continue

        first_line = part.split('\n')[0]
        base_name = get_filename_from_heading(first_line)
        
        if not base_name:
            base_name = "Untitled"
            
        # Collision handling for duplicate headings
        if base_name in file_counts:
            file_counts[base_name] += 1
            filename = f"{base_name} ({file_counts[base_name]}).md"
        else:
            file_counts[base_name] = 1
            filename = f"{base_name}.md"
            
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as df:
            df.write(part)
        created_count += 1

    print(f"Export complete.")
    print(f"- Processed {len(parts)} potential entries.")
    print(f"- Created {created_count} files.")
    print(f"- Skipped {skipped_count} empty entries.")
    print(f"Files saved to: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twos to Obsidian: Export Twos Archive to individual Markdown files.")
    parser.add_argument("--input", help="Path to the Twos-YYYYMMDD.md archive file.")
    parser.add_argument("--output", help="Directory to save exported files (will be created if it doesn't exist).")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_dir = args.output
    
    # Interactive mode if arguments are missing
    if not input_file:
        input_file = input("Enter path to Twos archive file (e.g., Twos-20260224.md): ").strip()
        # Remove surrounding quotes if user pasted path with quotes
        input_file = input_file.strip("'\"")
        
    if not output_dir:
        output_dir = input("Enter directory to export to (will be created if it doesn't exist): ").strip()
        output_dir = output_dir.strip("'\"")
    
    if input_file and output_dir:
        process_archive(input_file, output_dir)
    else:
        print("Error: Both input file and output directory are required.")
