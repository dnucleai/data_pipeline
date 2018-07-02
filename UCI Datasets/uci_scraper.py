import bs4
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

old_url = "https://archive.ics.uci.edu/ml/"
url = """https://archive.ics.uci.edu/ml/datasets.html?format=&task=&att=&area=life&numAtt=&numIns=&type=&sort=nameUp&view=table"""

words = ["patient", "patients", "treatment", "medical", "health", "cancer", "illness", "Adolescent", "breast", "Breast", "wife", "lymphography"]

client = urlopen(url)
page = client.read()
client.close()

def page_parser(url):
    page = html_page(url)
    text = page.get_text()
    textWords = text.split()
    topic = False
    for word in words:
        if word in textWords:
            topic = True

    if (topic):
        download_pages = parse_page(page)
    
    else:
        return False

def parse_page(page):
    outer_table = page.find("table", {"width" : "100%", "border" : "0", "cellpadding" : "2"})
    table = outer_table
    link = table.find_all("a")[0]['href'][3:]
    path = old_url + link
    download_page = html_page(path)
    table = download_page.body.table
    links = table.find_all("a")
    print(links)
    for link in links:
        if (link):
            href = link['href']
            if (href.endswith('.data') or href.endswith('.names') or href.endswith('.xls')):
                urllib.request.urlretrieve(path + "/" + href, href)
                
    pass

def get_urls(url):
    page = html_page(url)
    outer_table = page.find("table", {"cellpadding" : "3"})
    table = outer_table.find_all("table", {"border" : "1", "cellpadding" : "5"})[0]
    links = []
    for member in table:
        additional_link = member.find_all("a")[0]['href']
        links.append(old_url + additional_link)
    links = links[1:]
    return links

def html_page(url):
    client = urlopen(url)
    page = client.read()
    client.close()
    return soup(page, "html.parser")

links = get_urls(url)
for link in links:
    page_parser(link)
