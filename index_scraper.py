import time
import datetime
from requests_html import HTMLSession
import smtplib, ssl
from imbox import Imbox

session = HTMLSession()

port = 465  # For SSL

# e-mail info for the bot - need to hide the password eventually, this is just for the testing purposes
password = "indexbot123"
sender_email = "botzaindex@gmail.com"
receiver_email = "matijanjic@gmail.com"


# Create a secure SSL context
context = ssl.create_default_context()

# empty dictionary that will hold the article links and titles
articles = {}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
# main url of the web to scrape
url = 'https://www.index.hr'
response = session.get(url, headers = headers)

# returns the first container with the css class of main-category-holder
container = response.html.find(".main-category-holder", first = True)

container2 = response.html.find("#tab-content-latest-vijesti", first = True)

# find all 'a' elements inside
links = container.find("a")
links2 = container2.find(".vijesti-text-hover")

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

for link in links2:
    title = link.text
    link = link.absolute_links
    linkStr = "".join(link)            
    articles[linkStr] = title

for k, v in articles.items():
    print(k + "\n" + v)

# while True loop that checks every 10 seconds to see if any new articles are published. If there are, send them via e-mail
index = 0
while True:
    # go through all the articles again, check if there are new ones. If there are, add them to the dictionary and send them via email.
    # sleep for 30 seconds, then do it all over again
        response = session.get(url, headers = headers)
        container = response.html.find(".main-category-holder", first = True)
        links = container.find("a")
        for link in links:
            title = link.find(".title", first = True)
            link = link.absolute_links
            if title != None and "/tag/" not in link:
                linkStr = "".join(link)
                if linkStr not in articles.keys():
                    timestamp = datetime.datetime.now()            
                    dateTime = timestamp.strftime("%x %X")
                    message = "Subject: No. " + str(index) + ": " + title.text[:70] + "\n\n" + dateTime + "\n" + title.text + "\n" + linkStr
                    print(message)
                    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                        server.login("botzaindex@gmail.com", password)
                        server.sendmail(sender_email, receiver_email, message.encode("utf8"))
                    index += 1
                    articles[linkStr] = title.text
        
        # add the ability to stop the program remotely via email containing the word stop
        with Imbox('imap.gmail.com',
        username='botzaindex@gmail.com',
        password = password,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

            messages = imbox.messages(unread = True, sent_from = receiver_email)
            for uid, message in messages:
                
                if 'STOP' in str(message.body['plain']).upper():
                    imbox.mark_seen(uid)
                    exit()
                    
        time.sleep(30)       
                







            

