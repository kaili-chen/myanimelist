import re
from datetime import datetime
import utility
from utility import Bs4Error

dt = datetime.now()
timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")

### FUNCTIONS
def get_anime_info(url, full=False):
    '''
    Gets anime information from mal anime url.

    Parameters:
        url (string): mal anime url (https://myanimelist.net/anime/...)
        full (bool) [defualt=False]: indicate whether to get additional information (episodes, mal statistics)

    Returns
        info (dict): mal anime information
    '''

    soup = utility.get_soup(url)
    info = {}

    ### BASIC ANIME INFO
    ## META INFO
    mal_id = url[url.find("/anime/")+1:].split("/")[1]
    info["malId"] = mal_id

    title = soup.find("meta", property="og:title")
    title['url'] = title["content"].strip()

    url_tag = soup.find('meta', property="og:url")
    if url_tag:
        info['url'] = url_tag['content']
    else:
        info['url'] = url

    synopsis_tag = soup.find('meta', property="og:description")
    if synopsis_tag:
        synopsis = synopsis_tag['content']
        # removes last line
        synopsis = synopsis.replace("[Written by MAL Rewrite]", "")
        info['synopsis'] = synopsis.strip()
    else:
        info['synopsis'] = ""


    dark_text_tags = soup.find_all("span", {"class": "dark_text"})
    for tag in dark_text_tags:
        # SECTIONS: (alternative titles) english, synonyms, japanese
        #           (information) type, episodes
        section_name = tag.text.lower()
        if section_name[-1] == ":":
            section_name = section_name[:-1]
        # print("section name : {}".format(section_name))

        span_parent = tag.parent
        # print("\t {}".format(span_parent))
        values = []
        spans = span_parent.find_all("span")
        links = span_parent.find_all("a")
        if spans:
            # print("span found: {}".format(spans))
            for span in spans[1:]:
                values.append(span.text.strip())
                # print("\tspan: {}".format(span.text.strip()))
        if links:
            for link in links:
                values.append(link.text.strip())
                # print("\tlink: {}".format(link.text.strip()))

        if len(values) < 1:
            span_parent = utility.remove_children(span_parent)
            values.append(span_parent.text.strip())

        values = list(set(values))
        if len(values) < 2:
            values = values[0]
            if section_name == "synonyms":
                values = values.split(",")
            if section_name in ["episodes", "popularity", "members", "favorites"]:
                values = re.sub("[#,]", "", values)
                try:
                    values = int(values)
                except ValueError:
                    if values.lower() == "unknown":
                        values = None
        if section_name == "score":
            score = {}
            for v in values:
                try:
                    # WARNING: might cause issues if less than 10 people scored the anime
                    if float(v) <= 10:
                        score['score'] = float(v)
                    else:
                        score['scoredBy'] = int(v)
                except ValueError:
                    continue
            values = score

        elif section_name == "ranked":
            top_anime_rank = tag.nextSibling
            if top_anime_rank == "N/A":
                values = None
            else:
                values = top_anime_rank.strip()

        info[section_name] = values

    if full:
        try:
            eps = get_anime_episodes("{}/episode".format(info['url']))
            info["episode_info"] = eps
        except Bs4Error:
            info["episode_info"] = []

        stats = get_mal_stats("{}/stats".format(info['url']))
        info["stats"] = stats

    ### POST-PROC BEFORE RETURN
    # if no english title in left side bar, use meta tag
    if not 'english' in info:
        info['english'] = soup.find('meta', property="og:title")['content']
    # trim leading and trailing white spaces from synonyms
    if not 'synonyms' in info:
        info['synonyms'] = []
    elif len(info['synonyms']) > 0:
        info['synonyms'] = [s.strip() for s in info['synonyms']]
    info['retrieved_on'] = timestamp
    return info


def get_anime_episodes(url):
    '''
    Gets anime episodes information from mal anime url.

    Parameters:
        url (string): mal anime episode url (https://myanimelist.net/anime/<anime_id>/episode)

    Returns
        eps (list): contains each episode as its own individual dict object
    '''
    soup = utility.get_soup(url)

    eps = []
    ep_rows = soup.find_all("tr", class_ = "episode-list-data")
    for row in ep_rows:
        ep_num = row.find("td", class_ = "episode-number").text
        titles = row.find("td", class_ = "episode-title")
        title_link = titles.find("a")
        ep_url = title_link["href"]
        eng_title = title_link.text.strip()
        jap_title = titles.find("span").text.strip()
        aired = row.find("td", class_="episode-aired").text.strip()

        eps.append({
            "ep_num": int(ep_num),
            "eng_title": eng_title,
            "jap_title": jap_title,
            "aired": aired,
            "url": ep_url
        })
    return eps


