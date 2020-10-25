## to-do
* [20 Sep 2020] [haikyuu_2020-09-18T23:50:02+08:00.json] [anime.py] "add more" values in field licensors
* [20 Sep 2020] [haikyuu_2020-09-18T23:50:02+08:00.json] [anime.py] synonyms have leading spaces
* [20 Sep 2020] [haikyuu_2020-09-18T23:50:02+08:00.json] [anime.py] episode_info date in ISO8601
* [20 Sep 2020] can automate this note-taking process?
* [20 Sep 2020] [anime.py] check for missing fields and fill in with blanks as needed
* [20 Sep 2020] [anime.py] durations for movies (type) to be in seconds minutes instead of string
* !! [20 Sep 2020] character page
* [20 Sep 2020] [anime.py] before returning data, make "Unknown" -> None

### 19 September 2020
* [8:46 PM] [anime.py] [get_anime_info] added retrieved_on timestamp to final info dict

### 20 September 2020
* [utility.py] added class Bs4Error to deal with 404 errors from when anime is movie and there is not episode url
* [anime.py] added try except to when full=True to make episode_info = [] when Bs4Error thrown
* [10:49 PM] [test_utility.py] unittest file to test utility's is_mal_url function
* [11:06 PM] [anime.py] refactor decompose parent element code blocks to use utility remove_children function
* [11:10 PM] [anime.py] changes episode_info's fields changes from camel case to udnerscore seperated (epNum -> ep_num, engTitle -> eng_title, japTitle -> jap_title), for more consistency in naming convention
* [11:17 PM] [anime.py] issues with int() with unaired anime, lmao need to really comment code wth is happening
* [11:25 PM] [anime.py] (for prev point) added try catch for ValueError (when cannot convert string to int) to check if value field is "Unknown" for sections ["episodes", "popularity", "members", "favorites"]

### 21 September 2020
* [5:23 PM] [anime.py] added post-proc to deal with no english title in left side-bar - use meta tag og:title instead
* [9:42 PM] [moriarty_2020-09-20T23:23:22+08:00.json] [anime.py] why does it show ranked = "top anime" when it is N/A ? <-- cos code goes through span text and link text, with link text for ranked always being "top anime" (mouse over tooltip text)
* [9:46 PM] [anime.py > get_mal_stats] set scoreVotes to None (null in json) if no score table
* [9:47 PM] [anime.py > get_mal_stats] change dict field scoreValues -> score_values, for consistency
* [10:04 PM] [anime.py > get_anime_info] made ranked field reflect N/A or rank of anime in top anime charts
* [10:15 PM] [utility.py > get_soup] changed print and sys.exit to raise custom Bs4Error instead

### 23 September 2020
* [2:41 PM] [anime.py > get_anime_info] added post proc to make licensors "add some" to be None  (null), also changes duration "Unknown" to None (null)

### 18 October 2020
* [7:01 PM] character seems to just be random and the "attributes" of a character depends on the anime - e.g. Tobio has "team" and "ability parameters" and does not have "known siblings" (which lelouch has) --> just get general attributess
