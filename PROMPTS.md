# Twos to Obsidian Prompts

## Objective

Export a large Twos app archive into individual Markdown files compatible with Obsidian.

## Core Rules

1. **Split Logic**: Split the archive by every Level 1 heading (`#`).
2. **Skip Logic**: **Ignore** any entry that contains no content (excluding the heading and whitespace).
3. **Naming**:
   - Date headings (`# ⌛️ Wed, 2024 Feb 7 ...`) -> `YYYY-MM-DD.md`.
   - Standalone headings (`# Note Title`) -> `Note Title.md`.
4. **Safety**:
   - Sanitize filenames (remove `\/*?:"<>|`).
   - Truncate filenames to 150 characters to avoid Windows path length errors.
   - Handle duplicates by automatically appending `(n)`.
5. **Preservation**: Keep all Markdown formatting, S3 image links, and to-do lists exactly as they are.

## Implementation Details

The utility [export_twos.py](file:///d:/My%20Documents/TwosApp%20backup/Twos-20260224/export_twos.py) is a generalized CLI tool.

### Usage

- **CLI**: `python export_twos.py --input <archive.md> --output <export_dir>`
- **Interactive**: Just run `python export_twos.py` and follow the prompts.

> [!NOTE]
> The export directory will be automatically created if it does not already exist.
