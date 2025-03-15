# ListenBrainz Playlist Sync for Plex

This is a Python project made to import the 'Weekly Jams' playlist from ListenBrainz into Plex.

## Setup
### Step 1 - Python
Make sure you have Python `3.11` installed:

[Python homepage](https://www.python.org/)

### Step 2 - Download Project Files
Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/Mjsciarabba/Listenbrainz-Playlist-Sync/releases

### Step 3 - Configuration
In the project directory rename `config.yml.example` to `config.yml`, open `config.yml` with your text editor and edit where needed.

#### Plex
The method for obtaining a Plex token is described here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

In the config file, enter your Plex library/section name containing your music, like so:
`music_section: 'Music'` 

The `poster_file_path` field is optional. This is for if you want to upload a custom playlist cover instead of using the 
auto-generated one from Plex. This upload only happens during initial creation of the playlist

`filter_genre` is also optional. This field is used to filter out unwanted tracks by genre. A use case could be removing pesky Christmas songs infiltrating your playlist in the off-season.

`playlist_prefix` is optional. Playlists are "Weekly Jams" and "Daily Jams". If you want to put something in front to make them "A_Weekly Jams" or whatever, put it here. Leave it blank (two quotes '' ) to not use a prefix.

A completed Plex section looks like this:

```
# Plex Info
baseurl: '192.168.1.70:32400' 
token: 'abcdef123456789' 
music_section: 'Music' 
poster_file_path: 'path\to\poster.png'
filter_genre: 'Christmas'
playlist_prefix: ''
```

#### ListenBrainz
Information on how to obtain the ListenBrainz token for your user can be found here: https://listenbrainz.readthedocs.io/en/latest/users/api/index.html#get-the-user-token

The `playlist_username` should be your ListenBrainz username

`api_email` is needed for the Musicbrainz API to make queries. You do not need to have a Musicbrainz account, and you 
can use any email address

`create_daily` and `create_weekly` allow you to set whether that playlist type will sync from ListenBrainz. By default, only `create_weekly` is set to `True`

A completed ListenBrainz section looks like this:
```
# ListenBrainz Info
user_token: 'abcdef123456789' 
playlist_username: 'listenbrainz'
api_email: 'mail@example.com'
create_daily: False
create_weekly: True
```

### Step 4 - Install Requirements

Install the additional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`

### Step 5 - Run the Program
Now that configuration is finished and requirements have been installed, we can finally start the script:

`python main.py`

### Optional - Schedule Task
Using the Windows Task Scheduler, you can have this script run on a weekly basis automatically. Here's how to set it up:

1. Create a `Runner.cmd` file by opening the text editor (i.e. Notepad, TextEdit) and pasting the following code:
```
cd C:\Users\USERNAMEHERE\Listenbrainz Playlist Sync
python main.py
```
2. Open Task Scheduler by searching for it in the Start Menu or by opening the Run window (Windows + R) and typing taskschd.msc before hitting OK.
** Ensure that Task Scheduler is opened and not Task Manager **
3. Select "Create a basic task" on the right-hand column
4. Give the task a name, such as `Listenbrainz Sync` and then select "Next"
5. Choose the frequency that this should run, `Weekly` is suggested.
6. Choose the action "Start a program" and select "Next".
7. Click "Browse", Navigate to the directory and choose `Runner.cmd`, which was created in Step 1, then select "Open".
8. Copy the directory everything up to but not including `Runner.cmd` from the "Program/Script" field, and paste it into the "Start in" field.
9. Click "Finish".
10. Click "Task Schedule Library" on the left. The "Listenbrainz Sync" task should be visible.


## Requirements

[Python 3.11](https://www.python.org/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)

[ListenBrainz API](https://listenbrainz.readthedocs.io/en/latest/users/api/index.html)
