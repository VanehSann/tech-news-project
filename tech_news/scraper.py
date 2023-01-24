import time

import requests
from parsel import Selector

from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, headers={"user-agent": "Fake user-agent"})
        time.sleep(1)
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    urls = selector.css("a.cs-overlay-link::attr(href)").getall()
    return urls


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    url = selector.css("a.next::attr(href)").get()
    return url


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("div.entry-header-inner h1.entry-title::text").get()
    title = "".join(title).strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a::text").get()
    comments_count = 0
    summary = selector.css(
        "div.entry-content > p:first-of-type *::text"
    ).getall()
    summary = "".join(summary).strip()
    tags = selector.css("section.post-tags a::text").getall()
    category = selector.css("a.category-style span.label::text").get()
    newsList = {
        "url": url,
        "title": title,
        "writer": writer,
        "summary": summary,
        "comments_count": comments_count,
        "timestamp": timestamp,
        "tags": tags,
        "category": category,
    }
    return newsList


# Requisito 5
def get_tech_news(amount):
    html_content = fetch("https://blog.betrybe.com/")
    urls = scrape_updates(html_content)
    while len(urls) < amount:
        url_next_page = scrape_next_page_link(html_content)
        html_content = fetch(url_next_page)
        urls.extend(scrape_updates(html_content))
    newsList = []
    for item in range(amount):
        html_content = fetch(urls[item])
        newsList.append(scrape_news(html_content))
    create_news(newsList)
    return newsList
