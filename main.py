import yaml
from modules.listenbrainz_functions import get_playlists
from modules.plex_functions import set_section

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

if __name__ == "__main__":
    set_section()
    get_playlists(cfg['user_token'])
