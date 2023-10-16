from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLINT_ID = "YOUR SPOTIFY DEVELOPER CLINT ID"
CLINT_SECRET = "YOUR SPOTIFY DEVELOPWE CLINT SECRET"
SCOPE = "playlist-modify-private"

date = input("Enter date you wanna jump back to(yyyy-mm-dd): ")
html = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")

# A bit messy but works
soup = BeautifulSoup(html.text, "html.parser")
titles_html = soup.find_all(name="h3", id="title-of-a-story")
titles = [title.getText().strip() for title in titles_html]
for title in titles:
    if title == "Songwriter(s):" or title == 'Imprint/Promotion Label:' or title == "Additional Awards":
        titles.remove(title)
del titles[1]
del titles[1]
titles = titles[:200]
song_names = []
for title in titles:
    if titles.index(title) % 2 != 0:
        song_names.append(title)

# MAM
# soup = BeautifulSoup(html.text, 'html.parser')
# song_names_spans = soup.select("li ul li h3")
# song_names = [song.getText().strip() for song in song_names_spans]

# Random Dude
# while True:
#     date = input("Which date to travel to? Format YYYY-MM-DD: ")
#     if len(date) == 10 and date[4] == '-' and date[7] == '-':
#         if date[:4].isdigit() and date[5:7].isdigit() and date[8:].isdigit():
#             break
#     else:
#         print("Invalid format. Please try again.")
#
# r = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
# top_100 = BeautifulSoup(r.text, "html.parser")
# chart_results = top_100.find_all(class_="o-chart-results-list-row")
#
# billboard_top_100 = []
#
# for song in chart_results:
#     song_title = song.h3.get_text().replace('\n', '').replace('\t', '')
#     artist = song.h3.next_sibling.next_sibling.get_text().replace('\n', '').replace('\t', '')
#     print(song_title, artist)
#     new_data = {
#         "song": song_title,
#         "artist": artist
#     }
#     billboard_top_100.append(new_data)
#
# print(billboard_top_100)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLINT_ID, client_secret=CLINT_SECRET, cache_path="token.txt", redirect_uri="https://example.com", username="Shri"))
user_id = sp.current_user()["id"]

song_links = []
for track in song_names:
    try:
        link = sp.search(q=f"track:{track} year:{date[:4]}", type="track", limit=1)
        song_links.append(link["tracks"]["items"][0]["external_urls"]["spotify"])
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Top 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_links)
print("Playlist created ^_~")
