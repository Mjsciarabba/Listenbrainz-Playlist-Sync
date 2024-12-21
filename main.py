import yaml
from modules.listenbrainz_functions import get_playlists
from modules.plex_functions import set_section
import logging

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("musicbrainzngs").setLevel(logging.WARNING)
logging.getLogger("plexapi").setLevel(logging.WARNING)


if __name__ == "__main__":
    set_section()
    get_playlists(cfg['user_token'])
