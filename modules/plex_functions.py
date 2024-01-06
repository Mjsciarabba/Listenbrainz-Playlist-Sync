import yaml
import plexapi.exceptions

from plexapi.server import PlexServer

import modules.global_variables as g
from modules.logger_utils import logger
from modules.misc_utils import *


with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)


plex = PlexServer(cfg['baseurl'], cfg['token'])

poster_path = cfg['poster_file_path']

plex_tracks = []  # Found tracks to be added to Plex
missing_tracks = []  # Any tracks that aren't found in Plex


def set_section():
    """
    Sets the Plex library section to search in
    """
    # Handle if the section name passed in is blank
    if cfg['music_section'] == "":
        # Throw an error
        raise ValueError("Section name cannot be blank.")

    # Set the section
    try:
        g.section = plex.library.section(cfg['music_section'])
    except plexapi.exceptions.NotFound:
        raise ValueError("Section not found.")


# Search through the Plex library for the track matching the name
def search_for_track(track_list: list[dict]):
    """
    Search through the Plex library for the track matching the names in the track_list
    :param track_list: List of tracks to search for
    """

    count = 0
    guid_match: bool = False

    for track in track_list:
        title = track['title']
        artist = track['artist']
        album_artist = track['album_artist']
        mbids = track['mbids']

        try:
            logger.info(f"Searching for {title}...")
            guid_match = False
            search_result = g.section.searchTracks(title=title)
            if not search_result:
                # Attempt Normalizing title and search again
                logger.warning("No match on first pass, attempting to normalize title...")
                normalized_title = normalize_characters(title)
                search_result = g.section.searchTracks(title=normalized_title)
                if not search_result:
                    logger.error(f"No match found for {title} after normalize, skipping...")
                    missing_tracks.append(track)
                    continue
                else:
                    logger.info(f"Found {search_result[0].title} - {search_result[0].artist().title} after Normalizing")
                    count += 1
                    plex_tracks.append(search_result[0])
            elif len(search_result) > 1:
                logger.warning(f"Found {len(search_result)} results for {title}, checking for exact match...")
                for result in search_result:
                    # Check to see if the result has a GUID
                    if not result.guids:
                        continue  # This means the result in Plex does not have a match
                    # Compare the guid of the result to the list of MBIDs
                    if result.guids[0].id in mbids:
                        logger.info(f"Found {result.title} - {result.artist().title} with GUID Matching")
                        count += 1
                        guid_match = True
                        plex_tracks.append(result)
                        break

                if not guid_match:
                    for result in search_result:
                        if result.artist().title == album_artist:
                            logger.info(f"Found {result.title} - {result.artist().title} with Artist Matching")
                            count += 1
                            plex_tracks.append(result)
                            break

                        # If on the last result and no match was found, add to missing tracks
                        if result == search_result[-1]:
                            logger.error(f"No match found for {title}, skipping...")
                            missing_tracks.append(track)
            else:
                # Match was found on first try
                logger.info(f"Found {search_result[0].title} - {search_result[0].artist().title} by Exact Match")
                count += 1
                plex_tracks.append(search_result[0])

        except plexapi.exceptions.NotFound:
            raise ValueError("Track not found.")

    logger.info(f"Found a total of {count} tracks")
    logger.warning(f"Missing {len(missing_tracks)} tracks: ")
    for track in missing_tracks:
        logger.debug(track['title'])

    create_playlist()


def create_playlist():
    """
    Creates a playlist in Plex. Will check if a playlist with the same name exists, and if it does it will
    replace/add tracks as needed
    """
    logger.info("Checking playlist status...")
    try:
        # Check if the playlist already exists
        playlist = g.section.playlist(g.playlist_name)
        logger.warning("Playlist already exists, checking for new tracks...")

        if playlist.items() == plex_tracks:
            logger.error("No new tracks found, skipping creation")
            return

        # Remove old tracks
        logger.info("New tracks found, updating playlist...")
        items = playlist.items()
        playlist.removeItems(items)
        logger.info("Old tracks removed from playlist")

        # Add new tracks
        playlist.addItems(plex_tracks)
        logger.info("Tracks added to playlist")

    except plexapi.exceptions.NotFound:
        try:
            logger.info("Playlist not found, creating...")
            playlist = g.section.createPlaylist(title=g.playlist_name, items=plex_tracks)
            if poster_path:
                playlist.uploadPoster(filepath=poster_path)
            playlist.edit(summary=g.playlist_summary)
            logger.info("Playlist created")
        except Exception as e:
            # Handle specific exception for playlist creation failure
            logger.error(f"Failed to create playlist: {e}")
            # Add additional actions or logging if needed
    except Exception as e:
        # Handle other specific exceptions if needed
        logger.error(f"An unexpected error occurred: {e}")
