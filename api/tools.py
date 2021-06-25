from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup

def getUrlParam(url, param):
    return parse_qs(
        urlparse(url).query
    )[param][0]

def findAll(response, tag, param=None):
    root = BeautifulSoup(response.text, 'html.parser')
    if param:
        return root.findAll(tag, param)
    else:
        return root.findAll(tag)

def find(response, tag, param=None):
    root = BeautifulSoup(response.text, 'html.parser')
    if param:
        return root.find(tag, param)
    else:
        return root.find(tag)
