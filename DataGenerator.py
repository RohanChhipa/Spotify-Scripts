import json
import requests
import math

TOKEN = ''


def pullLikedSongs():

    print("Pulling liked songs...", end="")

    url = 'https://api.spotify.com/v1/me/tracks?offset=0&limit=50'
    headers = {'Authorization': f'Bearer {TOKEN}'}

    songs = []
    while url is not None:
        response = requests.get(url, headers=headers)

        data = json.loads(response.content)
        songs.extend(data['items'])

        url = data['next']

    print("DONE")

    return songs


def pullArtists(songs):

    print("Pulling artists...", end="")

    artists = {}
    artist_data = []

    for song in songs:
        for artist in song['track']['artists']:
            artists[artist['id']] = {'name': artist['name']}

    batch_size = 50
    for x in range(0, math.ceil(len(artists) / batch_size)):

        current_pos = batch_size * x
        current_batch = list(artists.keys())[
            current_pos: current_pos + batch_size]
        ids = ','.join(current_batch)

        response = requests.get(
            f'https://api.spotify.com/v1/artists?ids={ids}', headers={'Authorization': f'Bearer {TOKEN}'})

        data = json.loads(response.content)
        artist_data.extend(data['artists'])

    print("DONE")

    return artist_data


def writeData(data, file):
    print(f'Writing {file}')
    with open(file, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    songs = pullLikedSongs()
    artists = pullArtists(songs)

    writeData(songs, './data/songs.json')
    writeData(artists, './data/artists.json')
