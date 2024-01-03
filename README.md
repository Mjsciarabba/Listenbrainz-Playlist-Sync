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
From the project directory rename `config.yml.example` to `config.yml`, open `config.yml` with your text editor and edit where needed.

#### Plex
The method for obtaining a Plex token is described here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

In the config file enter your Plex library / section name containing your Music, like so:
`music_section: 'Music'` 

A completed Plex section looks like this:

```
# Plex Info
baseurl: '192.168.1.70:32400' 
token: 'abcdef123456789' 
music_section: 'Music' 
poster_file_path: 'path\to\poster.png'
```

#### Listenbrainz
Information on how to obtain the Listenbrainz token for your user can be found here: https://listenbrainz.readthedocs.io/en/latest/users/api/index.html#get-the-user-token

The `playlist_username` should be your Listenbrainz username

A completed Listenbrainz section looks like this:
```
# Listenbrainz Info
user_token: 'abcdef123456789' 
playlist_username: 'listenbrainz'
```

### Step 4 - Install Requirements

Install the addtional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`

### Step 5 - Run the Program
Now that configuration is finished and requirements have been installed we can finally start the script:

`python main.py`

## Requirements

[Python 3.11 or higher](https://www.python.org/)

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)