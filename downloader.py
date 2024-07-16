# Author: Erick Ruh Cardozo  (W1SD00M) - <erickruhcardozo98@gmail.com>
# Date: Jul 15, 2024 - 12:45 PM
# Description: This module downloads a donation report for a specified date.

from requests import Session
from datetime import date
from tempfile import NamedTemporaryFile
import json


def get_donations_count(session: Session, date: date) -> int:
    params = {'mes': date.month, 'ano': date.year, 'draw': 1, 'start': 0, 'length': 1}
    response = session.get('https://notaparana.pr.gov.br/nfprweb/app/v1/datatable/documentoFiscalDoado/', params=params)

    if not response.ok:
        return 0

    response = json.loads(response.text)
    return response['recordsTotal']


def download_donations(session: Session, date: date) -> bool | str:
    """
    Attempts to download a donation report. On success, returns the
    path to the downloaded report. If the request status code is not
    200 or the total records for the queried date are 0, returns False.
    """
    if get_donations_count(session, date) == 0:
        return False

    period = f'{date.month:02}/{date.year}'
    url = f'https://notaparana.pr.gov.br/nfprweb/RelatorioDocFiscalDoado?periodo={period}'
    print(f'Attempting download donation resume for period: {period}')
    with session.get(url, stream=True) as response:
        if not response.ok:
            print(f'Could not download resource: Server returned {response.status_code}')
            return False
        
        with NamedTemporaryFile('wb', delete=False) as f:
            print(f'Writing to file: {f.name}')
            for chunk in response.iter_content(10  * 1024):
                f.write(chunk)
            return f.name