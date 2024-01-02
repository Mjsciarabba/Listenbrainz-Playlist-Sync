from listenbrainz_functions import *

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

if __name__ == "__main__":
    set_section()
    get_weeklyjams_playlist(cfg['user_token'])

