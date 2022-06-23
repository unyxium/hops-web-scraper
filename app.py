from flask import Flask, request
#from rhino3dm import *
import ghhops_server as hs
import time
import scraper
import re

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


@hops.component(
    "/getwebpage",
    name="Get Webpage",
    description="Download a webpage",
    icon="icons/star.png",
    inputs=[
        hs.HopsString("URL", "U", "Webpage URL"),
    ],
    outputs=[
        hs.HopsString("Page", "P", "Webpage")
    ]
)
def ghgwp(location):
    return scraper.getwebpage(location)


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
    "/striptags",
    name="Strip Tags",
    description="Strip tags from input and return plain text",
    icon="icons/star.png",
    inputs=[
        hs.HopsString("Input", "I", "Input text")
    ],
    outputs=[
        hs.HopsString("Output", "O", "Output text")
    ]
)
def striptags(document):
    return re.sub(pattern='<\/?.+?>', repl='', string=document)


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
def testing(input):
    return input


if __name__ == '__main__':
    app.run(debug=True)
