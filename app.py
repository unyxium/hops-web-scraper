from flask import Flask
#from rhino3dm import *
import ghhops_server as hs
import time
import requests
from bs4 import BeautifulSoup
import scraper

app = Flask(__name__)
hops = hs.Hops(app)


@hops.component(
    "/info",
    name="Info",
    description="Basic info",
    icon="icons/star.png",
    inputs=[],
    outputs=[
        hs.HopsInteger("Time", "T", "Current time for version tracking"),
        hs.HopsString("Author", "A", "Author")
    ]
)
def info():
    return round(time.time()), 'unyxium'


# DEPRECATE THE DEDICATED URL VERSION
@hops.component(
    "/scrapeurl",
    name="Scrape URL",
    description="Scrape a webpage for data",
    icon="icons/star.png",
    inputs=[
        hs.HopsString("URL", "U", "Webpage URL"),
        hs.HopsString("Elements", "E", "List of targeted elements in order",
                      access="HopsParamAccess.TREE")
    ],
    outputs=[
        hs.HopsString("Output", "O", "Output data")
    ]
)
def ghscrape(location, tree):
    result = scraper.scrapeurl(location, tree)
    return [str(item) for item in result]


@hops.component(
    "/scrapedoc",
    name="Scrape Document",
    description="Scrape a document for data",
    icon="icons/star.png",
    inputs=[
        hs.HopsString("Document", "D", "Document at a single object"),
        hs.HopsString("Elements", "E", "List of targeted elements in order",
                      access="HopsParamAccess.TREE"),
        hs.HopsString("Attributes", "A", "List of attributes to filter elements",
                      access="HopsParamAccess.TREE",
                      optional=True, default=None)
    ],
    outputs=[
        hs.HopsString("Output", "O", "Output data")
    ]
)
def ghscrapedoc(document, tree, attributes):
    import json
    attrdicts = [json.loads(attr) for attr in attributes]
    if not len(attrdicts) == len(tree):
        return 'Attribute length mismatch'

    result = scraper.findtags(document, tree, attrdicts)
    return [str(item) for item in result]


@hops.component(
    "/test",
    name="TEST",
    description="Testing",
    icon="icons/star.png",
    inputs=[
        hs.HopsString("Input", "I", "Input values")
    ],
    outputs=[
        hs.HopsString("Output", "O", "Output values")
    ]
)
def testing(i):
    return i
