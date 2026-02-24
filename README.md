# Twos to Obsidian

A simple Python utility to split a large [Twos App](https://www.twosapp.com/) archive Markdown export into individual files, perfectly formatted for [Obsidian](https://obsidian.md/) or any other Markdown-based note-taking app.

## Features

- **Daily Log Extraction**: Automatically identifies date-based headings and names files as `YYYY-MM-DD.md`.
- **Standalone Note Support**: Splits all Level 1 headings into their own files.
- **Smart Cleanup**: Automatically skips headings that contain no actual content/notes.
- **OS Compatible**: Sanitizes and truncates filenames to prevent issues on Windows and other filesystems.
- **Interactive or CLI**: Use it as a simple interactive script or integrate it into a workflow via command-line arguments.

## Requirements

- Python 3.x (no external dependencies required).

## How to Export from TwosApp

To get your Twos archive, go to **Settings > Export > Download as markdown**.

## Usage

### Option 1: Interactive (Easiest)

Simply run the script and follow the prompts:

```bash
python export_twos.py
```

### Option 2: Command Line

Specify your input and output directly:

```bash
python export_twos.py --input "My-Twos-Archive.md" --output "./MyExport"
```

## How it Works

1. The script reads your Twos archive Markdown file.
2. it splits the file at every Level 1 heading (`#`).
3. If a heading follows the Twos daily log pattern, it's converted to a standard ISO date filename.
4. If it's a regular heading, the text is used as the filename (sanitized and truncated).
5. Empty entries are ignored to keep your vault clean.
6. Sub-headings, links, and S3 image URLs are preserved exactly as they appear.

## Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/pbeens/Twos-to-Obsidian/issues) page to report any bugs or suggest new features.

## License

Distributed under the MIT License. See `LICENSE` for more information.
