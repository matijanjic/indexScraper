import time
import datetime
from requests_html import HTMLSession
import smtplib
import ssl
from imbox import Imbox
import re

# e-mail info for the bot - need to hide the password eventually, this is just for the testing purposes
password = "indexbot123"
sender_email = "botzaindex@gmail.com"
receiver_email = "matijanjic@gmail.com"

# For SSL
port = 465
# Create a secure SSL context
context = ssl.create_default_context()


def sendEmail(index, title, link):

    timestamp = datetime.datetime.now()
    dateTime = timestamp.strftime("%x %X")
    message = "Subject: No. " + \
        str(index) + ": " + title[:70] + "\n\n" + \
        dateTime + "\n" + title + "\n" + link
    print(message)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("botzaindex@gmail.com", password)
        server.sendmail(
            sender_email, receiver_email, message.encode("utf8"))

def main():

    # empty dictionary that will hold the article links(k) and titles(v)
    articles = {}

    # select the categories on the Index.hr page - 0 is news, 1 is sports and 2 is lifestyle
    categories = [0]
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    # main url of the web to scrape
    url = 'https://www.index.hr'
    session = HTMLSession()
    response = session.get(url, headers=headers)

    # returns the container with the class .main-category-holder depending on the index - 0 for news, 1 for sports and 2 for lifestyle
    for category in categories:
        container = response.html.find(".main-category-holder")[category]
        # finds the 'a' element and finds the title and link within them, rejecting any link that has /tag/ inside
        links = container.find("a")
        for link in links:
            title = link.find(".title", first=True)
            link = link.absolute_links
            if title != None and "/tag/" not in link:
                linkStr = "".join(link)
                pattern = '_\w\w\w=\d{6}'
                replace = ''
                linkStr = re.sub(pattern, replace, linkStr)
                # after that, link and title are added to the articles dictionary
                articles[linkStr] = title.text

    # same as above but for the side menu, so it's a bit different since the targeting
    # is with the class and id, and the text is between the <a> tags.
    for i in categories:  # 0 for news, 1 for sports and 2 for lifestyle
        if i == 0:
            artId = "#tab-content-latest-vijesti"
            artClass = ".vijesti-text-hover"
        elif i == 1:
            artId == "#tab-content-latest-sport"
            artClass = ".sport-text-hover"
        else:
            artId == "#tab-content-latest-magazin"
            artClass = ".magazin-text-hover"

        container = response.html.find(artId, first=True)
        links = container.find(artClass)
        for link in links:
            title = link.text
            link = link.absolute_links
            linkStr = "".join(link)
            pattern = '_\w\w\w=\d{6}'
            replace = ''
            linkStr = re.sub(pattern, replace, linkStr)
            # doesn't have the .text method as above since it already is a string type
            articles[linkStr] = title

    for k, v in articles.items():
        print(k + "\n" + v)

    # while True loop that checks every 10 seconds to see if any new articles are published. If there are, send them via e-mail
    index = 0
    while True:
        # go through all the articles again, check if there are new ones. If there are, add them to the dictionary and send them via email.
        # sleep for 30 seconds, then do it all over again
        response = session.get(url, headers=headers)
        for category in categories:
            container = response.html.find(".main-category-holder")[category]
            links = container.find("a")
            for link in links:
                title = link.find(".title", first=True)
                link = link.absolute_links
                if title != None and "/tag/" not in link:
                    linkStr = "".join(link)
                    pattern = '_\w\w\w=\d{6}'
                    replace = ''
                    linkStr = re.sub(pattern, replace, linkStr)
                    if linkStr not in articles.keys():
                        articles[linkStr] = title.text
                        sendEmail(index, title.text, linkStr)
                        index += 1

        # checks the side container
        for category in categories:  # 0 for the news, 1 for sports and 2 for lifestyle
            if category == 0:
                artId = "#tab-content-latest-vijesti"
                artClass = ".vijesti-text-hover"
            elif category == 1:
                artId == "#tab-content-latest-sport"
                artClass = ".sport-text-hover"
            else:
                artId == "#tab-content-latest-magazin"
                artClass = ".magazin-text-hover"

            container = response.html.find(artId, first=True)
            links = container.find(artClass)
            for link in links:
                title = link.text
                link = link.absolute_links
                linkStr = "".join(link)
                pattern = '_\w\w\w=\d{6}'
                replace = ''
                linkStr = re.sub(pattern, replace, linkStr)
                if linkStr not in articles.keys():
                    articles[linkStr] = title
                    sendEmail(index, title, linkStr)
                    index += 1

        # add the option to stop the program remotely via email containing the word stop
        with Imbox('imap.gmail.com',
                   username='botzaindex@gmail.com',
                   password=password,
                   ssl=True,
                   ssl_context=None,
                   starttls=False) as imbox:

            messages = imbox.messages(unread=True, sent_from=receiver_email)
            for uid, message in messages:

                if 'STOP' in str(message.body['plain']).upper():
                    imbox.mark_seen(uid)
                    exit()

        time.sleep(30)


if __name__ == '__main__':
    main()
