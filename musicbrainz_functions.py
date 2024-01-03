import musicbrainzngs
import logging

from logger_utils import logger

# Set your MusicBrainz API key
musicbrainzngs.set_useragent("ListenbrainzToPlex", "1.0", "mjsciarabba72@gmail.com")

logging.getLogger("musicbrainzngs").setLevel(logging.WARNING)

mbids = []


# Function to get specific recording MBID for a general recording MBID
def get_track_mbids(recording_mbid):
    """
    Searches and returns all track IDs for a recording
    :param recording_mbid: The recording ID from Musicbrainz
    :return: All track IDs associated with a recording
    """
    try:
        # Get information about the general recording using the MBID
        result = musicbrainzngs.search_recordings(rid=recording_mbid)

        # Extract specific recording MBID from the result
        for track in result['recording-list'][0]['release-list']:
            mbid = 'mbid://' + track['medium-list'][0]['track-list'][0]['id']
            mbids.append(mbid)

        return mbids

    except musicbrainzngs.ResponseError as e:
        logger.error(f"Error: {e}")
        return None
