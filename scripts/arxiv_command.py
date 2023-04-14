from arxiv import Client, arxiv
from config import Config

import os
import os.path
import re

cfg = Config()

# Set a dedicated folder for file I/O
working_directory = "auto_gpt_workspace"

def download_recent_arxiv_papers(query, number):
    # Validate and convert the number argument
    if isinstance(number, str):
        try:
            number = int(number)
        except ValueError:
            raise ValueError("Invalid number. Please enter a positive integer.")

    if not isinstance(query, str) or not isinstance(number, int) or number < 1:
        raise ValueError("Invalid arguments. Query must be a string and number must be a positive integer.")

    # Create a search object using the arxiv library
    search = arxiv.Search(
        query=query,
        max_results=number,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    output_info = []

    # Iterate over the results and download each pdf
    for result in search.results():
        # Get the arXiv ID for the filename
        arxiv_id = result.entry_id.split('/')[-1]
        filename = f"{arxiv_id}.pdf"
        file_path = os.path.join(working_directory, filename)
        print(f"Saving: {filename}")
        result.download_pdf(filename=file_path)

        # Add the title and filename pair to the output_info list
        output_info.append((result.title, filename))

    return output_info

def download_arxiv_paper_by_id(arxiv_id):
    client = Client()

    # Fetch paper by arXiv ID
    paper = client.get_submission(arxiv_id)

    # Create a custom filename based on the arXiv ID
    filename = f"{arxiv_id}.pdf"
    file_path = os.path.join(working_directory, filename)
    print(f"Saving: {filename}")

    # Download the paper
    paper.download_pdf(filename=file_path)

    return (paper.title, filename)
