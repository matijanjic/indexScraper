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
# and add the title-link pair to the articles dictionary. So at this point, the dictionary is filled with current articles,
# which will be useful for checking if there are new ones
    if title != None and "/tag/" not in link:
        linkStr = "".join(link)            
        articles[linkStr] = title.text

# need to add a normal way of stopping the program. Maybe via e-mail so it can be stopped remotely?
# while True loop that checks every 10 seconds to see if any new articles are published. If there are, send them via e-mail
for k, v in articles.items():
    print(k + "\n" + v)

while True:
        container = response.html.find(".main-category-holder", first = True)
        links = container.find("a")
        for link in links:
            title = link.find(".title", first = True)
            link = link.absolute_links
            if title != None and "/tag/" not in link:
                linkStr = "".join(link)

                if linkStr not in articles.keys():
                    print(linkStr + "\n" + title.text)
        time.sleep(10)       
                







            

