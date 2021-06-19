# Index Scraper

Index scraper is a python program designed to scrape the index.hr webpage (Croatian news portal) and e-mail the user each time a new headline in the selected section (news, sports and lifestyle) is published. The recieved e-mail contains the headline and the link to the article. 

Why would somebody want something like that is beyond me, but it was good for practice.


## Motivation

I needed a project to learn web scraping and this seemed like a good one. I could test different libraries, use of Regex and (not implemented at the time of writing this readme) managing databases with SQLite.

## Dependencies
The main modules are Requests HTML and Imbox, but you can install all of the dependencies using
```bash
pip install -r requirements.txt
```

## Installation

Use the github clone feature

```bash
git clone https://github.com/matijanjic/indexScraper.git
```
For the next step it would be best if you had a new gmail account set up for the bot, for security reasons.

## Usage
Change the sender_e-mail to the bot account you created and the reciever_email to your e-mail
```python
# e-mail info for the bot
sender_email = "botzaindex@gmail.com"
receiver_email = "matijanjic@gmail.com"
```
Change the categories list variable to your liking - you can select up to 3 categories with 0 being news, 1 being sports and 2 being lifestyle. Don't try other numbers because I didn't catch the IndexError :D
```python
# select the categories on the Index.hr page - 0 is news, 1 is sports and 2 is lifestyle (for example [0, 2] for news and lifestyle)
categories = [0]
```

After you start the script, you will begin to receive e-mails. You can change the timeout between searches by editing the `time.sleep(30)` found at the end of main.

## Contributing
If you have an idea or a improvement I would be happy to cooperate. Pull requests or mail, both is fine.
