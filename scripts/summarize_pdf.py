# Import the necessary modules
import PyPDF4

from config import Config
import file_operations
import browse
import os
import os.path
from llm_utils import create_chat_completion

cfg = Config()

# Set a dedicated folder for file I/O
working_directory = "auto_gpt_workspace"

def summarize_pdf(pdf_path, question):
    """Summarize text from a PDF file within the working_directory using the LLM model"""
    if not pdf_path:
        return "Error: No PDF file to summarize"

    # Check if the file is in the working_directory
    if not pdf_path.startswith(working_directory):
        pdf_path = os.path.join(working_directory, pdf_path)

    # Confirm the existence of the file
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File '{pdf_path}' not found in the '{working_directory}' directory.")

    # Extract text from the PDF file
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF4.PdfFileReader(file)
        num_pages = pdf_reader.getNumPages()
        text = ""
        for i in range(num_pages):
            page = pdf_reader.getPage(i)
            text += page.extractText()

    text_length = len(text)
    print(f"Text length: {text_length} characters")

    summaries = []
    chunks = list(browse.split_text(text))

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i + 1} / {len(chunks)}")
        messages = [browse.create_message(chunk, question)]

        summary = create_chat_completion(
            model=cfg.fast_llm_model,
            messages=messages,
            max_tokens=300,
        )
        summaries.append(summary)

    print(f"Summarized {len(chunks)} chunks.")

    combined_summary = "\n".join(summaries)
    messages = [browse.create_message(combined_summary, question)]

    # temporary hack: use a larger context model all the time. 
    # TODO: swich between fast or slow model based on size of summaries to summarize
    final_summary = create_chat_completion(
        model=cfg.smart_llm_model,
        messages=messages,
        max_tokens=300,
    )

    return final_summary