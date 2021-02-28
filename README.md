# mal 
Uses web scrapping to return information from myanimelist (similar to an api)

# Installation
1. Clone/download this repository 
```bash
git clone https://github.com/kaili-chen/mal.git
```
2. Install requirements 
```
pip install requirements.txt
```

# Usage 
## Get anime information
### CLI
* in the `mal` dir
```
python anime.py <mal_anime_url> 
```
#### Flags
| Optional | Flag | Description |
| --- | --- | --- |
| No | --input | mal anime url (e.g. https://myanimelist.net/anime/4898/Kuroshitsuji) |

#### Example
```
python anime.py https://myanimelist.net/anime/4898/Kuroshitsuji"
```
(sample result can be found at [`./sample outputs/anime.json`](https://github.com/kaili-chen/mal/blob/master/sample%20outputs/anime.json))

# Result
* Notes
    * Not all key-value pairs might be present
    * if values are empty, "Unknown", "NA", or other similar indicators of unavailability, the value would be `null` in the result

## Anime 
| Key | Type | Description |
| --- | --- | --- |
| aired | `string` | date range that anime was aired |
| broadcast | `string` | weekday of broadcast, usually in JST |
| duration | `string` | duration of each anime episode / length of movie |
| english | `string` | english name of anime |
| episodes | `number` | number of episodes |
| favorites | `number` | how many mal members added this anime to their favourites |
| genres | `array` of `string` | genre(s) of anime |
| japanese | `string` |  japanese name of anime |
| licensors | `array` of `string` |anime's licensors |
| mal_id | `string` | mal's anime id |
| members | `number` | number of mal members that have this anime in their anime list |
| popularity | `number` | popularity ranking, [based on how many members have anime added to their anime list](https://myanimelist.net/info.php?go=topanime) |
| premiered | `string` | date that anime premiered |
| producers | `array` of `string` | anime's producers |
| ranked | `number` | rank of anime on ['top anime' list](https://myanimelist.net/info.php?go=topanime)|
| rating | `number` | viewership rating |
| related | `array` of `object` | related works of anime - [more info on `object` below](#anime-related) |
| retrieved_on | `string` | datetime string of when the information was extracted |
| score | `object` | rating of anime (same as previously mentioned rating) and the number of mal members that rated anime |
| source | `string` | source of material used for anime |
| status | `string` | current status of anime (e.g. airing, completed) |
| studios | `array` of `string` | studios that worked on anime |
| synonyms | `array` of `string` | other titles/names that anime go by |
| synopsis | `string` | synopsis of anime |
| type | `string` | type of anime (e.g. TV, ONA, OVA) |
| url | `string` | url of anime's mal page |

### Anime: related
| Key | Type | Description |
| --- | --- | --- |
| link | `string` | mal link to related material |
| related_type | `string` | type of relation to anime (e.g. adaption, sequel) |
| title | `string` | title of related material |

### Anime: score
| Key | Type | Description |
| --- | --- | --- |
| score | `number` | [weighted average by mal users](https://myanimelist.net/info.php?go=topanime) |
| scored_by | `number` | number of mal users who scored the anime |

## Character
| Key | Type | Description |
| --- | --- | --- |
| eng_name | `string` | character's english name |
| jap_name | `string` | character's japanese name |
| mal_id | `string` | mal's character id |
| favorites | `number` | how many mal members added this chafacter to their favourites |
| retrieved_on | `string` | datetime string of when the information was extracted |
| url | `string` | url of character's mal page |

# To-Do
## Character
* get long description of character
* get character's animeography
* get character's mangaography

# Background story
this frankly started as an information gathering project for some mindlessly fun visualisations but i got too invested and am working on it on-and-off in my free time. i am still motivated to refine it, as a way to learn data mining, making packages that make sense and so on. here's the pitch: any support in the form of coffee $ is appreciated :) (sponsor button is on the top of this page)