from datetime import datetime
import utility
import logging
import os

### init timestamp
dt = datetime.now()
timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")

### init log
if not os.path.exists("./log") and not os.path.isdir("./log"):
    os.mkdir("./log")
logging.basicConfig(format='[%(asctime)s] %(module)s:%(funcName)s:%(levelname)s:%(message)s',
                    filename='log/person_{}.log'.format(dt.strftime("%Y-%m-%dT%H-%M-%S")),
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.WARNING)

### FUNCTIONS
def get_info(url):
    '''
    Extracts info from a mal people url.

    Input:
        url (string): mal people url (https://myanimelist.net/people/<mal_id>/<name>)

    Returns:
        person_data (dict): dict object containing person's data from mal
    '''

    # TODO: add url validation

    logging.info('STARTED')
    logging.debug('input_url={}'.format(url))

    soup = utility.get_soup(url)

    person_data = {}

    ### PERSON BASIC INFO
    ## from meta data
    person_full_name = soup.find("meta", property="og:title")["content"].strip()
    person_data["full_name"] = person_full_name

    person_url = soup.find("meta", property="og:url")["content"]
    person_data["url"] = person_url

    ## from left side bar space
    basic_info_spans = soup.find_all('span', class_='dark_text')
    # ignore last span for more
    for span in basic_info_spans:
        info_label = span.text.replace(":", "").lower()
        info_label = info_label.replace(" ", "_")
        # print(info_label)
        if info_label == "more":
            continue
        span_parent = span.parent
        if info_label == "website":
            website_tag = span.nextSibling.nextSibling
            if website_tag.name == 'a':
                info = website_tag['href']
        elif span_parent.name != "div":
            info = span.nextSibling.strip().lower()
        else:
            # print(span_parent.text)
            span_parent = utility.remove_children(span_parent)
            info = span_parent.text.strip()

        # print("{} = {}".format(info_label, info))
        person_data[info_label] = info

    ## from left side bar bottom part
    add_info_div = soup.find_all("div", class_="people-informantion-more")
    add_info = add_info_div[0].text
    add_info = add_info.split('\n')

    info_cats = ["birth place:", "height:", "weight:", "blood type:", "more:"]
    for s in add_info:
        str = s.strip()
        if len(str) > 0 and any(substring in str.lower() for substring in info_cats):
            arr = str.split(":")
            info_label = arr[0].strip().lower()
            info = arr[1].strip()

            person_data[info_label] = info


    ### ROLES
    va_roles = []
    staff_roles = []
    for section in soup.find_all('div', class_='normal_header'):
        header = utility.remove_children(section).text.strip().lower()
        # print(header.text.strip().lower())
        if header == "voice acting roles":
            # assumes the next tag is a table; each row is a role
            try:
                rows = section.nextSibling.find_all('tr')
            except AttributeError:
                # no anime roles most likely, skip
                continue

            for row in rows:
                role = row.find_all('td')
                anime_td = role[1]
                # get first link in td
                anime_name = anime_td.find('a').text.strip()
                anime_url = anime_td.find('a')['href']
                # print("{} ({})".format(anime_title, anime_url))

                character_td = role[2]
                character_name = character_td.find('a').text.strip()
                character_url = character_td.find('a')['href']
                character_type = character_td.find('div').text.strip().lower()
                # print("{} ({})".format(character_name, character_url))
                va_roles.append({
                    'anime_name': anime_name,
                    'anime_url': anime_url,
                    'character_name': character_name,
                    'character_type': character_type,
                    'character_url': character_url
                })

        elif header == "anime staff positions":
            try:
                rows = section.nextSibling.find_all('tr')
            except AttributeError:
                # no staff roles most likely, skip
                continue
            # print(rows)
            for row in rows:
                role = row.find_all('td')
                anime_td = role[1]
                # # get first link in td
                anime_name = anime_td.find('a').text.strip()
                # print(anime_name)
                anime_url = anime_td.find('a')['href']
                # print("{} ({})".format(anime_name, anime_url))
                staff_role = anime_td.find('small').text
                staff_roles.append({
                    'anime_name': anime_name,
                    'anime_url': anime_url,
                    'role': staff_role
                })

    person_data['va_roles'] = va_roles
    person_data['staff_roles'] = staff_roles

    ### POST PROCESSING (to make data more managable when exported)
    ## make birthday ISO-1806
    try :
        # change "Unknown" birthday to ""
        if person_data['birthday'].lower() == "unknown":
            person_data['birthday'] = ''
        else:
            person_data['birthday'] = datetime.strptime(person_data['birthday'], "%b  %d, %Y").strftime('%Y-%m-%d')
    except ValueError:
        # if birthday does not match date format and is not unknown, leave as it is and log
        logging.warning("exception: birthday did not fit format: Y-m-d")
        pass

    ## make alternate_names into an array
    if 'alternate_names' in person_data:
        person_data['alternate_names'] = person_data['alternate_names'].split(',')
    else:
        person_data['alternate_names'] = []

    person_data['member_favorites'] = int(person_data['member_favorites'].replace(",", ""))

    ## deal with empty website
    if 'website' not in person_data or person_data['website'] in ['https', 'http://']:
        person_data['website'] = ''

    ## add mal_id
    mal_id = person_data['url'].replace('https://myanimelist.net/people/', '')
    mal_id = mal_id[:mal_id.rfind('/')]
    person_data['mal_id'] = mal_id.strip()

    ## add timestamp to person_data
    person_data['retrieved_on'] = timestamp

    return person_data

if __name__ == "__main__":
    pass
