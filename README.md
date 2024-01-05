# ListenBrainz Playlist Sync for Plex

This is a Python project made to import the 'Weekly Jams' playlist from ListenBrainz into Plex.

## Setup
### Step 1 - Python
Make sure you have Python `3.11` or higher installed:

[Python homepage](https://www.python.org/)

### Step 2 - Download Project Files
Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/Mjsciarabba/Listenbrainz-Playlist-Sync/releases

### Step 3 - Configuration
From the project directory rename `config.yml.example` to `config.yml`, open `config.yml` with your text editor and edit where needed.

#### Plex
The method for obtaining a Plex token is described here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

In the config file enter your Plex library / section name containing your music, like so:
`music_section: 'Music'` 

The `poster_file_path` field is optional. This is for if you want to upload a custom playlist cover instead of using the 
auto-generated one from Plex. This upload only happens during initial creation of the playlist

A completed Plex section looks like this:

```
# Plex Info
baseurl: '192.168.1.70:32400' 
token: 'abcdef123456789' 
music_section: 'Music' 
poster_file_path: 'path\to\poster.png'
```

#### ListenBrainz
Information on how to obtain the ListenBrainz token for your user can be found here: https://listenbrainz.readthedocs.io/en/latest/users/api/index.html#get-the-user-token

The `playlist_username` should be your ListenBrainz username

`api_email` is needed for the Musicbrainz API to make queries. You do not need to have a Musicbrainz account, and you 
can use any email address

A completed ListenBrainz section looks like this:
```
# ListenBrainz Info
user_token: 'abcdef123456789' 
playlist_username: 'listenbrainz'
api_email: 'mail@example.com'
```

### Step 4 - Install Requirements

Install the additional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`

### Step 5 - Run the Program
Now that configuration is finished and requirements have been installed we can finally start the script:

`python main.py`

## Requirements

[Python 3.11 or higher](https://www.python.org/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)
[ListenBrainz API](https://listenbrainz.readthedocs.io/en/latest/users/api/index.html)