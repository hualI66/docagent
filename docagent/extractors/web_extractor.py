from typing import Optional
import requests
from bs4 import BeautifulSoup

class WebExtractor:
    """Extract content from web pages for documentation generation."""

    def __init__(self, timeout: int = 10):
        """Initialize WebExtractor.

        Args:
            timeout: Request timeout in seconds (default 10)
        """
        self._type: Optional[str] = None
        self._result: Optional[dict] = None
        self._timeout = timeout

    def extract(self, url: str) -> dict:
        """Extract title and content from a URL.

        Args:
            url: The URL to extract content from

        Returns:
            dict with 'title', 'content', and 'url' keys

        Raises:
            ValueError: If URL is invalid
            ConnectionError: If connection fails
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=self._timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise ConnectionError(f"Request timed out for URL: {url}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch {url}: {str(e)}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else ""

        # Remove script and style tags
        for tag in soup(['script', 'style']):
            tag.decompose()

        # Extract body text
        content = soup.get_text(separator='\n', strip=True)

        # Clean empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        content = '\n'.join(lines)

        self._type = 'web'
        self._result = {
            'title': title,
            'content': content,
            'url': url
        }

        return self._result

    def get_type(self) -> Optional[str]:
        """Return the type of extracted content.

        Returns:
            'web' if extract() has been called, None otherwise
        """
        return self._type