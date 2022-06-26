import requests
from bs4 import BeautifulSoup


def findtags(document, tree, attributes=None, count=None):
    # if there are no attributes, create an empty list of dicts:
    if attributes == None:
        attributes = [{} for _ in range(len(tree))]

    # if there are no search counts, generate default:
    if count == None:
        # count of 0 means find all:
        count = [0 for _ in range(len(tree))]

    # subpage is a list of all parts of the page with tags found
    # to search again:
    subpage = [BeautifulSoup(document, features='lxml')]

    for i, tag in enumerate(tree):
        for item in subpage:
            # found objs is for the next iteration:
            found_objs = []

            if count[i] == 1:
                # perf optimisation, only find 1
                found_objs.append(item.find(tag, attrs=attributes[i]))
            else:
                # find multiple
                for j, obj in enumerate(item.find_all(tag, attrs=attributes[i])):
                    found_objs.append(obj)

                    # limit the list if a limit was specified:
                    if count[i] > 1 and count[i] == j+1:
                        break

        subpage = found_objs

    return subpage


def scrapeurl(location, tree, attributes=None, count=None):
    page = requests.get(location)
    if page.status_code == 200:
        return findtags(page.content, tree, attributes, count)
    else:
        return []


def scrapefile(location, tree, attributes=None, count=None):
    with open(location) as page:
        return findtags(page, tree, attributes, count)


def getwebpage(URL):
    page = requests.get(URL)
    return str(page.text)
