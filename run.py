import asyncio
import pprint

from ai_extractor import unearth_insights
from schemas import NewsPortalSchema, digital_marketplace_blueprint
from web_scraping import async_scrape_with_playwright

# Main execution block for testing
if __name__ == "__main__":
    word_limit = 4000

    # URLs for scraping
    cnn_url = "https://www.cnn.com"
    wsj_url = "https://www.wsj.com"
    nyt_url = "https://www.nytimes.com/ca/"
    amazon_url = "https://www.amazon.ca/s?k=computers&crid=1LUXGQOD2ULFD&sprefix=%2Caps%2C94&ref=nb_sb_ss_recent_1_0_recent"

    async def playwright_scrape_and_analyze(url: str, tags, **kwargs):
        html_content = await async_scrape_with_playwright(url, tags)

        print("Unearthing insights with the Language Genie")

        html_content_fits_context_window_llm = html_content[:word_limit]

        extracted_content = unearth_insights(
            **kwargs, textual_matter=html_content_fits_context_window_llm
        )

        pprint.pprint(extracted_content)

    # Scrape and Extract with Language Model
    asyncio.run(
        playwright_scrape_and_analyze(
            url=wsj_url, tags=["span"], schema_pydantic=NewsPortalSchema
        )
    )