def get_mal_stats(url):
    '''
    Gets anime mal stats information from mal anime url.

    Parameters:
        url (string): mal anime stats url (https://myanimelist.net/anime/<anime_id>/stats)

    Returns
        stats (dict): mal stats
    '''

    soup = utility.get_soup(url)
    stats = {}
    divs = soup.find_all("div", class_="spaceit_pad")
    for d in divs:
        span = d.find('span')
        if span and span.text.strip() in ["Watching:", "Completed:", "On-Hold:", "Dropped:", "Plan to Watch:", "Total:"]:
            stat_label = span.text.replace(":", "").strip().lower()
            span.decompose()
            stat_value = int(d.text.replace(",", ""))
            # print("{} : {}".format(stat_label, stat_value))
            stats[stat_label] = stat_value

    score_table = soup.find("table", class_="score-stats")
    scores = {}
    if score_table:
        for row in score_table.find_all("tr"):
            score_label = int(row.find("td", class_="score-label").text)
            votes = row.find("small").text
            votes = int(re.sub("\D", "", votes))
            # print("score = {}, votes = {}".format(score_label, votes))
            scores[score_label] = votes
        stats["score_votes"] = scores
    else:
        stats["score_votes"] = None

    return stats


def get_anime_characters(url):
    '''
    Gets anime characters' information from mal anime url.

    Parameters:
        url (string): mal anime url (https://myanimelist.net/anime/<mal anime id>/characters)

    Returns
        characters (dict): mal anime characters' information
    '''

    soup = utility.get_soup(url)
    # print(soup.prettify())
    characters = []
    h2_headers = soup.find_all("h2")
    # print(h2_headers)
    for h in h2_headers:
        h = utility.remove_children(h)
        h2_text = h.text.strip()

        if h2_text == "Characters & Voice Actors" or h2_text == "Characters &amp; Voice Actors":
            current_tag = h.parent.nextSibling

            while current_tag is not None and current_tag.name == "table":
                cells = current_tag.find_all("td")

                character = cells[1]
                character_url = character.find("a")["href"]
                character_name = character.find("a").text.strip()
                character_type = character.find("div").find("small").text.strip()
                # print("{} [{}]".format(character_name, character_type))

                for cell in cells[3:]:
                    if cell["valign"] == "top":
                        seiyuu_name = cell.find("a").text.strip()
                        seiyuu_url = cell.find("a")["href"]
                        seiyuu_lang = cell.find("small")
                        if not seiyuu_lang:
                            continue
                        seiyuu_lang = seiyuu_lang.contents[0]
                        # print("\t{}".format(cell))
                        # print("\t{} [{}]".format(seiyuu_name, seiyuu_lang))
                        # print("\t{}".format(seiyuu_url))
                        characters.append({
                            "character": character_name,
                            "characterUrl": character_url,
                            "characterType": character_type,
                            "va": seiyuu_name,
                            "lang": seiyuu_lang,
                            "url": seiyuu_url
                        })
                current_tag = current_tag.nextSibling
    return characters


def get_anime_staff(url):
    '''
    Gets anime staff information from mal anime url.

    Parameters:
        url (string): mal anime url (https://myanimelist.net/anime/<mal anime id>/characters)

    Returns
        staff (dict): mal anime staff information
    '''

    soup = utility.get_soup(url)
    # print(soup.prettify())
    staff = []
    h2_headers = soup.find_all("h2")
    # print(h2_headers)
    for h in h2_headers:
        h = utility.remove_children(h)
        h2_text = h.text.strip()

        if h2_text == "Staff":
            current_tag = h.parent.nextSibling
            # cells = current_tag.find_all("td")
            # print(cells[1].find("small").text.strip())

            while current_tag is not None and current_tag.name == "table":
                cells = current_tag.find_all("td")
                staff_person = cells[1]
                staff_name = staff_person.find('a').text.strip()
                staff_url = staff_person.find('a')['href']
                # print("{} ({})".format(staff_name, staff_url))
                role_str = staff_person.find("small").text.strip()
                if len(role_str) > 0:
                    roles = [r.strip() for r in role_str.split(",")]
                else:
                    roles = []
                # print("\t{}".format(roles))
                staff.append({
                    "staff": staff_name,
                    "staffUrl": staff_url,
                    "roles": roles
                })
                current_tag = current_tag.nextSibling
    return staff


if __name__ == "__main__":
    # TODO: add command line usage
    pass
