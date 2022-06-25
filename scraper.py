import requests
from bs4 import BeautifulSoup


def findtags(document, tree, attributes=None):
    # if there are no attributes, create an empty list of dicts
    if attributes == None:
        attributes = [{} for _ in range(len(tree))]

    # subpage is a list of all parts of the page with tags found
    # to search again
    subpage = [BeautifulSoup(document, features='lxml')]

    for i, tag in enumerate(tree):
        for item in subpage:
            # found objs is for the next iteration
            found_objs = []
            for obj in item.find_all(tag, attrs=attributes[i]):
                found_objs.append(obj)
            #print('FOUND OBJS ::::: ', found_objs)
        subpage = found_objs

    return subpage


def scrapeurl(location, tree, attributes=None):
    page = requests.get(location)
    if page.status_code == 200:
        return findtags(page.content, tree, attributes)
    else:
        return []


def scrapefile(location, tree, attributes=None):
    with open(location) as page:
        return findtags(page, tree, attributes)


def getwebpage(URL):
    page = requests.get(URL)
    return str(page.content)
