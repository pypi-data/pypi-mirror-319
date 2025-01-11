import click
import PyPDF2
import re
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from pathlib import Path
import scholarly
from tqdm import tqdm
import time
import difflib
import subprocess

def extract_references(pdf_path):
    """Extract references section from PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # First try reading the entire document
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            
            # Try to detect if this is a two-column format
            lines = page_text.split('\n')
            if len(lines) > 10:  # Need enough lines to detect pattern
                # Check if we have alternating short lines (potential column format)
                line_lengths = [len(line.strip()) for line in lines if line.strip()]
                if line_lengths:  # Only proceed if we have non-empty lines
                    avg_length = sum(line_lengths) / len(line_lengths)
                    max_length = max(line_lengths)
                    
                    # Count lines that are significantly shorter than the longest line
                    short_lines = sum(1 for length in line_lengths if length < max_length * 0.5)
                    
                    if short_lines > len(line_lengths) * 0.3:  # If more than 30% are short lines
                        # Likely two-column format, try to merge columns
                        # First, group lines by their horizontal position
                        left_col = []
                        right_col = []
                        
                        for line in lines:
                            if not line.strip():
                                continue
                            # If line starts with significant whitespace, it's likely right column
                            if line.startswith('    '):
                                right_col.append(line.strip())
                            else:
                                left_col.append(line.strip())
                        
                        # Merge columns with proper spacing
                        merged_text = ""
                        max_lines = max(len(left_col), len(right_col))
                        for i in range(max_lines):
                            left = left_col[i] if i < len(left_col) else ""
                            right = right_col[i] if i < len(right_col) else ""
                            merged_text += left
                            if right:
                                merged_text += " " + right
                            merged_text += "\n"
                        
                        page_text = merged_text
            
            full_text += page_text + "\n"
        
        # Try to find the references section
        ref_section = None
        ref_patterns = [
            r'(?:REFERENCES|Bibliography|Works Cited|References Cited)[\s\n]+(.+?)(?=\n\s*(?:APPENDIX|Acknowledgments|Notes|Supplementary|$))',
            r'\n(?:REFERENCES|Bibliography|Works Cited|References Cited)\s*\n(.+?)(?=\n\s*(?:APPENDIX|Acknowledgments|Notes|Supplementary|$))',
            r'\[\s*REFERENCES\s*\]\s*\n(.+?)(?=\n\s*(?:APPENDIX|Acknowledgments|Notes|Supplementary|$))',
        ]
        
        for pattern in ref_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                ref_section = match.group(1)
                break
        
        # If no clear references section found, use the latter part of the document
        if not ref_section and len(full_text.split('\n')) > 20:
            lines = full_text.split('\n')
            # Look for a line that starts with a reference-like pattern
            for i, line in enumerate(lines):
                if re.match(r'(?:\[\d+\]|\d+\.|References:?|Bibliography:?)', line.strip()):
                    ref_section = '\n'.join(lines[i:])
                    break
        
        final_text = ref_section if ref_section else full_text
        click.echo(f"Total text length after cleanup: {len(final_text)} characters")
        
        return final_text

def parse_references(ref_text):
    """Parse individual references with improved splitting."""
    if not ref_text:
        return []
    
    click.echo(f"\nAttempting to parse references from text of length: {len(ref_text)}")
    
    # Remove duplicate REFERENCES headers and clean up text
    ref_text = re.sub(r'(?:REFERENCES\s*)+', '', ref_text, flags=re.IGNORECASE)
    ref_text = re.sub(r'\s+', ' ', ref_text)  # Normalize whitespace
    
    # Split references by looking for numbered patterns in continuous text
    references = []
    
    # Multiple patterns to match different reference formats
    patterns = [
        # Standard numbered format with dot: "1. Author et al..."
        r'(?:^|\s+)(\d{1,3})\.\s+([^0-9][^\n]+?)(?=\s+\d{1,3}\.\s+|$)',
        # Bracketed format: "[1] Author et al..."
        r'(?:^|\s+)\[(\d{1,3})\]\s+([^0-9][^\n]+?)(?=\s+\[\d{1,3}\]\s+|$)',
        # Harvard style: "Author et al. (YEAR)..."
        r'(?:^|\s+)([A-Z][^.]+?et\s+al\.,?\s+\(\d{4}\)[^.]+\.)(?=\s+[A-Z]|$)',
        # Author-year format: "Author, Year..."
        r'(?:^|\s+)([A-Z][^,]+?,\s+(?:19|20)\d{2}[^.]+\.)(?=\s+[A-Z]|$)'
    ]
    
    # Try each pattern until we find references
    for pattern in patterns:
        matches = re.finditer(pattern, ref_text, re.DOTALL | re.MULTILINE)
        refs = []
        
        for match in matches:
            if len(match.groups()) == 2:  # Numbered formats
                ref_num, ref_content = match.groups()
                # Validate reference number is reasonable
                if int(ref_num.strip('[]')) > 100:  # Skip unreasonably high numbers
                    continue
            else:  # Author-year format
                ref_content = match.group(1)
            
            # Clean up the reference text
            ref_content = ref_content.strip()
            ref_content = re.sub(r'\s+', ' ', ref_content)  # Normalize whitespace
            
            # Filter out false positives
            if len(ref_content) < 30:  # Too short to be a reference
                continue
            if not re.search(r'[A-Z][a-z]+', ref_content):  # No proper names
                continue
            if ref_content.startswith(('http://', 'https://', 'www.')):  # Just a URL
                continue
            if 'permission' in ref_content.lower():  # Copyright/permission text
                continue
            
            refs.append(ref_content)
        
        if len(refs) >= 5:  # Only use this pattern if it found a reasonable number of references
            references = refs
            break
    
    # If no references found with patterns, try simple line-based splitting
    if not references:
        # Look for lines that start with numbers or author names
        lines = ref_text.split('\n')
        current_ref = ""
        
        for line in lines:
            line = line.strip()
            # Start of a new reference
            if re.match(r'(?:\d+\.|\[\d+\]|[A-Z][a-z]+\s+(?:et\s+al\.|and|&))', line):
                if current_ref and len(current_ref) > 30:
                    references.append(current_ref)
                current_ref = line
            # Continuation of current reference
            elif line and current_ref:
                current_ref += " " + line
        
        # Add the last reference
        if current_ref and len(current_ref) > 30:
            references.append(current_ref)
    
    # Final filtering of references
    filtered_refs = []
    for ref in references:
        # Must contain at least one proper name
        if not re.search(r'[A-Z][a-z]+', ref):
            continue
        # Must be a reasonable length
        if len(ref) < 30 or len(ref) > 1000:
            continue
        # Must not be just a URL or DOI
        if ref.strip().startswith(('http://', 'https://', 'www.', '10.')):
            continue
        filtered_refs.append(ref)
    
    click.echo(f"Found {len(filtered_refs)} references")
    
    # Debug output for first few references
    if filtered_refs:
        click.echo("\nFirst few references found:")
        for i, ref in enumerate(filtered_refs[:3], 1):  # Only show top 3 for testing
            click.echo(f"{i}. {ref[:150]}...")
    
    return filtered_refs

def get_doi_from_reference(ref):
    """Enhanced DOI extraction from reference text."""
    # Standard DOI pattern with more variations
    doi_patterns = [
        r'(?:doi:?\s*|(?:https?://)?(?:dx\.)?doi\.org/)(10\.\d{4,9}/[-._;()/:\w]+)',
        r'(10\.\d{4,9}/[-._;()/:\w]+)'
    ]
    
    for pattern in doi_patterns:
        match = re.search(pattern, ref, re.IGNORECASE)
        if match:
            # Get the DOI part from the match
            doi = match.group(1) if len(match.groups()) > 0 else match.group(0)
            # Clean up DOI
            doi = doi.strip('.')  # Remove trailing periods
            return doi
    return None

def get_title_from_reference(ref):
    """Extract title from reference text."""
    # Try to get title before the first period that's not part of et al.
    parts = re.split(r'(?<!al)\.\s+', ref)
    if parts:
        title = parts[0].strip()
        # Remove any leading numbers or brackets
        title = re.sub(r'^\s*\d+\.\s*|\[\d+\]\s*', '', title)
        # Clean up the title for filename use
        title = re.sub(r'[^\w\s-]', '', title)
        title = re.sub(r'\s+', '_', title)
        return title[:100]  # Limit length for filename
    return None

def try_open_access_sources(doi, ref):
    """Try to get PDF from open access sources."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try PubMed Central
    try:
        # Convert DOI to PubMed ID
        pmid_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={doi}&format=json"
        response = requests.get(pmid_url, headers=headers, timeout=10)
        data = response.json()
        
        if 'records' in data and data['records']:
            record = data['records'][0]
            if 'pmcid' in record:
                pmcid = record['pmcid']
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf"
                response = requests.get(pdf_url, headers=headers, timeout=10)
                if response.headers.get('content-type', '').lower() == 'application/pdf':
                    return response.content, "PubMed Central"
    except:
        pass

    # Try Unpaywall API
    try:
        email = "getpapers@example.com"  # Should be replaced with user's email
        unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
        response = requests.get(unpaywall_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('is_oa') and data.get('best_oa_location'):
                pdf_url = data['best_oa_location'].get('pdf_url')
                if pdf_url:
                    response = requests.get(pdf_url, headers=headers, timeout=10)
                    if response.headers.get('content-type', '').lower() == 'application/pdf':
                        return response.content, "Unpaywall"
    except:
        pass
    
    # Try arXiv (if reference contains arXiv ID)
    try:
        arxiv_match = re.search(r'arxiv:?(\d+\.\d+)', ref, re.IGNORECASE)
        if arxiv_match:
            arxiv_id = arxiv_match.group(1)
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            response = requests.get(pdf_url, headers=headers, timeout=10)
            if response.headers.get('content-type', '').lower() == 'application/pdf':
                return response.content, "arXiv"
    except:
        pass
    
    return None, None

def paper_already_downloaded(title, doi, output_dir):
    """Check if paper is already downloaded by looking for title or DOI in filenames."""
    if not title and not doi:
        return False
        
    for file in output_dir.glob('*.pdf'):
        filename = file.stem  # Get filename without extension
        if title and title.lower() in filename.lower():
            return True
        if doi and doi.replace('/', '_') in filename:
            return True
    return False

def rename_downloaded_pdf(pdf_path, ref=None, doi=None):
    """Rename PDF using pdfrenamer command-line tool."""
    try:
        # Run pdfrenamer with title and year format
        result = subprocess.run(
            ['pdfrenamer', '-f', '{T}_{YYYY}', str(pdf_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get the new filename from the output
        for line in result.stdout.split('\n'):
            if '-->' in line:
                _, new_name = line.split('-->')
                new_name = new_name.strip()
                click.echo(f"Renamed to: {new_name}")
                return pdf_path.parent / new_name
        
        return pdf_path
    except subprocess.CalledProcessError as e:
        click.echo(f"Warning: Could not rename PDF: {e.stderr}")
        return pdf_path
    except Exception as e:
        click.echo(f"Warning: Could not rename PDF: {str(e)}")
        return pdf_path

def download_paper(doi, ref, output_dir):
    """Download paper from Sci-Hub with enhanced error handling and open access fallback."""
    # Check if already downloaded
    title = get_title_from_reference(ref)
    if paper_already_downloaded(title, doi, output_dir):
        return True, "Already downloaded"
    
    scihub_urls = [
        'https://sci-hub.se/',
        'https://sci-hub.st/',
        'https://sci-hub.ru/',
        'https://sci-hub.ee/',
        'https://sci-hub.wf/'
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    last_error = "Failed to download from all sources"
    
    # First try Sci-Hub
    pdf_content = None
    source = None
    
    for base_url in scihub_urls:
        try:
            response = requests.get(f"{base_url}{doi}", headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pdf_url = None
            iframe = soup.find('iframe', {'id': 'pdf'})
            if iframe and 'src' in iframe.attrs:
                pdf_url = iframe['src']
            
            if not pdf_url:
                embed = soup.find('embed', {'id': 'pdf'})
                if embed and 'src' in embed.attrs:
                    pdf_url = embed['src']
            
            if not pdf_url:
                last_error = f"No PDF URL found on {base_url}"
                continue
                
            if not pdf_url.startswith('http'):
                pdf_url = 'https:' + pdf_url if pdf_url.startswith('//') else base_url + pdf_url
            
            pdf_response = requests.get(pdf_url, headers=headers, timeout=10)
            if pdf_response.headers.get('content-type', '').lower() != 'application/pdf':
                last_error = f"Invalid content type from {base_url}"
                continue
            
            pdf_content = pdf_response.content
            source = "Sci-Hub"
            break
        except requests.RequestException as e:
            last_error = f"Request failed for {base_url}: {str(e)}"
        except Exception as e:
            last_error = f"Error with {base_url}: {str(e)}"
    
    # If Sci-Hub failed, try open access sources
    if not pdf_content:
        pdf_content, source = try_open_access_sources(doi, ref)
    
    if pdf_content:
        try:
            # Use title for filename, fallback to DOI if no title
            if not title:
                title = doi.replace('/', '_')
            
            # Clean filename and add source
            title = re.sub(r'[<>:"/\\|?*]', '', title)  # Remove invalid filename characters
            filename = f"{title}__{source}.pdf"
            output_path = output_dir / filename
            
            # Save the PDF
            with open(output_path, 'wb') as f:
                f.write(pdf_content)
            
            # Try to rename the file with better metadata
            renamed_path = rename_downloaded_pdf(output_path, ref, doi)
            return True, None
        except Exception as e:
            return False, f"Error saving PDF: {str(e)}"
    
    return False, last_error

def get_doi_from_title(title):
    """Try to find DOI using paper title via CrossRef API."""
    try:
        headers = {
            'User-Agent': 'GetPapers/1.0 (mailto:getpapers@example.com)'
        }
        # Clean and encode the title
        query = re.sub(r'\s+', '+', title.strip())
        url = f"https://api.crossref.org/works?query.title={query}&rows=1"
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data['message']['items']:
            item = data['message']['items'][0]
            # Check if the similarity is high enough (you might want to adjust this threshold)
            if 'title' in item and item['title']:
                title_similarity = difflib.SequenceMatcher(None, 
                    title.lower(), 
                    item['title'][0].lower()
                ).ratio()
                
                if title_similarity > 0.8:  # 80% similarity threshold
                    return item.get('DOI')
    except Exception as e:
        click.echo(f"Error searching CrossRef: {str(e)}", err=True)
    return None

def extract_title_from_reference(ref):
    """Extract title from reference string."""
    # Remove any leading numbers or brackets
    ref = re.sub(r'^\s*\d+\.\s*|\[\d+\]\s*', '', ref)
    
    # Try to get the title (text before the first period that's not part of et al.)
    match = re.split(r'(?<!al)\.\s+', ref)
    if match:
        return match[0].strip()
    return None

def format_click_table(headers, rows, title=None):
    """Create a nicely formatted click table with optional title."""
    table = tabulate(rows, headers=headers, tablefmt="grid")
    if title:
        table = f"\n{click.style(title, fg='blue', bold=True)}\n{table}"
    return table

# Remove the main() function and CLI code as it will be moved to cli.py 