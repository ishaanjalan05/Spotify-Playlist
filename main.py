import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

client_id = "8b31056b265f4f1795fc3616b37867c9"
client_secret = "2fee944e0a9a428da5e38a586bd89830"
redirect_url = "http://example.com"
OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

authentication = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url,
                              scope="playlist-modify-private", show_dialog=True,
                              cache_path="token.txt")

sp = spotipy.Spotify(auth_manager=authentication)
user_id = sp.current_user()["id"]
date = input("What year do you want to travel to? Type the date in this format YYY-MM-DD: ")
url = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url)
content = response.text
soup = BeautifulSoup(content, "html.parser")
count = 0


songs = soup.find_all(name="h3", id="title-of-a-story",
                      class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

songs_list = [soup.find(name="a", class_="c-title__link lrv-a-unstyle-link").getText()]

artist_list = [soup.find(name="p", class_="c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150").getText()]

artists = soup.find_all(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
for artist in artists:
    data = artist.getText().strip().split()
    name = data[0] + " "
    if len(data) > 1:
        name += data[1]
    artist_list.append(name)

for song in songs:
    songs_list.append(song.getText())

year = date.split("-")[0]
song_uris = []
for i in range(100):
    print(artist_list[i])
    response = sp.search(q=f"track:{songs_list[i]} artist: {artist_list[i]}", type="track")
    try:
        song_uris.append(response["tracks"]["items"][0]["uri"])
    except:
        print(f"{songs_list[i]} doesn't exist in Spotify. Skipped.")


with open("token.txt") as file:
    data = json.loads(file.read())
    access_token = data["access_token"]

print(access_token)
playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist_id)
sp.playlist_add_items(playlist_id=playlist_id["id"], items=song_uris)
