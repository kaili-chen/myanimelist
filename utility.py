'''
Contains utility functions for mal.py

Methods
-------
get_soup(url -> string): returns b24.BeautifulSoup object from url
'''

import sys
import requests
from bs4 import BeautifulSoup

### UTILITY FUNCTIONS
def get_soup(url):
    '''
    Returns a BeautifulSoup object of the HTML contents of a provided url.

    Parameters:
        url (string): url of the site to generate soup object of

    Returns:
        soup (bs4.BeautifulSoup):
    '''
    webpage = requests.get(url)
    if webpage.status_code != 200:
        print('webpage status code = {}, exiting'.format(webpage.status_code))
        sys.exit()

    soup = BeautifulSoup(webpage.text, "html.parser")
    if soup is None or soup == "":
        print("no soup, exiting")
        sys.exit()

    return soup


# TODO: add function to remove children from bs4 parent element
