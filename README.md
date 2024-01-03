# Listenbrainz Playlist Sync for Plex

This is a Python project made to import the 'Weekly Jams' playlist from Listenbrainz into Plex.

## Setup
### Step 1 - Python
Make sure you have Python 3.11 or higher installed:

[Python homepage](https://www.python.org/)

### Step 2 - Download Project Files
Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/Mjsciarabba/Listenbrainz-Playlist-Sync/releases

### Step 3 - Configuration
From the project directory rename `config.yml.example` to `config.yml`, open `config.yml` with your favorite text editor and edit where needed.

### Step 4 - Install Requirements

Install the addtional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`

### Step 5 - Run the Program
Now that configuration is finished and requirements have been installed we can finally start the script:

`python main.py`

## Requirements

[Python 3.7 or higher](https://www.python.org/)

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)