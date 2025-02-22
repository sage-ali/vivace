import requests
from bs4 import BeautifulSoup
import markdownify
import pypdf
from io import BytesIO
import os
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)


def get_website_content(urls):
    """Extracts text from HTML and PDF files, handling multiple URLs and errors."""
    text_content = ""
    errors = []
    for url_str in urls.split(","):
        url = url_str.strip()
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            if response.headers["Content-Type"] == "application/pdf":
                # Handle PDF files
                try:
                    pdf_reader = PdfReader(BytesIO(response.content))
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
                except Exception as e:
                    logger.error(f"Error processing PDF {url}: {e}")
                    errors.append(f"Error processing PDF {url}: {e}")
            else:
                # Handle HTML files
                try:
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Remove tags that are difficult to process by the AI
                    tags_to_remove = ["img", "script", "style", "iframe"]
                    for tag in soup.find_all(tags_to_remove):
                        tag.decompose()

                    # Remove all attributes from all tags
                    for tag in soup.find_all():
                        tag.attrs = None

                    # Convert the modified HTML to markdown
                    text_content += markdownify.markdownify(str(soup)) + "\n"
                except Exception as e:
                    logger.error(f"Error processing HTML {url}: {e}")
                    errors.append(f"Error processing HTML {url}: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            errors.append(f"Error fetching URL {url}: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred for URL {url}: {e}")
            errors.append(f"An unexpected error occurred for URL {url}: {e}")

    if errors:
        logger.error(f"Errors occurred during website content extraction: {errors}")
    return text_content
