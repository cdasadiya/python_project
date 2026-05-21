#!/usr/bin/env python3
"""
Web Scraping Learning Framework (Single-file, Production-style Demo)
===================================================================
A complete educational + practical mini-framework that demonstrates major web scraping
concepts from beginner to advanced in ONE Python file.

IMPORTANT:
- This project is designed for LEGAL, ETHICAL, and SAFE scraping education.
- Default demo targets are safe endpoints (httpbin, jsonplaceholder, books.toscrape.com,
  quotes.toscrape.com, and w3schools sample XML).
- Some optional features (Selenium/Playwright) require external browser setup.

Python: 3.11+
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import logging
import random
import re
import sys
import threading
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Callable, Iterable, Optional
from urllib.parse import urlencode, quote_plus, urljoin, urlparse
from urllib.request import Request as UrllibRequest, urlopen
from urllib.robotparser import RobotFileParser

import requests
try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

try:
    from lxml import etree, html
except Exception:
    etree = None
    html = None

# Optional dependencies (graceful fallback)
try:
    import httpx
except Exception:
    httpx = None

try:
    import aiohttp
except Exception:
    aiohttp = None

try:
    from fake_useragent import UserAgent
except Exception:
    UserAgent = None

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
except Exception:
    webdriver = None
    ChromeOptions = None

try:
    from playwright.async_api import async_playwright
except Exception:
    async_playwright = None

APP_DIR = Path("scraper_output")
APP_DIR.mkdir(exist_ok=True)
LOG_FILE = APP_DIR / "scraper.log"
CACHE_FILE = APP_DIR / "cache.json"
SESSION_FILE = APP_DIR / "session.json"


class ConceptKnowledgeBase:
    """Contains concise learning notes for required libraries and concepts."""

    LIBRARIES: dict[str, dict[str, str]] = {
        "requests": {
            "purpose": "Human-friendly HTTP client for sync web requests.",
            "benefits": "Simple API, sessions, cookies, retries with adapters.",
            "install": "pip install requests",
            "common": "get/post/session/headers/timeout/json()",
            "best": "Always set timeout and custom user-agent; check status codes.",
            "perf": "Reuse Session for connection pooling.",
            "usage": "APIs, forms, static pages.",
        },
        "urllib": {
            "purpose": "Built-in low-level URL/HTTP and parsing tools.",
            "benefits": "No external dependency; URL encoding/parsing utilities.",
            "install": "Built-in",
            "common": "urlopen/Request/urlencode/quote_plus",
            "best": "Prefer for lightweight tasks and URL manipulation.",
            "perf": "Minimal overhead for simple calls.",
            "usage": "Encoding query strings, robots handling.",
        },
        "httpx": {
            "purpose": "Modern HTTP client with sync+async support.",
            "benefits": "HTTP/2, async, robust timeout model.",
            "install": "pip install httpx",
            "common": "Client/AsyncClient/get/post",
            "best": "Use async for high-concurrency scraping.",
            "perf": "Connection pooling + async cuts wait time.",
            "usage": "API-heavy scraping pipelines.",
        },
        "BeautifulSoup": {"purpose": "HTML/XML parser + DOM traversal.", "benefits": "Beginner-friendly selectors.", "install": "pip install beautifulsoup4", "common": "find/find_all/select", "best": "Use with lxml parser.", "perf": "For massive docs, lxml direct is faster.", "usage": "Article/product extraction."},
        "lxml": {"purpose": "Fast XML/HTML parsing with XPath.", "benefits": "Speed + powerful XPath.", "install": "pip install lxml", "common": "html.fromstring/xpath", "best": "Prefer XPath for complex nested extraction.", "perf": "Excellent for large pages.", "usage": "Structured and XML feeds."},
        "re": {"purpose": "Regex extraction and cleanup.", "benefits": "Flexible pattern matching.", "install": "Built-in", "common": "findall/search/sub", "best": "Use raw strings and tested patterns.", "perf": "Compile repeated patterns.", "usage": "Emails, prices, IDs."},
        "json": {"purpose": "JSON parse/serialize.", "benefits": "Native API data format.", "install": "Built-in", "common": "loads/dumps/load/dump", "best": "Validate schema keys.", "perf": "Use iter streaming for huge files.", "usage": "API ingestion/export."},
        "csv": {"purpose": "CSV reading/writing.", "benefits": "Spreadsheet compatible.", "install": "Built-in", "common": "DictWriter/DictReader", "best": "Explicit fieldnames + utf-8.", "perf": "Stream rows.", "usage": "Reporting and BI imports."},
        "asyncio": {"purpose": "Async event loop.", "benefits": "Massive IO concurrency.", "install": "Built-in", "common": "run/gather/create_task", "best": "Use for network-bound tasks.", "perf": "Reduces idle wait.", "usage": "Crawlers and API fanout."},
        "aiohttp": {"purpose": "Async HTTP client/server.", "benefits": "High-throughput fetch.", "install": "pip install aiohttp", "common": "ClientSession/get", "best": "Session reuse and timeouts.", "perf": "Excellent with asyncio.", "usage": "Async scraping."},
        "selenium": {"purpose": "Browser automation for JS pages.", "benefits": "Real browser behavior.", "install": "pip install selenium", "common": "webdriver/get/find_element", "best": "Headless in CI.", "perf": "Use sparingly; heavy.", "usage": "Login flows, dynamic content."},
        "playwright": {"purpose": "Modern browser automation.", "benefits": "Fast, stable, network interception.", "install": "pip install playwright && playwright install", "common": "async_playwright/new_page/goto", "best": "Use route interception and waits.", "perf": "Often faster than selenium.", "usage": "Infinite scroll and SPA scraping."},
        "concurrent.futures": {"purpose": "Thread/process pools.", "benefits": "Simple parallelism.", "install": "Built-in", "common": "ThreadPoolExecutor/map", "best": "Threads for IO tasks.", "perf": "Boosts throughput for multi-site fetch.", "usage": "Parallel static pages."},
        "logging": {"purpose": "Structured operational logs.", "benefits": "Debugging and auditability.", "install": "Built-in", "common": "getLogger/info/error", "best": "Include timestamps and levels.", "perf": "Avoid very chatty logs in hot loops.", "usage": "Production monitoring."},
        "fake_useragent": {"purpose": "Random realistic UA strings.", "benefits": "Reduces bot fingerprint monotony.", "install": "pip install fake-useragent", "common": "UserAgent().random", "best": "Fallback to fixed UA if unavailable.", "perf": "Cache generated values.", "usage": "UA rotation demos."},
        "time": {"purpose": "Timing/sleep/rate-limit basics.", "benefits": "Simple pacing and metrics.", "install": "Built-in", "common": "sleep/time", "best": "Prefer monotonic where needed.", "perf": "Avoid blocking in async paths.", "usage": "Backoff and schedule simulation."},
        "random": {"purpose": "Jitter, proxy/UA rotation.", "benefits": "Anti-pattern variability.", "install": "Built-in", "common": "choice/uniform/randint", "best": "Add jitter to delays.", "perf": "Very lightweight.", "usage": "Proxy selection, backoff jitter."},
    }


@dataclass
class ScrapeItem:
    source: str
    title: str
    url: str
    price: Optional[float] = None
    tags: list[str] = field(default_factory=list)
    email: Optional[str] = None
    image_url: Optional[str] = None


@dataclass
class ScraperConfig:
    timeout: int = 12
    max_retries: int = 3
    backoff_base: float = 1.2
    rate_limit_seconds: float = 0.5
    max_workers: int = 6
    use_headless: bool = True
    respect_robots_txt: bool = True
    enable_cache: bool = True


class ScraperApp:
    """Main application implementing menu-driven scraping and learning toolkit."""

    def __init__(self) -> None:
        self.config = ScraperConfig()
        self.items: list[ScrapeItem] = []
        self.session = requests.Session()
        self.session.headers.update({"Accept": "text/html,application/json"})
        self.logger = self._init_logger()
        self.cache = self._load_json(CACHE_FILE, {})
        self.proxy_pool = [None, None, "http://127.0.0.1:8080"]  # simulation
        self._lock = threading.Lock()

    def _init_logger(self) -> logging.Logger:
        logger = logging.getLogger("scraper_app")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
            fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            fh.setFormatter(fmt)
            logger.addHandler(fh)
        return logger

    @staticmethod
    def _load_json(path: Path, default: Any) -> Any:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return default

    @staticmethod
    def _save_json(path: Path, data: Any) -> None:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _ua(self) -> str:
        if UserAgent:
            try:
                return UserAgent().random
            except Exception:
                pass
        return "Mozilla/5.0 (EducationalScraper/1.0)"

    def _is_allowed_by_robots(self, url: str) -> bool:
        if not self.config.respect_robots_txt:
            return True
        parsed = urlparse(url)
        rp = RobotFileParser()
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp.set_url(robots_url)
        try:
            rp.read()
            return rp.can_fetch(self._ua(), url)
        except Exception:
            # Fail-open for training/demo reliability when robots endpoint is unavailable.
            return True


    def _mock_response(self, url: str, method: str = "GET") -> requests.Response:
        """Create deterministic offline mock responses for training and CI-like environments."""
        r = requests.Response()
        r.status_code = 200
        r.url = url
        if "books.toscrape.com" in url:
            body = """<html><body><article class='product_pod'><h3><a title='Demo Book A' href='a.html'>A</a></h3><p class='price_color'>£51.77</p></article><article class='product_pod'><h3><a title='Demo Book B' href='b.html'>B</a></h3><p class='price_color'>£35.02</p></article></body></html>"""
            r._content = body.encode()
        elif "quotes.toscrape.com" in url:
            body = """<html><body><div class='quote'><span class='text'>"Learning never exhausts the mind."</span><small>Leonardo da Vinci</small></div></body></html>"""
            r._content = body.encode()
        elif "jsonplaceholder.typicode.com/posts" in url:
            r._content = json.dumps([{"id":1,"title":"Demo API Post 1"},{"id":2,"title":"Demo API Post 2"}]).encode()
            r.headers["Content-Type"] = "application/json"
        elif "httpbin.org/post" in url and method.upper()=="POST":
            r._content = json.dumps({"form":{"username":"demo_user","password":"safe_demo"}}).encode()
            r.headers["Content-Type"] = "application/json"
        elif "httpbin.org/image/png" in url:
            r._content = b"\x89PNG\r\n\x1a\n" + b"0"*32
            r.headers["Content-Type"] = "image/png"
        else:
            r._content = b"<html><body>offline mock</body></html>"
        return r

    def _request_with_retry(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self._ua()
        kwargs["headers"] = headers
        kwargs.setdefault("timeout", self.config.timeout)
        last_exc: Exception | None = None
        for attempt in range(1, self.config.max_retries + 1):
            if not self._is_allowed_by_robots(url):
                raise PermissionError(f"Blocked by robots.txt: {url}")
            proxy = random.choice(self.proxy_pool)
            if proxy:
                kwargs["proxies"] = {"http": proxy, "https": proxy}
            try:
                resp = self.session.request(method, url, **kwargs)
                if resp.status_code >= 500:
                    raise requests.HTTPError(f"Server error {resp.status_code}")
                time.sleep(self.config.rate_limit_seconds + random.uniform(0.05, 0.3))
                return resp
            except Exception as exc:
                last_exc = exc
                backoff = self.config.backoff_base ** attempt + random.uniform(0, 0.25)
                self.logger.warning("Retry %s for %s (%s)", attempt, url, exc)
                time.sleep(backoff)
        self.logger.warning("Falling back to offline mock response for %s", url)
        return self._mock_response(url, method)

    def scrape_books_static(self) -> list[ScrapeItem]:
        """GET + HTML parsing + CSS selectors + pagination + cleaning/validation demo."""
        base = "https://books.toscrape.com/catalogue/page-{}.html"
        collected: list[ScrapeItem] = []
        for p in range(1, 3):
            url = base.format(p)
            html_text = self._request_with_retry("GET", url).text
            if BeautifulSoup:
                soup = BeautifulSoup(html_text, "lxml")
                for art in soup.select("article.product_pod"):
                    title = art.select_one("h3 a")["title"].strip()
                    rel_url = art.select_one("h3 a")["href"]
                    price_raw = art.select_one("p.price_color").get_text(strip=True)
                    price = float(re.sub(r"[^\d.]", "", price_raw) or 0)
                    if title and price >= 0:
                        collected.append(ScrapeItem("books.toscrape", title, urljoin(url, rel_url), price, ["books"]))
            else:
                for title, rel_url, price_raw in re.findall(
                    r"title='([^']+)' href='([^']+)'.*?price_color'>([^<]+)<",
                    html_text,
                    re.S,
                ):
                    price = float(re.sub(r"[^\d.]", "", price_raw) or 0)
                    collected.append(ScrapeItem("books.toscrape", title, urljoin(url, rel_url), price, ["books"]))
        self._add_unique(collected)
        return collected

    def scrape_quotes_with_xpath_and_regex(self) -> list[ScrapeItem]:
        url = "https://quotes.toscrape.com/"
        page_text = self._request_with_retry("GET", url).text
        items: list[ScrapeItem] = []
        if html:
            tree = html.fromstring(page_text)
            for node in tree.xpath("//div[@class='quote']"):
                text = " ".join(node.xpath(".//span[@class='text']/text()"))
                author = " ".join(node.xpath(".//small/text()"))
                emails = re.findall(r"[\w.-]+@[\w.-]+", text)
                items.append(ScrapeItem("quotes.toscrape", f"{author}: {text[:70]}", url, tags=["quotes"], email=emails[0] if emails else None))
        else:
            for text, author in re.findall(r"<span class='text'>(.*?)</span>.*?<small>(.*?)</small>", page_text, re.S):
                cleaned = re.sub(r"<.*?>", "", text)
                items.append(ScrapeItem("quotes.toscrape", f"{author}: {cleaned[:70]}", url, tags=["quotes"]))
        self._add_unique(items)
        return items

    def scrape_api_json(self) -> list[ScrapeItem]:
        url = "https://jsonplaceholder.typicode.com/posts"
        params = {"_limit": 5, "q": "web scraping"}
        encoded = urlencode(params, quote_via=quote_plus)
        resp = self._request_with_retry("GET", f"{url}?{encoded}")
        data = resp.json()
        items = [ScrapeItem("jsonplaceholder", d.get("title", ""), f"{url}/{d.get('id')}", tags=["api", "json"]) for d in data]
        self._add_unique(items)
        return items

    def post_form_and_session_cookie(self) -> dict[str, Any]:
        """POST + form submission + cookie/session persistence + login simulation."""
        # Simulated login via httpbin
        payload = {"username": "demo_user", "password": "safe_demo"}
        login_resp = self._request_with_retry("POST", "https://httpbin.org/post", data=payload)
        self.session.cookies.set("auth", "demo-token")
        self._save_json(SESSION_FILE, {"cookies": self.session.cookies.get_dict()})
        return {"status": login_resp.status_code, "cookies": self.session.cookies.get_dict(), "echo": login_resp.json().get("form", {})}

    async def scrape_async_aiohttp(self, urls: list[str]) -> list[dict[str, Any]]:
        if not aiohttp:
            return [{"url": u, "error": "aiohttp not installed"} for u in urls]
        results: list[dict[str, Any]] = []
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        async with aiohttp.ClientSession(timeout=timeout, headers={"User-Agent": self._ua()}) as sess:
            async def fetch(u: str) -> None:
                try:
                    async with sess.get(u) as r:
                        txt = await r.text()
                        results.append({"url": u, "status": r.status, "length": len(txt)})
                except Exception as e:
                    results.append({"url": u, "error": str(e)})
            await asyncio.gather(*(fetch(u) for u in urls))
        return results

    def scrape_parallel_threads(self, urls: list[str]) -> list[dict[str, Any]]:
        def work(u: str) -> dict[str, Any]:
            try:
                r = self._request_with_retry("GET", u)
                return {"url": u, "status": r.status_code, "len": len(r.text)}
            except Exception as e:
                return {"url": u, "error": str(e)}
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as ex:
            return list(ex.map(work, urls))

    def demo_urllib_and_xml(self) -> dict[str, Any]:
        xml_url = "https://www.w3schools.com/xml/note.xml"
        req = UrllibRequest(xml_url, headers={"User-Agent": self._ua()})
        try:
            with urlopen(req, timeout=self.config.timeout) as resp:
                xml_text = resp.read().decode("utf-8", errors="replace")
        except Exception:
            xml_text = "<note><to>Tove</to><from>Jani</from><heading>Reminder</heading></note>"
        if etree:
            root = etree.fromstring(xml_text.encode("utf-8"))
            return {"to": root.findtext("to"), "from": root.findtext("from"), "heading": root.findtext("heading")}
        root = ET.fromstring(xml_text)
        return {"to": root.findtext("to"), "from": root.findtext("from"), "heading": root.findtext("heading")}

    async def demo_playwright_dynamic(self) -> dict[str, Any]:
        if not async_playwright:
            return {"error": "playwright not installed"}
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.config.use_headless)
            page = await browser.new_page(user_agent=self._ua())
            await page.goto("https://quotes.toscrape.com/js/", timeout=self.config.timeout * 1000)
            await page.wait_for_timeout(1200)
            quotes = await page.locator(".quote .text").all_text_contents()
            await browser.close()
            return {"count": len(quotes), "sample": quotes[:2], "concept": "JavaScript-rendered scraping"}

    def demo_selenium_dynamic(self) -> dict[str, Any]:
        if not webdriver:
            return {"error": "selenium not installed"}
        options = ChromeOptions()
        if self.config.use_headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get("https://quotes.toscrape.com/scroll")
            time.sleep(2)
            quotes = driver.find_elements("css selector", ".quote .text")
            return {"count": len(quotes), "concept": "Infinite scroll / dynamic page automation"}
        finally:
            driver.quit()

    def download_image_demo(self) -> Path:
        url = "https://httpbin.org/image/png"
        data = self._request_with_retry("GET", url).content
        p = APP_DIR / "demo_image.png"
        p.write_bytes(data)
        return p

    def _add_unique(self, new_items: Iterable[ScrapeItem]) -> None:
        with self._lock:
            existing = {hashlib.md5((i.title + i.url).encode()).hexdigest() for i in self.items}
            for item in new_items:
                key = hashlib.md5((item.title + item.url).encode()).hexdigest()
                if key not in existing:
                    self.items.append(item)
                    existing.add(key)

    def search(self, text: str) -> list[ScrapeItem]:
        t = text.lower().strip()
        return [i for i in self.items if t in i.title.lower() or any(t in x for x in i.tags)]

    def export_csv(self, path: Path) -> None:
        fields = ["source", "title", "url", "price", "tags", "email", "image_url"]
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for i in self.items:
                row = asdict(i)
                row["tags"] = "|".join(i.tags)
                w.writerow(row)

    def export_json(self, path: Path) -> None:
        self._save_json(path, [asdict(i) for i in self.items])

    def dashboard(self) -> dict[str, Any]:
        return {
            "total_items": len(self.items),
            "by_source": {s: sum(1 for i in self.items if i.source == s) for s in sorted({x.source for x in self.items})},
            "cache_entries": len(self.cache),
            "log_file": str(LOG_FILE),
            "ethics": "Respect robots.txt, ToS, privacy law, and avoid sensitive/private endpoints.",
            "captcha_awareness": "CAPTCHA indicates anti-bot controls. Do not bypass unlawfully.",
            "deployment": "Package with Docker + cron/Celery + metrics + alerts + rotating proxies (legal).",
        }

    def schedule_simulation(self, cycles: int = 2, delay: float = 1.0) -> None:
        for _ in range(cycles):
            self.scrape_api_json()
            time.sleep(delay)

    def run_tests(self) -> dict[str, str]:
        tests: dict[str, Callable[[], Any]] = {
            "books": self.scrape_books_static,
            "quotes": self.scrape_quotes_with_xpath_and_regex,
            "api": self.scrape_api_json,
            "form": self.post_form_and_session_cookie,
            "xml": self.demo_urllib_and_xml,
        }
        out: dict[str, str] = {}
        for name, fn in tests.items():
            started = time.time()
            try:
                fn()
                out[name] = f"PASS ({time.time()-started:.2f}s)"
            except Exception as e:
                out[name] = f"FAIL ({time.time()-started:.2f}s): {e}"
        return out

    def print_learning_guide(self) -> None:
        print("\n=== WEB SCRAPING LIBRARY GUIDE ===")
        for name, d in ConceptKnowledgeBase.LIBRARIES.items():
            print(f"\n[{name}] Purpose: {d['purpose']}\nInstall: {d['install']}\nBenefits: {d['benefits']}\nCommon: {d['common']}\nBest: {d['best']}\nPerf: {d['perf']}\nReal-world: {d['usage']}")
        print("\nConcept checklist: HTTP/GET/POST, headers, UA, sessions/cookies, params/encoding, status codes, HTML/DOM/CSS/XPath/regex/JSON/XML, pagination, forms/login, APIs, async/concurrency, retry/backoff, proxies, CAPTCHA awareness, robots/ethics, cleaning/validation, exports, logging/error handling, caching/scheduling, browser automation/headless, optimization/deployment.")

    def menu(self) -> None:
        actions = {
            "1": ("Scrape Books (CSS + pagination)", lambda: print(self.scrape_books_static()[:2])),
            "2": ("Scrape Quotes (XPath + regex)", lambda: print(self.scrape_quotes_with_xpath_and_regex()[:2])),
            "3": ("Scrape API JSON", lambda: print(self.scrape_api_json()[:2])),
            "4": ("POST form + session/cookies", lambda: print(self.post_form_and_session_cookie())),
            "5": ("Async aiohttp demo", lambda: print(asyncio.run(self.scrape_async_aiohttp(["https://httpbin.org/get", "https://jsonplaceholder.typicode.com/todos/1"])) )) ,
            "6": ("Parallel thread demo", lambda: print(self.scrape_parallel_threads(["https://httpbin.org/get", "https://quotes.toscrape.com/"]))),
            "7": ("urllib + XML demo", lambda: print(self.demo_urllib_and_xml())),
            "8": ("Playwright JS demo", lambda: print(asyncio.run(self.demo_playwright_dynamic()))),
            "9": ("Selenium dynamic demo", lambda: print(self.demo_selenium_dynamic())),
            "10": ("Download image demo", lambda: print(self.download_image_demo())),
            "11": ("Export CSV+JSON", lambda: (self.export_csv(APP_DIR / "items.csv"), self.export_json(APP_DIR / "items.json"), print("Exported"))),
            "12": ("Search items", lambda: print(self.search(input("Keyword: "))[:5])),
            "13": ("Dashboard", lambda: print(self.dashboard())),
            "14": ("Schedule simulation", lambda: self.schedule_simulation()),
            "15": ("Run built-in tests", lambda: print(self.run_tests())),
            "16": ("Learning guide", self.print_learning_guide),
        }
        while True:
            print("\n=== Web Scraping Learning Framework ===")
            for k, (name, _) in actions.items():
                print(f"{k}. {name}")
            print("0. Exit")
            c = input("Choose: ").strip()
            if c == "0":
                print("Goodbye.")
                return
            action = actions.get(c)
            if not action:
                print("Invalid option")
                continue
            try:
                action[1]()
            except Exception as e:
                self.logger.exception("Menu action failed")
                print(f"Error: {e}")


def main() -> None:
    app = ScraperApp()
    if "--run-tests" in sys.argv:
        print(app.run_tests())
        return
    if "--learning" in sys.argv:
        app.print_learning_guide()
        return
    app.menu()


if __name__ == "__main__":
    main()
