"""
Heading Tag Analyser - Core Logic
Fetches a webpage and extracts all heading tags (H1-H6) with their counts and text.
"""

import requests
from bs4 import BeautifulSoup

HEADING_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_headings(url: str) -> dict:
    """
    Fetch a webpage and return heading counts and texts.

    Returns:
        {
            "success": True/False,
            "url": str,
            "headings": {
                "h1": ["text1", "text2", ...],
                "h2": [...],
                ...
            },
            "error": str or None
        }
    """
    # Ensure URL has a scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    result = {
        "success": False,
        "url": url,
        "headings": {tag: [] for tag in HEADING_TAGS},
        "error": None,
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        result["error"] = f"Could not connect to {url}. Check that the URL is correct."
        return result
    except requests.exceptions.Timeout:
        result["error"] = f"Request timed out after 15 seconds. The site may be too slow."
        return result
    except requests.exceptions.HTTPError as e:
        result["error"] = f"HTTP error {e.response.status_code}: {e.response.reason}"
        return result
    except requests.exceptions.RequestException as e:
        result["error"] = f"Request failed: {str(e)}"
        return result

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in HEADING_TAGS:
            elements = soup.find_all(tag)
            result["headings"][tag] = [el.get_text(strip=True) for el in elements]
        result["success"] = True
    except Exception as e:
        result["error"] = f"Failed to parse page HTML: {str(e)}"

    return result


def get_total_headings(headings: dict) -> int:
    return sum(len(texts) for texts in headings.values())
