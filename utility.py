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

### MAL SPECIFIC UTILITY FUNCTIONS
class MalUrlError(Exception):
    pass

def is_mal_url(url, check_type=None):
    '''
    Checks if url provided is a mal url

    Parameters:
        url (string):  url
        check_type (string): indicate which kind of mal urls to check for (e.g. anime, people)

    Returns:
        (boolean) indicating if url provided is a mal url
            - if check_type is not None and valid, True when url is mal url and is of type
    '''
    # TODO: seperate into type of mal page for url
    TYPES = ['anime', 'people']
    if check_type is not None and not check_type in TYPES:
        raise MalUrlError("check type provided: {}, is not valid or currently supported.".format(check_type))
    if url.find('myanimelist.net') > -1:
        return True
    return False

### BEAUTIFULSOUP UTILITY FUNCTIONS
class Bs4Error(Exception):
    pass

def get_soup(url):
    '''
    Returns a BeautifulSoup object of the HTML contents of a provided url.

    Parameters:
        url (string): url of the site to generate soup object of

    Returns:
        soup (bs4.BeautifulSoup):
    '''
    webpage = requests.get(url)
    # print("{}\n\t{}".format(url, webpage))
    if webpage.status_code != 200:
        # print('webpage status code = {}, exiting'.format(webpage.status_code))
        # sys.exit()
        raise Bs4Error("{}: status code = {}, exiting get_soup function".format(url, webpage.status_code))

    soup = BeautifulSoup(webpage.text, "html.parser")
    if soup is None or soup == "":
        # print("no soup, exiting")
        # sys.exit()
        raise Bs4Error("{}: no soup, exiting get_soup function".format(url, webpage.status_code))
    return soup

def remove_children(element):
    '''
    Removes children elements from a bs4.element.Tag (changes the input element).

    Inputs:
        element (bs4.element.Tag)

    '''
    # print("input = {}".format(element))
    for child in element.children:
        try:
            child.decompose()
            # print("\tdecom = {}".format(element))
        except AttributeError:
            continue
        # print()
    return element

### GENERAL UTILITY FUNCTIONS
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
        json.dump(data, json_file, ensure_ascii=False, indent=4, sort_keys=True)

    return os.path.abspath(filename)
