from datetime import datetime

from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    news = search_news({"title": {"$regex": title, '$options': 'i'}})
    result = []
    for item in news:
        result.append((item["title"], item["url"]))
    return result


# Requisito 7
def search_by_date(date):
    try:
        date = datetime.fromisoformat(date).strftime("%d/%m/%Y")
        news = search_news({"timestamp": {"$regex": date}})
        result = []
        for item in news:
            result.append((item["title"], item["url"]))
        return result
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    news = search_news({"tags": {"$regex": tag, '$options': 'i'}})
    result = []
    for item in news:
        result.append((item["title"], item["url"]))
    return result


# Requisito 9
def search_by_category(category):
    news = search_news({"category": {"$regex": category, '$options': 'i'}})
    result = []
    for item in news:
        result.append((item["title"], item["url"]))
    return result
