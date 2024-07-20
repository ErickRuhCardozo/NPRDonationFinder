# Author: Erick Ruh Cardozo  (W1SD00M) - <erickruhcardozo98@gmail.com>
# Date: Jul 15, 2024 - 13:55 PM
# Description: This module attempts to find the last time an EIN appears in a donation.

import json

from requests import Session
import auth
import pandas as pd
import downloader as dl
from datetime import date, datetime
from dateutil.relativedelta import relativedelta as datedelta
from pprint import PrettyPrinter


EIN_SOUGHT = ''
MAX_DOWNLOAD_ATTEMPTS = 3 # How many download attempts in a row before skipping to next user


def donation_count(session: Session, date: date) -> int:
    params = {'mes': date.month, 'ano': date.year, 'draw': 1, 'start': 0, 'length': 1}
    response = session.get('https://notaparana.pr.gov.br/nfprweb/app/v1/datatable/documentoFiscalDoado/', params=params)

    if not response.ok:
        return 0

    response = json.loads(response.text)
    return response['recordsTotal']


def load_users() -> list[auth.User]:
    with open('./users.json') as f:
        return json.load(f, cls=auth.UserDecoder)


def wrangle_donations(df: pd.DataFrame):
    df.drop(columns=['CNPJ', 'ENTIDADE', 'SITUAÇÃO'], inplace=True)
    df['NOTA'] = df['NOTA'].apply(lambda x: x[6:20])
    df['NOTA'] = df['NOTA'].apply(lambda x: f'{x[0:2]}.{x[2:5]}.{x[5:8]}/{x[8:12]}-{x[12:]}')
    df.rename(columns={'NOTA': 'CNPJ', 'DATA DA DOAÇÃO': 'DATA'}, inplace=True)
    df.drop_duplicates(keep='first', subset=['CNPJ'], inplace=True)
    #df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')


def main():
    users = load_users()
    donations = [] # Date of donations were EIN_SOUGHT was found

    for user in users:
        if session := auth.login(user) == False:
            print(f'Could not log-in user: {user.name}. Skipping...')
            continue

        donations.append({user.name: []})
        date = datetime.today()
        failed_download_attempts = 0

        while failed_download_attempts < MAX_DOWNLOAD_ATTEMPTS:
            if donation_count(session, date) == 0 or (filename := dl.download_donations(session, date) == False):
                print(f'Could not download donations of user: {user.name}, for the period: {date}. Skipping...')
                date = date - datedelta(months=1)
                failed_download_attempts += 1
                continue

            df = pd.read_csv(filename, encoding='iso8859-1', skiprows=1, sep=';')
            wrangle_donations(df)

            if EIN_SOUGHT in df['CNPJ'].values:
                row = df.query(f'CNPJ == "{EIN_SOUGHT}"').index[0]
                donations[-1][user.name].append(df.loc[row, 'DATA'])

            date = date - datedelta(months=1)
    
    for d in donations:
        for k in d:
            d[k].reverse()

    print('Finished Look Up.')
    print('Donation Dates:')
    PrettyPrinter().pprint(donations)


if __name__ == '__main__':
    main()
