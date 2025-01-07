import click
from pathlib import Path
import time
from .core import (
    extract_references, parse_references, get_doi_from_reference,
    get_title_from_reference, paper_already_downloaded, download_paper,
    extract_title_from_reference, get_doi_from_title, format_click_table
)

class DownloadProgress:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.bar = click.progressbar(
            length=total,
            label='Downloading papers',
            show_pos=True,
            show_percent=True,
            show_eta=True,
            width=50
        )

    def update(self, amount=1):
        self.current += amount
        self.bar.update(amount)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.bar.finish()

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='downloaded_papers', 
              help='Directory to save downloaded papers')
@click.option('--email', default="getpapers@example.com",
              help='Email for Unpaywall API (optional)')
@click.option('--force', '-f', is_flag=True,
              help='Force download even if paper already exists')
def main(pdf_path, output_dir, email, force):
    """Download referenced papers from a PDF using Sci-Hub."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Extract and parse references
    with click.progressbar(
        length=1,
        label='Extracting references',
        show_eta=False,
        show_percent=False
    ) as bar:
        ref_text = extract_references(pdf_path)
        bar.update(1)
    
    references = parse_references(ref_text)
    
    if not references:
        click.echo("No references found in the PDF.")
        return
    
    # Process each reference
    results = []
    failed_downloads = []
    skipped = 0
    
    with DownloadProgress(len(references)) as progress:
        for i, ref in enumerate(references, 1):
            doi = get_doi_from_reference(ref)
            status = "No DOI found"
            
            # If no DOI found, try to get it from the title
            if not doi:
                title = extract_title_from_reference(ref)
                if title:
                    click.echo(f"\nSearching DOI for: {title[:100]}...")
                    doi = get_doi_from_title(title)
                    if doi:
                        click.echo(f"Found DOI: {doi}")
            
            if doi:
                # Check if already downloaded (unless force flag is set)
                if not force and paper_already_downloaded(get_title_from_reference(ref), doi, output_dir):
                    status = "Already downloaded"
                    skipped += 1
                else:
                    success, error = download_paper(doi, ref, output_dir)
                    if success:
                        status = "Downloaded"
                    else:
                        status = "Download failed"
                        failed_downloads.append({
                            'number': i,
                            'reference': ref,
                            'doi': doi,
                            'error': error
                        })
            else:
                failed_downloads.append({
                    'number': i,
                    'reference': ref,
                    'doi': 'No DOI found',
                    'error': 'Could not extract DOI or find it via title'
                })
            
            results.append([i, ref[:100] + "...", doi or "N/A", status])
            progress.update()
            time.sleep(1)  # Be nice to APIs
    
    # Display results table with nice formatting
    headers = ["#", "Reference", "DOI", "Status"]
    # Format the results for better display
    formatted_results = []
    for row in results:
        status_color = {
            "Downloaded": "green",
            "Already downloaded": "blue",
            "Download failed": "red",
            "No DOI found": "yellow"
        }.get(row[3], "white")
        
        formatted_row = [
            row[0],
            row[1],
            row[2],
            click.style(row[3], fg=status_color)
        ]
        formatted_results.append(formatted_row)
    
    click.echo(format_click_table(headers, formatted_results, title="Download Summary"))
    
    # Summary statistics with colored output
    success_count = sum(1 for r in results if r[3] == "Downloaded")
    click.echo(f"\nSuccessfully downloaded {click.style(str(success_count), fg='green')} "
               f"out of {click.style(str(len(references)), fg='blue')} papers.")
    if skipped > 0:
        click.echo(f"Skipped {click.style(str(skipped), fg='yellow')} papers (already downloaded)")
    
    # Display failed downloads with nice formatting
    if failed_downloads:
        failed_rows = []
        for fail in failed_downloads:
            failed_rows.append([
                fail['number'],
                fail['reference'][:100] + "...",
                fail['doi'],
                click.style(fail['error'], fg='red')
            ])
        
        click.echo(format_click_table(
            headers=["#", "Reference", "DOI", "Error"],
            rows=failed_rows,
            title="Failed Downloads"
        ))

if __name__ == '__main__':
    main() 