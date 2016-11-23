from urllib.request import urlopen
from bs4 import BeautifulSoup

urlhandler = urlopen("https://en.wikipedia.org/wiki/Sustainable_energy")
html = urlhandler.read()

crawler_file = open("1_webpage.txt","wb")
crawler_file.write(html)
crawler_file.close()
