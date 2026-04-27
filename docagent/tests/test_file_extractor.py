import pytest
import os
from docagent.extractors.file_extractor import FileExtractor

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def test_extract_python_file():
    extractor = FileExtractor()
    content = extractor.extract(os.path.join(FIXTURES_DIR, "sample.py"))
    assert "def hello" in content
    assert extractor.get_type() == "code"

def test_extract_markdown_file():
    extractor = FileExtractor()
    content = extractor.extract(os.path.join(FIXTURES_DIR, "sample.md"))
    assert "# Title" in content
    assert extractor.get_type() == "markdown"

def test_unsupported_file():
    extractor = FileExtractor()
    with pytest.raises(ValueError):
        extractor.extract(os.path.join(FIXTURES_DIR, "sample.xyz"))

def test_get_type_before_extract():
    extractor = FileExtractor()
    assert extractor.get_type() is None

def test_file_not_found():
    extractor = FileExtractor()
    with pytest.raises(FileNotFoundError):
        extractor.extract("nonexistent_file.py")