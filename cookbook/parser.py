import requests
from bs4 import BeautifulSoup

def wr_scrape():
    r = requests.get('https://www.apetitonline.cz/recept/chrestovy-quiche')
    soup = BeautifulSoup(r.text)

    wr_scrape()
