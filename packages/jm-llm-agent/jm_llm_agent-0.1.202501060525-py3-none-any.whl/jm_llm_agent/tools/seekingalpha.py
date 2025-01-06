import asyncio
import json
import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Tuple
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from jm_llm_agent.tools.web import read_urls

logger = logging.getLogger(__name__)


def select_one(soup: BeautifulSoup, pattern: str) -> str:
    element = soup.select_one(pattern)
    return element.get_text(separator="\n", strip=True) if element else ""


def select(soup: BeautifulSoup, pattern: str) -> list[str]:
    return [div.get_text(separator="\n", strip=True) for div in soup.select(pattern)]


def convert_time(time: str) -> str:
    if not time:
        return ""
    time_str = time
    clean_str = time_str.replace(" ET", "")
    naive_date = datetime.strptime(clean_str, "%b. %d, %Y %I:%M %p")
    aware_date = naive_date.astimezone(ZoneInfo("America/New_York"))
    return aware_date.isoformat()


def parse_sk(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    title = select_one(soup, "h1")
    content = "\n".join(select(soup, "div[data-test-id='content-container']"))
    comments = select(soup, "div[data-test-id='comment-content']")

    # metas
    time = select_one(soup, "span[data-test-id='post-date']")
    time = convert_time(time)
    ticker = select_one(soup, "a[data-test-id='key-stats-ticker-link']")

    return {
        "title": title,
        "time": time,
        "ticker": ticker,
        "content": content,
        "comments": comments,
    }


def parse_sk_json(js_obj: dict):
    base_url = "https://seekingalpha.com"
    try:
        articles_obj = js_obj
        articles = articles_obj["data"]
        return [
            {
                "title": article["attributes"]["title"],
                "url": f"{base_url}/{article['links']['self']}",
            }
            for article in articles
        ]
    except Exception as e:
        logger.error(f"parse_sk_json: {str(e)}")
        return []


async def list_articles(tick: str) -> List[Dict[str, str]]:
    url = f"https://seekingalpha.com/symbol/{tick}/analysis"
    results = await read_urls(
        [{"url": url, "xhr_pattern": r"analysis\?"}],
        parse_sk_json,
        headless=False,
        timeout=5000,
        save_cookies=False,
    )
    results = results[url]
    return results


def parse_trending_articles(html_content: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.select("article[data-test-id='post-list-item']")
    base_url = "https://seekingalpha.com"
    articles_list = []
    for article in articles:
        h3 = article.select_one("h3")
        a = h3.select_one("a")
        title = a.get_text(strip=True)
        url = a["href"]
        articles_list.append(
            {
                "title": title,
                "url": f"{base_url}/{url}",
            }
        )
    return articles_list


async def list_trending_articles():
    url = "https://seekingalpha.com/trending-analysis"
    results = await read_urls(
        [{"url": url, "scroll_times": 3}], parse_trending_articles, headless=False
    )
    return results[url]


async def list_growth_articles():
    url = "https://seekingalpha.com/growth-analysis"
    results = await read_urls(
        [{"url": url, "scroll_times": 3}], parse_trending_articles, headless=False
    )
    return results[url]


async def get_articles(urls: List[str]) -> Dict[str, Dict[str, Any]]:
    article_infos = {}
    for url in urls:
        results = await read_urls(
            [{"url": url, "scroll_times": 10}], parse_sk, headless=False
        )
        result = results[url]
        article_id = url.split("/")[-1]
        result["_id"] = article_id
        result["url"] = url
        result["platform"] = "seekingalpha"
        article_infos[url] = result
    return article_infos


async def save_article_to_remote(article: Dict[str, Any]):
    API_BASE = "https://followany.com/api"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE}/content/save", json=article, timeout=30.0
            )
            response.raise_for_status()
            logger.info(f"Successfully saved content to api: {article.get('_id')}")
            return True
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred while saving content: {str(e)}")
        return False

    except httpx.RequestError as e:
        logger.error(f"Request error occurred while saving content: {str(e)}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error while saving content: {str(e)}")
        return False


async def save_to_remote(
    urls: List[str], gap: Tuple[int, int] = (3, 5)
) -> List[Dict[str, Any]]:
    ret_infos = []
    for url in urls:
        article_infos = await get_articles([url])
        article_info = article_infos[url]
        if "content" not in article_info or "title" not in article_info:
            logger.warning(f"no content or title found for {url}")
            continue
        if not article_info["ticker"]:
            logger.warning(f"no ticker found for {url}")
        logger.info(
            f"start saving article: {article_info['_id']} ticker:{article_info['ticker']} "
            f"title: {article_info['title']}\ncontent: {article_info['content'][:20]}"
        )
        success = await save_article_to_remote(article_info)
        if success:
            ret_infos.append(article_info)
            await asyncio.sleep(random.randint(gap[0], gap[1]))
    return ret_infos


async def sk_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
        )
        try:
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
                # 添加其他浏览器特征
                java_script_enabled=True,
                has_touch=False,
                is_mobile=False,
                locale="en-US",
            )

            # 注入脚本以避免被检测为自动化浏览器
            await context.add_init_script(
                """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
            )

            page = await context.new_page()

            # 直接访问登录页面
            await page.goto("https://seekingalpha.com/login")
            logger.info("Waiting for manual login...")

            # 等待登录成功
            await page.wait_for_timeout(60000)
            logger.info("Login successful!")

            cookies = await context.cookies()
            cookie_file = "cookies/seekingalpha.com.json"
            with open(cookie_file, "w") as f:
                json.dump(cookies, f)
                logger.info(f"Saved cookies for seekingalpha.com to {cookie_file}")

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
        finally:
            await browser.close()
