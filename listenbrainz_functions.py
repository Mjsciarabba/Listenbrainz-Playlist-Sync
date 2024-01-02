import re
import requests
from datetime import datetime, timedelta


from plex_functions import *
import global_variables as g
from musicbrainz_functions import *
from logger_utils import logger, get_tqdm_bar

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

track_list = []

# Get the current date
current_date = datetime.now()

# Calculate the difference in days between the current day and Monday (weekday 0)
days_to_monday = (current_date.weekday() - 0) % 7

# Subtract the difference to get the date of the most recent Monday
most_recent_monday = current_date - timedelta(days=days_to_monday)

# Format the date as 'YYYY-MM-DD'
formatted_date = most_recent_monday.strftime('%Y-%m-%d')

search_title = f"Weekly Jams for {cfg['playlist_username']}, week of {formatted_date} Mon"


def get_weeklyjams_playlist(user_token):
    """
    Goes through all the 'Created For' playlists and returns the 'Weekly Jams' playlist for the current week
    :param user_token: The Listenbrainz token for the user
    :return: The 'Weekly Jams' playlist info
    """
    username = cfg['playlist_username']

    try:
        logger.info("Getting playlists...")

        # Set up headers with the user token
        headers = {
            'Authorization': f'Token {user_token}',
            'Content-Type': 'application/json',
        }

        # Make a GET request to the ListenBrainz API to retrieve recommendations
        response = requests.get(f'https://api.listenbrainz.org/1/user/{username}/playlists/createdfor',
                                headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            logger.info("API call successful, parsing response...")

            # Parse the JSON response
            playlist_data = response.json()

            # Extract relevant information from the response
            playlists = playlist_data.get('playlists')

            # Find the playlist that is titled search_title
            for playlist in playlists:
                if playlist['playlist']['title'] == search_title:
                    playlist_mbid = playlist['playlist']['identifier'].split('/')[-1]

                    # Get the name of the second playlist
                    g.playlist_name = playlist['playlist']['title']
                    g.playlist_name = ' '.join(g.playlist_name.split(' ')[:2])

                    # Get the summary of the second playlist
                    g.playlist_summary = playlist['playlist']['annotation']
                    # Remove the HTML tags from the summary
                    g.playlist_summary = re.sub('<[^<]+?>', '', g.playlist_summary)
                    # Remove the newlines and extra spaces from the summary
                    g.playlist_summary = ' '.join(g.playlist_summary.split())

                    get_tracks_from_playlist(user_token, playlist_mbid)
                    break
            else:
                raise ValueError(f'No playlist found with title "{search_title}"')

        else:
            raise ValueError(f"Error getting playlists: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()


def get_tracks_from_playlist(user_token, playlist_mbid):
    """
    Retrieves all tracks and their related info for a specific playlist
    :param playlist_mbid: The Musicbrainz ID for the playlist to pull tracks from
    :param user_token: The Listenbrainz token for the user
    :return: A list of tracks from the searched playlist
    """
    try:
        logger.info("Getting tracks...")

        # Set up headers with the user token
        headers = {
            'Authorization': f'Token {user_token}',
            'Content-Type': 'application/json',
        }

        # Make a GET request to the ListenBrainz API to retrieve recommendations
        response = requests.get(f'https://api.listenbrainz.org/1/playlist/{playlist_mbid}',
                                headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            playlist_data = response.json()

            logger.info("API call successful, parsing response...")

            playlist_tracks = playlist_data['playlist']['track']

            # Iterate through tracks and access information
            for track_data in get_tqdm_bar(playlist_tracks):
                track_title = track_data['title']
                track_artist = track_data['creator']
                album_artist = track_data['extension']['https://musicbrainz.org/doc/jspf#track']['additional_metadata']['artists'][0]['artist_credit_name']
                mbids = get_specific_recording_mbids(track_data['identifier'].split('/')[-1])

                track_info = {
                    'title': track_title,
                    'artist': track_artist,
                    'album_artist': album_artist,
                    'mbids': mbids
                }
                # logger.info("Found info for track: " + track_title)
                track_list.append(track_info)

        else:
            print(f"Error getting tracks: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()

    logger.info("Parsing complete, searching for tracks...")

    search_for_track(track_list)
