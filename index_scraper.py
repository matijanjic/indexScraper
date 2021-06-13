import time
import datetime
from requests_html import HTMLSession
import smtplib, ssl

session = HTMLSession()

port = 465  # For SSL
password = "botzaindex123"
sender_email = "botzaindex@gmail.com"
receiver_email = "matijanjic@gmail.com"


# Create a secure SSL context
context = ssl.create_default_context()
articles = {}
url = 'https://www.index.hr'
response = session.get(url)
container = response.html.find(".main-category-holder", first = True)
links = container.find("a")
for link in links:
    title = link.find(".title", first = True)
    link = link.absolute_links
    
    if title != None:
        if "/tag/" not in link:
            linkStr = "".join(link)
            print(link)
            print(title.text)
            articles[linkStr] = title.text
    


articleList = []




            

