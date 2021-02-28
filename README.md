# mal 
Uses web scrapping to return information from myanimelist (like an api)

# Installation
```
pip install requirements.txt
```

# Usage 
## Get anime information
### CLI
```
python anime.py <mal_anime_url> 
```
### Example
```
python anime.py https://myanimelist.net/anime/4898/Kuroshitsuji"
```
#### Result
* saved as output_{timestamp}.json
```json
{
    "aired": "Oct 3, 2008 to Mar 27, 2009",
    "broadcast": "Unknown",
    "duration": "24 min. per ep.",
    "english": "Black Butler",
    "episodes": 24,
    "favorites": 23489,
    "genres": [
        "Comedy",
        "Action",
        "Demons",
        "Historical",
        "Mystery",
        "Shounen",
        "Supernatural"
    ],
    "japanese": "黒執事",
    "licensors": [
        "Funimation",
        "Aniplex of America"
    ],
    "mal_id": "4898",
    "members": 873109,
    "popularity": 92,
    "premiered": "Fall 2008",
    "producers": [
        "Aniplex",
        "Movic",
        "Trinity Sound",
        "Mainichi Broadcasting System",
        "Square Enix",
        "Yomiko Advertising"
    ],
    "ranked": "#927",
    "rating": "R - 17+ (violence & profanity)",
    "retrieved_on": "2021-02-14T11:10:47+08:00",
    "score": {
        "score": 7.75,
        "scoredBy": 444046
    },
    "source": "Manga",
    "status": "Finished Airing",
    "studios": "A-1 Pictures",
    "synonyms": [
        "Kuro Shitsuji",
        "Kuroshitsuzi"
    ],
    "synopsis": "Young Ciel Phantomhive is known as \"the Queen's Guard Dog,\" taking care of the many unsettling events that occur in Victorian England for Her Majesty. Aided by Sebastian Michaelis, his loyal butler with seemingly inhuman abilities, Ciel uses whatever means necessary to get the job done. But is there more to this black-clad butler than meets the eye? In Ciel's past lies a secret tragedy that enveloped him in perennial darkness—during one of his bleakest moments, he formed a contract with Sebastian, a demon, bargaining his soul in exchange for vengeance upon those who wronged him. Today, not only is Sebastian one hell of a butler, but he is also the perfect servant to carry out his master's orders—all the while anticipating the delicious meal he will eventually make of Ciel's soul. As the two work to unravel the mystery behind Ciel's chain of misfortunes, a bond forms between them that neither heaven nor hell can tear apart.",
    "type": "TV",
    "url": "https://myanimelist.net/anime/4898/Kuroshitsuji"
}
```