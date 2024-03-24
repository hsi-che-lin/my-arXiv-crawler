import requests
import json
from bs4 import BeautifulSoup

from rater import rater

def refineURL(url):
    with requests.get(url) as resp:
        soup = BeautifulSoup(resp.text, "html.parser")
    
    text = soup.find("h3").string
    totalEntries = text.split(" ")[-2]
    newURL = url.replace("show=25", f"show={totalEntries}")

    return newURL


def crawlPapers(url, rater):
    url = refineURL(url)

    with requests.get(url) as resp:
        soup = BeautifulSoup(resp.text, "html.parser")
    
    paperIDs = soup.find_all("a", title = "Abstract")
    paperInfos = soup.find_all("dd")
    results = []
    stat = {}

    for (paperID, paperInfo) in zip(paperIDs, paperInfos):
        paperID = paperID.string.replace("arXiv:", "")
        title = paperInfo.findChild("div", class_ = "list-title mathjax").text.replace("Title:", "").strip()
        rating, keywords = rater(paperInfo)
        stat[rating] = stat.get(rating, 0) + 1
        results.append({
            "paper id": paperID,
            "abstract url": "https://arxiv.org/abs/" + paperID,
            "title": title,
            "rating": rating,
            "keywords": keywords
        })
    
    results = sorted(results, key = lambda x: (-x["rating"], x["paper id"]))
    tmp = [("total", len(paperIDs))] + [(k, v) for (k, v) in sorted(stat.items(), key = lambda x: -x[0])]
    stat = {
        k: v for (k, v) in tmp
    }

    return results, stat


def transformDate(date):
    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    
    parts = date.split(" ")
    newDate = parts[3] + months[parts[2]] + f"{parts[1]:0>2}"

    return newDate


if (__name__ == "__main__"):
    url = "https://arxiv.org/list/cs/pastweek?skip=0&show=25"

    with requests.get(url) as resp:
        soup = BeautifulSoup(resp.text, "html.parser")
        html = soup.prettify()
    
    with open("metadata.json", "r") as f:
        metadata = json.load(f)

    tags = soup.find_all("li", limit = 5)

    for tag in tags:
        tag = tag.findChild("a")
        date = transformDate(tag.string.strip())
        
        if (date not in metadata.keys()):
            href = "https://arxiv.org" + tag["href"]
            results, stat = crawlPapers(href, rater)
            metadata[date] = stat

            with open(f"results/{date}.json", "w") as f:
                json.dump(results, f, indent = 4)

    metadata = {
        k: v for (k, v) in sorted(metadata.items(), key = lambda x: -int(x[0]))
    }

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent = 4)
