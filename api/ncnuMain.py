from api.tools import *
import requests
from bs4 import BeautifulSoup

class NcnuMain():
    def getAnno(self):
        response = requests.get('https://www.ncnu.edu.tw/ncnuweb/ann/tabs.aspx?homeType=ncnu&unit=ncnu')
        block = find(response, 'div', param={'id': 'annNews'})

        return [{
            'title': " ".join(anno.text.split(' ')[1:]),
            'link': "https://www.ncnu.edu.tw/ncnuweb/ann/" + anno.get('href')
        } for anno in block.findAll('a')]
