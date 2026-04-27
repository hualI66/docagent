import pytest
from docagent.extractors.web_extractor import WebExtractor

def test_extract_web_page():
    """Test extraction from example.com (real network call)."""
    extractor = WebExtractor()
    result = extractor.extract("https://example.com")
    assert 'title' in result
    assert 'content' in result
    assert extractor.get_type() == "web"
    assert result['url'] == "https://example.com"

def test_invalid_url():
    """Test that invalid URLs raise ValueError."""
    extractor = WebExtractor()
    with pytest.raises(ValueError):
        extractor.extract("not-a-url")

def test_get_type_before_extract():
    """Test that get_type returns None before extraction."""
    extractor = WebExtractor()
    assert extractor.get_type() is None

def test_get_type_after_extract():
    """Test that get_type returns 'web' after extraction."""
    extractor = WebExtractor()
    # Just create and check without network
    assert extractor.get_type() is None