"""
Content fetcher module for URL-based content extraction.
Supports fetching and normalizing content from web URLs.
"""

import re
from typing import Optional
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB_DEPS = True
except ImportError:
    HAS_WEB_DEPS = False


class ContentFetchError(Exception):
    """Custom exception for content fetching errors."""
    pass


class ContentFetcher:
    """
    Fetches and normalizes content from URLs.
    
    Supports extracting readable content from web pages,
    stripping HTML and extracting main article text.
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the content fetcher.
        
        Args:
            timeout: Request timeout in seconds
        """
        if not HAS_WEB_DEPS:
            raise ContentFetchError(
                "URL fetching requires 'requests' and 'beautifulsoup4' packages. "
                "Install with: pip install requests beautifulsoup4"
            )
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def fetch(self, url: str) -> str:
        """
        Fetch content from a URL.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            Extracted and normalized text content
            
        Raises:
            ContentFetchError: If fetching or parsing fails
        """
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ContentFetchError(f"Invalid URL: {url}")
        
        if parsed.scheme not in ("http", "https"):
            raise ContentFetchError(f"Unsupported URL scheme: {parsed.scheme}")
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ContentFetchError(f"Failed to fetch URL: {e}")
        
        # Parse HTML
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            return self._extract_content(soup)
        except Exception as e:
            raise ContentFetchError(f"Failed to parse content: {e}")
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from parsed HTML.
        
        Attempts to find the main article content by looking for
        common article containers and falling back to body text.
        """
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()
        
        # Try to find main content containers
        content = None
        
        # Common article containers
        selectors = [
            "article",
            "[role='main']",
            "main",
            ".post-content",
            ".article-content",
            ".entry-content",
            ".content",
            "#content",
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element and len(element.get_text(strip=True)) > 200:
                content = element
                break
        
        # Fallback to body
        if content is None:
            content = soup.body if soup.body else soup
        
        # Extract and normalize text
        text = content.get_text(separator="\n", strip=True)
        return self._normalize_text(text)
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize extracted text.
        
        - Removes excessive whitespace
        - Joins broken lines
        - Removes very short lines (likely navigation)
        """
        lines = text.split("\n")
        
        # Filter out very short lines (likely nav/buttons)
        filtered_lines = []
        for line in lines:
            line = line.strip()
            # Keep lines with substantial content
            if len(line) > 20 or (filtered_lines and len(line) > 0):
                filtered_lines.append(line)
        
        # Join with proper spacing
        text = "\n\n".join(
            line for line in filtered_lines 
            if line
        )
        
        # Clean up multiple newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        return text.strip()


def fetch_content(url: str, timeout: int = 30) -> str:
    """
    Convenience function to fetch content from a URL.
    
    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Extracted text content
    """
    fetcher = ContentFetcher(timeout=timeout)
    return fetcher.fetch(url)


def resolve_input(
    input_type: str,
    content: str,
    timeout: int = 30
) -> str:
    """
    Resolve input content based on type.
    
    Args:
        input_type: Either "text" or "url"
        content: The text content or URL
        timeout: Timeout for URL fetching
        
    Returns:
        Resolved text content
    """
    if input_type == "url":
        return fetch_content(content, timeout=timeout)
    return content
