
import requests
from bs4 import BeautifulSoup
all_url = 'http://www.mzitu.com/all/'
start_html = requests.get(all_url, headers=headers)   
Soup = BeautifulSoup(start_html.text, "lxml") 
