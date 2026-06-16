from plexapi.library import MusicSection
import os
import yaml

# Chosen Variables
section: MusicSection
mbid: str

playlist_name: str
playlist_summary: str

poster_path: str

base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.normpath(os.path.join(base_dir, ".."))
config_path = os.environ.get("CONFIG_PATH") or os.path.join(root_dir, "config.yml")
config_dir = os.path.dirname(os.path.abspath(config_path))

with open(config_path, 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

