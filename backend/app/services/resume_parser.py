from pathlib import Path

import fitz  # PyMuPDF
from docx import Document

from app.core.logging import get_logger

logger = get_logger(__name__)


class UnsupportedFileTypeError(Exception):
    pass


class EmptyResumeTextError(Exception):
    pass


def extract_text(file_path: Path) -> str:
    """Extract raw text from a PDF, DOCX, or TXT file."""
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        text = _extract_pdf_text(file_path)
    elif extension == ".docx":
        text = _extract_docx_text(file_path)
    elif extension == ".txt":
        text = _extract_txt_text(file_path)
    else:
        raise UnsupportedFileTypeError(f"Unsupported file extension: {extension}")

    text = text.strip()
    if not text:
        raise EmptyResumeTextError("No extractable text found in the resume")

    logger.info("Extracted text from resume, length=%d chars", len(text))
    return text


def _extract_pdf_text(file_path: Path) -> str:
    doc = fitz.open(file_path)
    try:
        pages = [page.get_text() for page in doc]
    finally:
        doc.close()
    return "\n".join(pages)


def _extract_docx_text(file_path: Path) -> str:
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)


def _extract_txt_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore")