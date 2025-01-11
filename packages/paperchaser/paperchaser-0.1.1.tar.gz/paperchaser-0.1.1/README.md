# PaperChaser

A Python tool for extracting and downloading academic paper references. Supports both single and two-column PDF formats.

## Features

- Extract references from PDF files with support for:
  - Single and two-column layouts
  - Multiple reference formats (numbered, bracketed, author-year)
  - Smart reference section detection
- Download papers using:
  - DOI lookup
  - Title-based search
  - Multiple sources (Sci-Hub, PubMed Central, arXiv, etc.)
- Automatic PDF renaming with metadata
- Beautiful command-line interface with:
  - Progress bars
  - Colored status indicators
  - Formatted tables
  - Detailed error reporting

## Installation

```bash
pip install paperchaser
```

## Usage

Basic usage:
```bash
# Extract and download references from a PDF
paperchaser path/to/paper.pdf

# Extract references without downloading (debug mode)
paperchaser path/to/paper.pdf --debug

# Specify output directory
paperchaser path/to/paper.pdf -o downloaded_papers

# Force re-download of existing papers
paperchaser path/to/paper.pdf -f
```

Advanced options:
```bash
Options:
  -o, --output-dir TEXT      Directory to save downloaded papers
  --email TEXT              Email for Unpaywall API (optional)
  -f, --force              Force download even if paper already exists
  --rename/--no-rename     Rename downloaded PDFs using metadata (default: True)
  --debug                  Show debug information without downloading
  --help                   Show this message and exit
```

## Output Format

The tool provides detailed information about the extraction and download process:
- Reference extraction progress
- Found references with numbering
- Download status for each paper
- Color-coded success/failure indicators
- Detailed error messages for failed downloads
