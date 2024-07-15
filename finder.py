# Author: Erick Ruh Cardozo  (W1SD00M) - <erickruhcardozo98@gmail.com>
# Date: Jul 15, 2024 - 13:55 PM
# Description: This module attempts to find the last time an EIN appears in a donation.

from csv import reader as csv_reader
from auth import User, UserDecoder, login
from downloader import download_donations
from datetime import datetime
from dateutil.relativedelta import relativedelta
from os import rename
from json import load, JSONDecoder


EIN_SOUGHT = ''

with open('users.json') as f:
    users = load(f, cls=UserDecoder)


for user in users:
    if (session := login(user)) == False:
        print(f'Could not login user: {user.name}')
        continue

    date = datetime.today()

    while date.month != 1:
        if (filename := download_donations(session, date)) == False:
            print(f'Could not download donations of user "{user.name}" for the period {date}')
            continue

        new_filename = f'{user.name} - {filename}'
        rename(filename, new_filename)

        with open(new_filename) as f:
            found_dates = set()
            reader = csv_reader(f, delimiter=';')
            for row in reader:
                if reader.line_num < 3: # Skip headers
                    continue

                access_key = row[2]
                ein = access_key[6:20]
                formated_ein = f'{ein[:2]}.{ein[2:5]}.{ein[5:8]}/{ein[8:12]}-{ein[12:]}'

                if EIN_SOUGHT == formated_ein and row[3] not in found_dates:
                    found_dates.add(row[3])
                    print(f'FOUND DONATION FROM USER: {user.name}, IN: {row[3]}')

        date = date - relativedelta(months=1)

    print(f'Finished cycle for user: {user.name}')
