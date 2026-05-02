from bs4 import BeautifulSoup
import re

def clean_email_body(raw_html: str) -> str:
    """
    Strips all HTML tags, scripts, and extra whitespace from an email body
    to return a clean string suitable for an LLM context window.
    """
    if not raw_html:
        return ""

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove all <script> and <style> elements
    for element in soup(["script", "style"]):
        element.extract()

    # Get text with a space separator to avoid words squishing together
    text = soup.get_text(separator=' ')

    # Remove extra whitespace (multiple spaces/newlines become single ones)
    clean_text = re.sub(r'\s+', ' ', text).strip()

    return clean_text
