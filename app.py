from flask import Flask
from rhino3dm import *
import ghhops_server as hs
import time
import requests
from bs4 import BeautifulSoup


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
    "/scraper",
    name="Web Scraper",
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
def scrape(location, tree):
    #location = 'https://example.com'
    #tree = ['p']

    page = requests.get(location)

    if page.status_code == 200:
        subpage = [BeautifulSoup(page.content, features='lxml')]

        for tag in tree:
            for item in subpage:
                # found objs is for the next iteration
                found_objs = []
                for obj in item.find_all(tag):
                    found_objs.append(obj)
                #print('FOUND OBJS ::::: ', found_objs)
            subpage = found_objs

        # this took ages to debug... turns out the items weren't strings
        result = [str(item) for item in subpage]

        return result
    else:
        return [f'Could not connect to {location}']


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
