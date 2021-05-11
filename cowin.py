#!/usr/bin/python3
import json
import requests
from datetime import datetime

PINCODES = ['600096', '600041']


headers = {'Content-Type': 'application/json',
           'Accept-Language': 'hi_IN',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
           }


def parse_vaccination_center(response):

    if 'centers' not in response:
        print("No vaccine centers")

    for center in response['centers']:
        name = center['name']
        service = center['fee_type']

        for session in center['sessions']:
            session_date = session['date']
            availability = session['available_capacity']
            vaccine = session['vaccine']
            age_limit = session['min_age_limit']

            print(session_date)
            print(vaccine)
            print(availability)

            if availability > 0:
                print("Vaccine available ")
            else:
                print("Vaccine Not available")

def get_cowin_data(url):
    response = requests.get(url, headers=headers)
    #print(response.text)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def check_availability_pincode(pincode):
    """

    :param pincode:
    :return: None
    """

    API_BASE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    QUERY_STRING = "?pincode=%s&date=%s"

    today = datetime.now().strftime('%d-%m-%Y')
    print(today)

    FULL_URL = API_BASE_URL + QUERY_STRING %(pincode, today)
    print(FULL_URL)

    response = get_cowin_data(FULL_URL)
    #print(response)

    parse_vaccination_center(response)


if __name__ == "__main__":

    for pin in PINCODES:
        print("Checking for ", pin)
        check_availability_pincode(pin)
