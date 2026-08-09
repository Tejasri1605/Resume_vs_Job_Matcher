import asyncio
from playwright.sync_api import sync_playwright


class ScrapingError(Exception):
    pass


CHROMIUM_PATH = (
    r"C:\Users\Palla. Saidulu\AppData\Local\ms-playwright"
    r"\chromium-1200\chrome-win64\chrome.exe"
)


def _scrape_sync(url: str, wait_time: int = 5) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROMIUM_PATH
        )

        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(wait_time * 1000)

        content = page.inner_text("body")
        browser.close()
        return content


async def scrape_linkedin_job_description(url: str, wait_time: int = 5) -> str:
    try:
        return await asyncio.to_thread(_scrape_sync, url, wait_time)
    except Exception as e:
        raise ScrapingError(
            f"Unexpected error during scraping of {url}: {e}"
        ) from e
