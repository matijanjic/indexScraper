import time
import datetime
from requests_html import HTMLSession
import smtplib, ssl

session = HTMLSession()

port = 465  # For SSL

# e-mail info for the bot - need to hide the password eventually, this is just for the testing purposes
password = "botzaindex123"
sender_email = "botzaindex@gmail.com"
receiver_email = "matijanjic@gmail.com"


# Create a secure SSL context
context = ssl.create_default_context()

# empty dictionary that will hold the article links and titles
articles = {}

# main url of the web to scrape
url = 'https://www.index.hr'
response = session.get(url)

# returns the first container with the css class of main-category-holder
container = response.html.find(".main-category-holder", first = True)

# find all 'a' elements inside
links = container.find("a")

# for each of the 'a' elements (since the find method returns a list) check the title and save it to a title variable, and find
# the exact link
for link in links:
    title = link.find(".title", first = True)
    link = link.absolute_links
# if a title exists and the link doesn't contain /tag/ string, convert the link from a set to a string using a .join method
# and add the title-link pair to the articles dictionary
    if title != None:
        if "/tag/" not in link:
            linkStr = "".join(link)
            print(linkStr)
            print(title.text)
            articles[linkStr] = title.text
for k, v in articles.items():
    print(k,v)    







            

