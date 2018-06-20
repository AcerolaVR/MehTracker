#! python3
# mehtracker.py - persistent program that texts the current Meh deal and price @ 00:01 daily

import time

import boto3
import bs4
import requests
import schedule

import APIKEYS

# poll the time to run the scraper when scheduled
def pollTime():
    schedule.every().day.at("00:01").do(scrapeMeh)

    while True:
        schedule.run_pending()
        time.sleep(15)  # wait one minute


# scrape the current Meh Deal and price and request a text to be sent
def scrapeMeh():
    # grab and parse the meh main page
    res = requests.get('http://www.meh.com')
    meh_soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #  h2 and button elements where the title and price reside
    h2_elems = meh_soup.select('h2')
    b_elems = meh_soup.select('button')
    # pull the correct strings and remove whitespace
    temp_price = b_elems[0].getText().strip().rsplit('\r', 1)
    item = h2_elems[0].getText().strip()
    price = temp_price[0]
    # send the message to a phone
    sendMessage(APIKEYS.MY_NUMBER, 'Today\'s Meh Deal is: ' + price + ' ' + item + ' www.meh.com')


# request AWS for a message to be sent
def sendMessage(phone_num, message):
    client = boto3.client(
        "sns",
        aws_access_key_id="AKIAJVSSG7WICWS63T3Q",
        aws_secret_access_key="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",
        region_name="us-east-1"
    )
    response = client.publish(
        PhoneNumber=phone_num,
        Message=message
    )
    print(response)

if __name__ == "__main__":
    scrapeMeh()
    pollTime()
