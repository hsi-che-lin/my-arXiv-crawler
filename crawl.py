import argparse
import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from rater import rater


def getDates():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", "-s", type = str, default = None, required = False,
                        help = "start date, format: yyyy-mm-dd")
    parser.add_argument("--end", "-e", type = str, default = None, required = False,
                        help = "end date, format: yyyy-mm-dd or \"today\"")
    arg = parser.parse_args()
    dates = []
    fmt = lambda x: x.strftime("%Y-%m-%d")
    oneDay = timedelta(days = 1)

    if (arg.start != None):
        yStart, mStart, dStart = arg.start.split("-")
        start = datetime(int(yStart), int(mStart), int(dStart))

        if (arg.end == "today"):
            end = datetime.today()
        elif (arg.end != None):
            yEnd, mEnd, dEnd = arg.end.split("-")
            end = datetime(int(yEnd), int(mEnd), int(dEnd))
        else:
            end = start + oneDay
    else:
        start = datetime.today() - oneDay
        end = datetime.today()

    while (fmt(start) != fmt(end)):
        dates.append((fmt(start), fmt(start + oneDay)))
        start = start + oneDay

    return dates


def search(fromDate, toDate, searched):
    url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-computer_science=y&classification-eess=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={fromDate}&date-to_date={toDate}&date-date_type=submitted_date_first&abstracts=show&size=200&order=-announced_date_first&start={searched}"
    url = url.format(fromDate = fromDate, toDate = toDate, searched = searched)

    with requests.get(url) as resp:
        soup = BeautifulSoup(resp.text, "html.parser")
    
    total = soup.find("h1", class_ = "title is-clearfix")
    total = int(total.text.strip().split(" ")[-2])
    papers = soup.findAll("li", class_ = "arxiv-result")

    return total, papers


def parse(tag, rater):
    idTag = tag.findChild("p", class_ = "list-title is-inline-block").findChild("a")
    paperId = idTag.text.strip().replace("arXiv:", "")
    abstractUrl = idTag["href"]
    title = tag.findChild("p", class_ = "title is-5 mathjax").text.strip()
    subjectTags = tag.findChildren("span", class_ = "tag is-small is-link tooltip is-tooltip-top")
    subjects = [t.text.strip() for t in subjectTags]
    abstract = tag.findChild("span", class_ = "abstract-full has-text-grey-dark mathjax")
    abstract = " ".join(abstract.text.strip().split()).replace(" \u25b3 Less", "")
    comment = tag.findChild("span", class_ = "has-text-grey-dark mathjax")
    comment = None if (comment == None) else " ".join(comment.text.strip().split())
    rating, keywords = rater(title, subjects, abstract, comment)

    result = {
        "paper id": paperId,
        "abstract url": abstractUrl,
        "title": title,
        "rating": rating,
        "keywords": keywords,
        "abstract": abstract,
        "subjects": subjects,
        "comment": comment
    }

    return result


if (__name__ == "__main__"):
    dates = getDates()

    with open("metadata.json", "r") as f:
        metadata = json.load(f)

    for (fromDate, toDate) in dates:
        print(f"crawling papers from {fromDate} to {toDate}")
        results = []
        stat = {}
        total = 1
        searched = 0

        while (searched < total):
            total, papers = search(fromDate, toDate, searched)
            searched += len(papers)

            for paper in papers:
                result = parse(paper, rater)
                results.append(result)
                stat[result["rating"]] = stat.get(result["rating"], 0) + 1

        results = sorted(results, key = lambda x: (-x["rating"], x["paper id"]))
        tmp = [("total", total)] + [(k, v) for (k, v) in sorted(stat.items(), key = lambda x: -x[0])]
        metadata[fromDate] = dict(tmp)

        with open(f"results/{fromDate}.json", "w") as f:
            json.dump(results, f, indent = 4)

    metadata = {
        k: v for (k, v) in sorted(metadata.items(), key = lambda x: -int(x[0].replace("-", "")))
    }
    
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent = 4)
