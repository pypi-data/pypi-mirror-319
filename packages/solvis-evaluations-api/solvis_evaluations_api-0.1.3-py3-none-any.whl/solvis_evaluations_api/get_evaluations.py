import logging
import csv
import requests
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
from typing import Optional


class GetEvaluations:
    """
    Teste
    A class to interact with the surveys API and fetch evaluations data.
    """

    def __init__(self) -> None:
        """
        Initialize the GetEvaluations class with default attributes.
        """
        self.user: Optional[str] = None
        self.password: Optional[str] = None
        self.session: Optional[requests.Session] = None

    def get_evaluations(
        self,
        user: str,
        password: str,
        survey_id: int,
        start_date: str,
        end_date: str,
        verbose: bool = True,
    ) -> pd.DataFrame:
        """
        Fetch survey responses from the API within a specified date range.

        Args:
            user (str): API username.
            password (str): API password.
            survey_id (int): Survey ID to fetch responses for.
            start_date (str): Start date in 'DD/MM/YYYY' format.
            end_date (str): End date in 'DD/MM/YYYY' format.
            verbose (bool): If True, logs INFO level messages; otherwise, logs ERROR level messages.

        Returns:
            pd.DataFrame: A DataFrame containing evaluations.

        Raises:
            ValueError: If date range is invalid.
            Exception: For API-related errors.
        """
        self.user = user
        self.password = password
        self.session = requests.Session()

        # Configure logging based on verbosity
        logging.basicConfig(
            level=logging.INFO if verbose else logging.ERROR,
            format='%(levelname)s - %(message)s',
        )

        try:
            start_datetime = datetime.strptime(start_date, '%d/%m/%Y')
            end_datetime = datetime.strptime(end_date, '%d/%m/%Y')
        except ValueError as e:
            raise ValueError(f'Invalid date format: {e}')

        days_count = (end_datetime - start_datetime).days + 1
        if days_count <= 0:
            raise ValueError('End date must be after start date.')

        api_base_url = f'https://www.solvis.net.br/results_api/v1/surveys/{survey_id}/responses'
        logging.info(f'Selected period: {start_date} to {end_date} ({days_count} days)')

        responses = []
        logging.info('Downloading responses...')

        for i in range(days_count):
            date_str = (start_datetime + timedelta(days=i)).strftime('%Y-%m-%d')
            logging.info(date_str)
            url = f'{api_base_url}?date={date_str}'
            try:
                resp = self.session.get(url, auth=(self.user, self.password))
                if resp.status_code != 200:
                    raise Exception(f'API request failed with status code {resp.status_code}')

                # Parse CSV data
                csv_text = resp.text
                csv_reader = csv.reader(StringIO(csv_text))
                rows = list(csv_reader)

                # Extract header and data rows
                if i == 0:
                    header = rows[0]
                    responses.append(header)
                data_rows = rows[1:]

                # Append valid rows
                for row in data_rows:
                    if len(row) == len(header):
                        responses.append(row)
                    else:
                        logging.warning(f'Row length mismatch on {date_str}: {row}')

                logging.info(f'Page {i + 1}/{days_count} fetched successfully.')
            except Exception as e:
                logging.error(f'Error fetching data for {date_str}: {e}')
                break

        df_responses = pd.DataFrame(responses[1:], columns=responses[0])
        logging.info('Data fetching complete.')

        return df_responses
