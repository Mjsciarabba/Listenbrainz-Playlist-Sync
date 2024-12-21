import musicbrainzngs
import yaml
import modules.misc_utils as misc

from modules.logger_utils import logger

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)


email = cfg['api_email']

# Set your MusicBrainz API key
musicbrainzngs.set_useragent(app='ListenBrainzToPlex', version='1.0', contact=email)


# Function to get specific recording MBID and psuedo titles for a recording MBID
def get_track_mbids(recording_mbid):
    try:
        # Lists to store the MBIDs and titles
        mbids = []
        titles = []

        # Get information about the general recording using the MBID
        result = musicbrainzngs.search_recordings(rid=recording_mbid)

        # Extract specific recording MBID from the result
        for track in result['recording-list'][0]['release-list']:
            mbid = 'mbid://' + track['medium-list'][0]['track-list'][0]['id']
            mbids.append(mbid)

            track_title = track['medium-list'][0]['track-list'][0]['title']
            if misc.contains_japanese(track_title):
                continue
            titles.append(track_title)

        return mbids, titles

    except musicbrainzngs.ResponseError as e:
        logger.error(f"Error: {e}")
        return None



