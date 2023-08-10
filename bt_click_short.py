import os

import requests
from urllib.parse import urlsplit
from dotenv import load_dotenv


def shorten_link(token, url):
    header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"long_url": url}
    user_url = 'https://api-ssl.bitly.com/v4/bitlinks'

    response = requests.post(user_url, headers=header, json=payload)
    response.raise_for_status()
    short_link = response.json().get('id')
    return short_link


def count_clicks(token, link):
    header = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    user_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'

    response = requests.get(user_url, headers=header)
    response.raise_for_status()
    total_clicks = response.json().get('total_clicks')
    return total_clicks


def is_bitlink(url, token):
    try:
        if 'bit.ly' in url:
            split_url = urlsplit(url)
            if split_url.scheme:
                url = split_url.netloc + split_url.path
            total_clicks = count_clicks(token, url)
            print('Total clicks :', total_clicks)
        else:
            short_link = shorten_link(token, url)
            print('Your link :', short_link)
    except requests.exceptions.HTTPError as e:
        print('HTTP Error: ', e)


def main():
    token = os.environ['ACCESS_TOKEN']
    url = input('Enter your url: ')
    is_bitlink(url, token)

load_dotenv('data.env')
main()
