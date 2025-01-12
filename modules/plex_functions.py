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


def search_for_track(track_list: list[dict]):
    """
    Search through the Plex library for the track matching the names in the track_list
    :param track_list: List of tracks to search for
    """
    count = 0
    plex_tracks.clear()
    missing_tracks.clear()

    for track in track_list:
        title = track['title']
        artist = track['artist']
        album_artist = track['album_artist']
        mbids = track['mbids']
        pseudo_titles = track['pseudo_titles']

        try:
            logger.debug(f"Searching for {title}...")
            search_result = search_with_fallbacks(title, pseudo_titles)

            if not search_result:
                logger.error(f"No match found for {title}, skipping...")
                missing_tracks.append(track)
                continue

            matched_track = match_track(search_result, mbids, album_artist)

            if matched_track:
                plex_tracks.append(matched_track)
                count += 1
                logger.info(f"Successfully matched: {matched_track.title} - {matched_track.artist().title}")
            else:
                logger.error(f"No suitable match found for {title}, skipping...")
                missing_tracks.append(track)

        except plexapi.exceptions.NotFound:
            logger.error(f"Track {title} not found in Plex.")
            missing_tracks.append(track)
        except Exception as e:
            logger.error(f"An unexpected error occurred while processing {title}: {e}")
            missing_tracks.append(track)

    logger.info(f"Found a total of {count} tracks")
    logger.warning(f"Missing {len(missing_tracks)} tracks:")
    for track in missing_tracks:
        logger.debug(track['title'])

    # After processing all tracks, create the playlist
    create_playlist()


def search_with_fallbacks(title, pseudo_titles):
    """
    Search for a track with normalization and pseudo-title fallbacks.
    """
    search_result = g.section.searchTracks(title=title)
    if search_result:
        return search_result

    logger.warning(f"No match for {title}, attempting normalization...")
    normalized_title = normalize_characters(title)
    search_result = g.section.searchTracks(title=normalized_title)
    if search_result:
        return search_result

    if pseudo_titles:
        logger.warning(f"No match after normalization, attempting pseudo-titles...")
        for pseudo_title in pseudo_titles:
            print(pseudo_title)
            search_result = g.section.searchTracks(title=pseudo_title)
            if search_result:
                return search_result

    return None


def match_track(search_result, mbids, album_artist):
    """
    Find the best match from search results based on GUIDs and artist matching.
    """

    logger.warning("Multiple results found, attempting to match with GUID...")
    for result in search_result:
        if result.guids and result.guids[0].id in mbids:
            logger.info(f"Match found via GUID: {result.title} - {result.artist().title}")
            return result

    logger.warning(f"No GUID match found, attempting to match with artist name...")
    for result in search_result:
        if result.artist().title == album_artist:
            logger.info(f"Match found via artist name: {result.title} - {result.artist().title}")
            return result

    return None

def create_playlist():
    """
    Creates a playlist in Plex. Will check if a playlist with the same name exists, and if it does it will
    replace/add tracks as needed
    """

    filter_tracks()

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
            if poster_path != 'YOUR_FILE_PATH':
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


def filter_tracks():
    """
    Filters out tracks by genre before creating/modifying the playlist.
    :return:
    """
    filter_genre = cfg['filter_genre']
    if filter_genre != 'YOUR_GENRE':
        for item in plex_tracks:
            track_album = item.album()
            genres = track_album.genres
            for album_genre in genres:
                if album_genre.tag == filter_genre:
                    logger.info(f'Track "{item.title}" removed due to genre filter.')
                    plex_tracks.remove(item)
                    continue


