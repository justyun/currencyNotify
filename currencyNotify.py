# -*- coding: utf-8 -*-

# Usage:
# python currencyNotify.py numberToSend(required) currencyNames(optional) repeatInterval(optional)

import sys
import requests
import json
import time
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

class CurrencyNotify(object):
    BASE_URL = 'http://www.google.ca/finance?q='
    DEFAULT_REQUEST = 'CADCNY'

    # SMS SID and Token info
    # You will need to have to sign up you own (free) twilio account and fill the info
    ACCOUNT_SID = ''
    AUTH_TOKEN = ''

    def notify(self, phoneNumber, equest = None):
        exchangeRate = self.get_exchange_rate(request)
        self.send_sms(exchangeRate, phoneNumber)

    def get_exchange_rate(self, request = None):
        try:
            if request is None:
                requestUrl = self.BASE_URL + self.DEFAULT_REQUEST;
            else:
                requestUrl = self.BASE_URL + request
            raw_page = requests.get(requestUrl)
            page = BeautifulSoup(raw_page.text, 'html.parser')
            exchangeRate = page.findAll('span', {'class': 'bld'})[0].contents[0]
            print exchangeRate
            return exchangeRate
        except Exception as e:
            print 'An issue happended: ', e

    def send_sms(self, exchangeRate, phoneNumber):
        client = TwilioRestClient(self.ACCOUNT_SID, self.AUTH_TOKEN)

        client.messages.create(
            to=phoneNumber,
            from_='', # You will need to have to sign up you own (free) twilio account and fill the info
            body=exchangeRate,
        )


if __name__ == '__main__':
    currencyNotify = CurrencyNotify()
    request = None
    phoneNumber = sys.argv[1]
    if len(sys.argv) >= 3:
        request = sys.argv[2]
    if len(sys.argv) >= 4:
        interval = int(sys.argv[3])
        while True:
            currencyNotify.notify(phoneNumber, request)
            time.sleep(interval)
    else:
        currencyNotify.notify(phoneNumber, request)
