import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def sanitize_html(html_content, unwanted_tags=["script", "style"]):
    """
    Sanitizes the HTML content by removing specified unwanted tags.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def harvest_tags(html_content, desired_tags: list[str]):
    """
    Harvests text from specified tags in HTML content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text_fragments = []

    for tag in desired_tags:
        elements = soup.find_all(tag)
        for element in elements:
            text_fragments.append(
                element.get_text()
                if tag != "a"
                else f"{element.get_text()} ({element.get('href')})"
            )

    return " ".join(text_fragments)


def streamline_content(content):
    """
    Streamlines the content by removing redundant lines and whitespace.
    """
    lines = content.split("\n")
    stripped_lines = [line.strip() for line in lines]
    non_empty_lines = [line for line in stripped_lines if line]
    seen = set()
    deduped_lines = [
        line for line in non_empty_lines if not (line in seen or seen.add(line))
    ]
    return "".join(deduped_lines)


async def async_scrape_with_playwright(
    url, desired_tags: list[str] = ["h1", "h2", "h3", "span"]
) -> str:
    """
    Asynchronously scrapes content from a URL using Playwright,
    focusing on extracting specific HTML tags and sanitizing the content.
    """
    print("Initiating web scraping magic...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)
            page_source = await page.content()
            results = streamline_content(
                harvest_tags(sanitize_html(page_source), desired_tags)
            )
            print("Content successfully scraped")
        except Exception as e:
            results = f"Scraping error: {e}"
        await browser.close()
    return results


# Testing the scraping function
if __name__ == "__main__":
    url = "https://www.everlane.com/collections/womens-new-arrivals"

    async def perform_scraping():
        results = await async_scrape_with_playwright(url)
        print(results)

    pprint.pprint(asyncio.run(perform_scraping()))
