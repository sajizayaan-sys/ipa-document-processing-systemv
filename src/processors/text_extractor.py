from pathlib import Path
from pypdf import PdfReader

def extract_text_from_file(file: Path) -> str:
    if file.suffix.lower() == ".txt":
        return file.read_text(encoding="utf-8", errors="ignore")

    if file.suffix.lower() == ".pdf":
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    return ""

