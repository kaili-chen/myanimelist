'''
Contains utility functions for mal.py

Methods
-------
get_soup(url -> string): returns b24.BeautifulSoup object from url
'''

import sys
import requests
from bs4 import BeautifulSoup
import os
import json

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

def save_json(data, filename):
    '''
    Saves data to a json file.

    Parameters:
        data (dict): data to save to json file
        filename (string): filename to save json file as (saves to current dir by default)

    Returns:
        path (string): absolute path to json file
    '''

    # TODO: use path_out instead of filename instead?

    # checks if file already has json extension
    if ".json" not in filename:
        filename = "{}.json".format(filename)

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

    return os.path.abspath(filename)

def remove_children():
    # TODO: add function to remove children from bs4 parent element
    pass
