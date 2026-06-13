from plexapi.library import MusicSection
import os
import yaml

# Chosen Variables
section: MusicSection
mbid: str

playlist_name: str
playlist_summary: str

config_path = os.environ.get("CONFIG_PATH", "config.yml")

with open(config_path, 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

