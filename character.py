'''
Functions and CLI for code to get mal character information.
'''

import re
from datetime import datetime
import utility
from utility import Bs4Error
from bs4 import NavigableString
import argparse
import sys

dt = datetime.now()
timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S+08:00')

def get_character_info(url, full=False):
    '''
    Gets character information from mal character url.

    Parameters:
        url [string]: mal anime url (https://myanimelist.net/anime/...)
        full [bool] [defualt=False]: indicate whether to get additional information (episodes, mal statistics)

    Returns
        info [dict]: mal anime information
    '''
    # TODO change full option to dict option, as add on (so check if is boolean or dict)
    info = {}
    soup = utility.get_soup(url)
    content = soup.find('div', {'id': 'content'})
    
    ## META INFO -START
    mal_id = url[url.find('/character/')+1:].split('/')[1]
    info['mal_id'] = mal_id

    url_tag = soup.find('meta', property="og:url")
    if url_tag:
        info['url'] = url_tag['content']
    else:
        info['url'] = url
    ### META INFO -END

    ### NAME -START
    eng_name_tag = content.find('h2', {'class':'normal_header'})    # 1st h2 header in content div
    jap_name_tag = eng_name_tag.find('small')
    if jap_name_tag:
        info['jap_name'] = re.sub(r'[\(\)]', '', jap_name_tag.text)
    if eng_name_tag:
        utility.remove_children(eng_name_tag)
        info['eng_name'] = eng_name_tag.text
    ### NAME -END

    ### MEMBER FAVES -START
    search = re.search(r'Member Favorites: ([0-9]*\,*[0-9]*)\n', content.text)
    if search:
        member_faves = int(re.sub(r'\D', '', search.group(0)))
        info['member_faves'] = member_faves
    ### MEMBER FAVES -END

    ### POST-PROCESSING -START
    info['retrieved_on'] = timestamp
    return info

if __name__ == '__main__':
    # cmd line colours
    RESET = '\033[0;0m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'

    # TODO add path_out
    ap = argparse.ArgumentParser()

    # positional arguments
    ap.add_argument('input', help='mal CHARACTER url')

    args = vars(ap.parse_args())

    # input validation
    if utility.get_mal_type(args['input']) is not 'character':
        print('{}ERROR: given url ({}) is not a valid mal character url'.format(RED,args['input']))
        sys.stdout.write(RESET)
        sys.exit()
    try: 
        data = get_character_info(args['input'])

        output_filename = 'output_{}.json'.format(re.sub(r'\W', '', timestamp))
        utility.save_json(data, output_filename)
        print('{}information saved to file: {}'.format(GREEN, output_filename))
    except Exception as e:
        print('{}ERROR: {}'.format(RED,str(e)))

    sys.stdout.write(RESET)