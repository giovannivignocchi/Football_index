#!/usr/bin/python3

import requests
import csv
import time
import datetime

now = datetime.datetime.now()
file_name = str(now.year) + '_' + str(now.month) + '_' + 'price.csv'


# Check if in the folder where the scraper is located is already present a file that records prices
# If it is not the case, it create a new file and write the header
try:
    f = open('/home/ec2-user/Football_index/price/'+file_name)
    f.close()
except FileNotFoundError:
    with open('/home/ec2-user/Football_index/price/'+file_name, mode='w') as csv_file:
        fieldnames = ['player', 'date', 'buy', 'sell']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

# Append to the csv file the new scraped data
with open('/home/ec2-user/Football_index/price/'+file_name, mode='a') as csv_file:
    writer = csv.writer(csv_file)

    scraping_time = time.time()
    fetched_data = 1
    page = 1

    while(fetched_data):

        fetched_data = 0

        xhr_url = 'https://api-prod.footballindex.co.uk/football.allTradable24hrchanges?page=' + str(page) + '&per_page=50&sort=asc'

        resp = requests.get(xhr_url)

        data = resp.json()

        for player in data['items']:

            fetched_data = fetched_data + 1

            player_id = player['optaid']
            buy_price = player['score']
            sell_price = player['scoreSell']

            writer.writerow([player_id, scraping_time, buy_price, sell_price])

        page = page + 1
