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

daily_bool = cfg['create_daily']
weekly_bool = cfg['create_weekly']

patch_list = []

if daily_bool:
        patch_list.append('daily-jams')
if weekly_bool:
        patch_list.append('weekly-jams')

patch_set = set(patch_list)

# Convert patch_list to a normalized set for consistency
normalized_patch_set = {patch.strip().lower() for patch in patch_list}

# Dictionary to store the first match for each patch
first_matches = []

def get_playlists(user_token):
    """
    Goes through all the 'Created For' playlists and returns the designated playlist for the current week
    :param user_token: The ListenBrainz token for the user
    :return: The specified playlist's info
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
                # Extract and normalize the source_patch
                source_patch = \
                playlist['playlist']['extension']['https://musicbrainz.org/doc/jspf#playlist']['additional_metadata'][
                    'algorithm_metadata']['source_patch']
                normalized_source_patch = source_patch.strip().lower()

                # Check if the source_patch is in the normalized set
                if normalized_source_patch in normalized_patch_set and normalized_source_patch not in first_matches:
                    playlist_mbid = playlist['playlist']['identifier'].split('/')[-1]
                    first_matches.append(playlist_mbid)

                # Stop early if all patches have matches
                if len(first_matches) == len(normalized_patch_set):
                    break

        else:
            raise ValueError(f"Error getting playlists: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()

    # for mbid in first_matches:
    #     get_tracks_from_playlist(user_token, mbid)

    get_tracks_from_playlist(user_token, 'c866fcc3-7dfc-41c1-a5cc-a2b75c447e31')


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

        # Make a GET request to the ListenBrainz API to retrieve recommendations
        response = requests.get(f'https://api.listenbrainz.org/1/playlist/{playlist_mbid}',
                                headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            playlist_data = response.json()

            logger.info("API call successful, parsing response...")

            # Get the name of the playlist
            g.playlist_name = playlist_data['playlist']['title']
            g.playlist_name = ' '.join(g.playlist_name.split(' ')[:2])

            # Get the summary of the playlist
            g.playlist_summary = playlist_data['playlist']['annotation']
            # Remove the HTML tags from the summary
            g.playlist_summary = re.sub('<[^<]+?>', '', g.playlist_summary)
            # Remove the newlines and extra spaces from the summary
            g.playlist_summary = ' '.join(g.playlist_summary.split())

            logger.info(f'Loading track info for {g.playlist_name}')

            playlist_tracks = playlist_data['playlist']['track']

            # Iterate through tracks and access information
            for track_data in get_tqdm_bar(playlist_tracks):
                try:
                    track_title = track_data['title']
                    track_artist = track_data['creator']

                    # Safeguard against missing or empty artists
                    artists = track_data['extension']['https://musicbrainz.org/doc/jspf#track']['additional_metadata'].get(
                        'artists', [])
                    album_artist = artists[0].get('artist_credit_name', 'Unknown') if artists else 'Unknown'

                    # Safeguard against missing identifier
                    track_identifier = track_data.get('identifier', [])
                    if not track_identifier:
                        logger.warning(f"No identifier for track: {track_data}")
                        continue
                    identifier = str(track_identifier[0])

                    # Process the identifier
                    mbid = identifier.split('/')[-1]
                    track_mbids = get_track_mbids(mbid)

                    track_info = {
                        'title': track_title,
                        'artist': track_artist,
                        'album_artist': album_artist,
                        'mbids': track_mbids
                    }
                    # logger.info("Found info for track: " + track_title)
                    track_list.append(track_info)


                except Exception as e:
                    logger.error(f"Error processing track: {track_data['title']} - {e}")
                    # Skip problematic track but continue processing others
                    continue

        else:
            logger.error(f"Error getting tracks: {response.status_code} - {response.text}")
            exit()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()

    logger.info("Parsing complete, searching for tracks...")

    search_for_track(track_list)




