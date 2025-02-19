import yaml
from modules.listenbrainz_functions import get_weeklyjams_playlist,get_weeklyexploration_playlist,get_dailyjams_playlist
from modules.plex_functions import set_section
from datetime import date
import calendar

from modules.logger_utils import logger


with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

if __name__ == "__main__":
    my_date = date.today()
    today = calendar.day_name[my_date.weekday()]
    logger.info("today is "+today)

    set_section()
    get_dailyjams_playlist(cfg['user_token'])
    if today == "Monday":
      get_weeklyjams_playlist(cfg['user_token'])
    #get_weeklyexploration_playlist(cfg['user_token'])
