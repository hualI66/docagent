from pathlib import Path
from typing import Optional
import time

class FileExtractor:
    CODE_EXTENSIONS = {'.py', '.js', '.java', '.go', '.rs', '.ts', '.cpp', '.c', '.rb', '.php'}
    MARKDOWN_EXTENSIONS = {'.md', '.markdown', '.txt'}

    def __init__(self):
        self._type: Optional[str] = None
        self._last_content: Optional[str] = None

    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()

        if ext == '.pdf':
            self._type = 'pdf'
            content = self._extract_pdf(file_path)
        elif ext in self.CODE_EXTENSIONS:
            self._type = 'code'
            content = path.read_text(encoding='utf-8')
        elif ext in self.MARKDOWN_EXTENSIONS:
            self._type = 'markdown'
            content = path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        self._last_content = content
        return content

    def get_type(self) -> Optional[str]:
        return self._type

    def _extract_pdf(self, file_path: str) -> str:
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        # Explicitly close reader to release file handle
        reader.stream.close() if hasattr(reader, 'stream') and reader.stream else None
        return text