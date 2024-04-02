import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def request_soup(session_args: requests.Request) -> requests.Response:
    '''Requests an arbitrary remote resource using the provided `Request`-formatted object.

    :param sessionArgs : Requests-formatted session arguments.
    :raises HTTPError: If the response status code is not 200.
    '''

    session = requests.Session()
    prepared_request = session.prepare_request(session_args)
    response: requests.Response = session.send(prepared_request)

    # Check if the status code is not 200
    if response.status_code != 200:
        # Raise an HTTPError if the status is not 200
        raise HTTPError(f'Error: Received status code {response.status_code} for URL: {response.url}', response=response)
    
    # Parse using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup