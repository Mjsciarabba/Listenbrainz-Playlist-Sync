import re
import requests


from modules.plex_functions import *
import modules.global_variables as g
from modules.musicbrainz_functions import *
from modules.logger_utils import logger, get_tqdm_bar
from modules.misc_utils import *

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

track_list = []

def get_dailyjams_playlist(user_token):
    """
    Goes through all the 'Created For' playlists and returns the 'Weekly Jams' playlist for the current week
    :param user_token: The ListenBrainz token for the user
    :return: The 'Weekly Jams' playlist info
    """
    username = cfg['playlist_username']

    search_title = get_playlist_daily_title(username)
    logger.info(search_title)
    # logger.info("---------------------------"+search_title)

    try:
        get_playlist(username,user_token,search_title)
    except Exception as e:
        logger.error(f"Unable to create Weekly Exploration playlist")

def get_weeklyjams_playlist(user_token):
    """
    Goes through all the 'Created For' playlists and returns the 'Weekly Jams' playlist for the current week
    :param user_token: The ListenBrainz token for the user
    :return: The 'Weekly Jams' playlist info
    """
    username = cfg['playlist_username']

    search_title = get_playlist_title(username)
    logger.info(search_title)
    logger.info("---------------------------"+search_title)

    try:
        get_playlist(username,user_token,search_title)
    except Exception as e:
        logger.error(f"Unable to create Weekly Exploration playlist")


def get_weeklyexploration_playlist(user_token):
    """
    Goes through all the 'Created For' playlists and returns the 'Weekly Exploration' playlist for the current week
    :param user_token: The ListenBrainz token for the user
    :return: The 'Weekly Exploration' playlist info
    """
    username = cfg['playlist_username']

    search_title = get_playlist_exploration_title(username)
    logger.info(search_title)
    logger.info("---------------------------"+search_title)

    try:
        get_playlist(username,user_token,search_title)
    except Exception as e:
        logger.error(f"Unable to create Weekly Exploration playlist")



def get_playlist(username, user_token, search_title):
    """
    Goes through all the 'Created For' playlists and returns the 'Weekly Exploration' playlist for the current week
    :param username: The ListenBrainz username for the user
    :param user_token: The ListenBrainz token for the user
    :param search_title: Search string for the playlist title
    :return: The 'Weekly Exploration' playlist info
    """
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
                if search_title in playlist['playlist']['title']:
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
    :param user_token: The ListenBrainz token for the user
    :return: A list of tracks from the searched playlist
    """
    try:
        logger.info("Getting tracks...")

        # Set up headers with the user token
        headers = {
            'Authorization': f'Token {user_token}',
            'Content-Type': 'application/json',
        }

        # Make a GET request to the ListenBrainz API to retrieve playlist data
        response = requests.get(f'https://api.listenbrainz.org/1/playlist/{playlist_mbid}',
                                headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            playlist_data = response.json()
            logger.info("API call successful, parsing response...")

            playlist_tracks = playlist_data.get('playlist', {}).get('track', [])
            if not playlist_tracks:
                logger.warning("No tracks found in the playlist.")
                return

            # Iterate through tracks and access information
            for track_data in get_tqdm_bar(playlist_tracks):
                try:
                    track_title = track_data.get('title', 'Unknown Title')
                    track_artist = track_data.get('creator', 'Unknown Artist')

                    # Navigate nested structure safely
                    artist_info = (
                        track_data.get('extension', {})
                        .get('https://musicbrainz.org/doc/jspf#track', {})
                        .get('additional_metadata', {})
                        .get('artists', [])
                    )

                    album_artist = artist_info[0].get('artist_credit_name') if artist_info else 'Unknown Album Artist'

                    identifier_list = track_data.get('identifier', [])
                    if not identifier_list:
                        logger.warning(f"Missing identifier for track: {track_title}")
                        continue

                    identifier = str(identifier_list[0])
                    track_mbids = get_track_mbids(identifier.split('/')[-1])

                    track_info = {
                        'title': track_title,
                        'artist': track_artist,
                        'album_artist': album_artist,
                        'mbids': track_mbids
                    }

                    track_list.append(track_info)

                except Exception as track_error:
                    logger.warning(f"Skipping track due to error: {track_error}")

        else:
            logger.error(f"Error getting tracks: {response.status_code} - {response.text}")
            exit()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()

    logger.info("Parsing complete, searching for tracks...")
    search_for_track(track_list)

