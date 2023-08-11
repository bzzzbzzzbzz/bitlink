import os
import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    header = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": url}
    user_url = 'https://api-ssl.bitly.com/v4/bitlinks'

    response = requests.post(user_url, headers=header, json=payload)
    response.raise_for_status()
    short_link = response.json().get('id')
    return short_link


def count_clicks(token, link):
    header = {"Authorization": f"Bearer {token}"}
    user_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'

    response = requests.get(user_url, headers=header)
    response.raise_for_status()
    total_clicks = response.json().get('total_clicks')
    return total_clicks


def is_bitlink(link, token):
    header = {"Authorization": f"Bearer {token}"}
    user_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(user_url, headers=header)
    return response.ok


def main():
    token = os.environ['TOKEN']
    url = input('Enter your url: ')
    try:
        if is_bitlink(url, token):
            total_clicks = count_clicks(token, url)
            print('Total clicks: ', total_clicks)
        else:
            short_link = shorten_link(token, url)
            print('Your link: ', short_link)
    except requests.exceptions.HTTPError as e:
        print('HTTP Error: ', e)


load_dotenv('data.env')

if __name__ == '__main__':
    main()
