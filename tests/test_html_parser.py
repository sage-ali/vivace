import pytest
from logic.utilities.html_parser import get_website_content


@pytest.mark.asyncio
async def test_get_website_content():
    """
    Tests the get_website_content function.

    Given a URL, this function should return its content as a string.
    The content should be a non-empty string.
    """
    urls = "https://aws.amazon.com/what-is/retrieval-augmented-generation/"
    content = get_website_content(urls)
    assert isinstance(content, str)
    assert len(content) > 0
