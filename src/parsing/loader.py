from pathlib import Path
from pypdf import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF resume."""

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file_path: str) -> str:
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text


def clean_text(text: str) -> str:
    """Clean unnecessary spaces and blank lines."""

    return " ".join(text.split())


def load_resume(file_path: str) -> list[str]:
    """
    Load a PDF or DOCX resume and split it into chunks.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".pdf":
        text = extract_pdf_text(str(path))

    elif extension == ".docx":
        text = extract_docx_text(str(path))

    else:
        raise ValueError(
            "Unsupported file type. Please use PDF or DOCX."
        )

    text = clean_text(text)

    if not text:
        raise ValueError(
            "No readable text found in the resume."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    return chunks