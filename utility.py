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
import re

### MAL SPECIFIC UTILITY FUNCTIONS
def get_mal_type(url):
    '''
    Returns what type (anime, character etc.) of mal url the given url is 

    Parameters:
        url [string]:  url

    Returns:
        mal_url_type [string]: type of mal url (if any) 
            - types: 'episode', 'anime', 'character', 'people'
            - returns None if not a mal url (does not match any types)
    '''
    mal_base_pattern = r'([https:\/\/]*myanimelist.net\/)'
    # episode needs to be matched before anime cos its url is a more specific ver of the anime one
    # TODO not allow invalid episodes to match anime pattern
    types_pattern = {
        'episode': r'anime\/.+\/episode\/\d+',
        'anime': r'anime\/.+',
        'character': r'character\/.+',
        'people': r'people\/.+'
    }
    
    # check for base mal url first
    patt = re.compile(mal_base_pattern)
    match = patt.match(url)
    if not match:
        return None
    
    # get url after the initial base pattern
    remaining = url[match.span()[1]:]
    for mal_type, pattern in types_pattern.items():
        patt = re.compile(pattern)
        match = patt.match(remaining)
        if match:
            return mal_type
    return None

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
        raise Bs4Error("{} [status: {}]: no soup, exiting get_soup function".format(url, webpage.status_code))
        
    return soup

def remove_children(element):
    '''
    Removes children elements from a bs4.element.Tag (changes the input element).

    Inputs:
        element (bs4.element.Tag)

    '''
    # print("input = {}".format(element))
    if element:
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
