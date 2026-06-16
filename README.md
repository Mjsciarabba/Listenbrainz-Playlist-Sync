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

If running via Docker, place your `config.yml` in the folder you map to `/config` inside the container rather than the project directory.

#### Plex
The method for obtaining a Plex token is described here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

In the config file, enter your Plex library/section name containing your music, like so:
`music_section: 'Music'`

`filter_genre` is also optional. This field is used to filter out unwanted tracks by genre. A use case could be removing pesky Christmas songs infiltrating your playlist in the off-season.

`playlist_prefix` is optional. Playlists are "Weekly Jams" and "Daily Jams". If you want to put something in front to make them "A_Weekly Jams" or whatever, put it here. Leave it blank (two quotes '' ) to not use a prefix.

A completed Plex section looks like this:

```
# Plex Info
baseurl: '192.168.1.70:32400' 
token: 'abcdef123456789' 
music_section: 'Music' 
filter_genre: 'Christmas'
playlist_prefix: ''
```

#### ListenBrainz
Information on how to obtain the ListenBrainz token for your user can be found here: https://listenbrainz.readthedocs.io/en/latest/users/api/index.html#get-the-user-token

The `playlist_username` should be your ListenBrainz username

`api_email` is needed for the Musicbrainz API to make queries. You do not need to have a Musicbrainz account, and you 
can use any email address

`create_daily` and `create_weekly` allow you to set whether that playlist type will sync from ListenBrainz. By default, only `create_weekly` is set to `True`

`filter_words` is optional. This field is used to remove unnecessary words from track titles to help with matching tracks. There are some included values by default, however this list can be modified as needed

A completed ListenBrainz section looks like this:
```
# ListenBrainz Info
user_token: 'abcdef123456789' 
playlist_username: 'listenbrainz'
api_email: 'mail@example.com'
create_daily: False
create_weekly: True

filter_words: [
    "original mix",
    "radio edit",
    "single edit",
    "alternate mix",
    "remastered",
    "remaster",
    "single version",
    "retail mix",
    "quartet"
]
```

#### Posters
The posters field is optional. This is for if you want to upload a custom playlist cover instead of using the auto-generated one from Plex. This upload only happens during initial creation of the playlist. There are two options for posters currently, one for the 'Daily' and one for the 'Weekly' playlists. 

There is a 'Daily' poster I created based on the ListenBrainz generated ones. To use it, download it and place it in your config directory, and then set `daily_poster` to the filename.

A completed Posters section looks like this:
```
# Poster Info
daily_poster: 'Daily Jams.png'
weekly_poster: 'Weekly Jams.png'
```
### Step 4 - Install Requirements

Install the additional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`

### Step 5 - Run the Program
Now that configuration is finished and requirements have been installed, we can finally start the script:

`python main.py`

### Optional - Docker
A Dockerfile is included for running the script in a container. Build the image from the project directory:

`docker build -t listenbrainz-playlist-sync .`

Then run it with your config folder mounted:

`docker run -v /path/to/your/config:/config listenbrainz-playlist-sync`

For Unraid, set the container path to `/config` and point it at your appdata folder, then place your `config.yml` there.

### Optional - Schedule Task
You can have this script run on a regular basis automatically. Here's how to set it up

#### Windows Task Scheduler
1. Create a `Runner.cmd` file by opening the text editor (i.e. Notepad, TextEdit) and pasting the following code:
```
cd C:\Users\USERNAMEHERE\Listenbrainz Playlist Sync
python main.py
```
2. Open Task Scheduler by searching for it in the Start Menu or by opening the Run window (Windows + R) and typing taskschd.msc before hitting OK.
** Ensure that Task Scheduler is opened and not Task Manager **
3. Select "Create a basic task" on the right-hand column
4. Give the task a name, such as `Listenbrainz Sync` and then select "Next"
5. Choose the frequency that this should run.
6. Choose the action "Start a program" and select "Next".
7. Click "Browse", Navigate to the directory and choose `Runner.cmd`, which was created in Step 1, then select "Open".
8. Copy the directory everything up to but not including `Runner.cmd` from the "Program/Script" field, and paste it into the "Start in" field.
9. Click "Finish".
10. Click "Task Schedule Library" on the left. The "Listenbrainz Sync" task should be visible.

#### User Scripts (Unraid)
1. Install the User Scripts plugin from the Unraid Community Applications store if you haven't already
2. Navigate to Settings > User Scripts and click "Add New Script"
3. Give the script a name such as `Listenbrainz Sync` and click "OK"
4. Click the gear icon next to the script and select "Edit Script"
5. Paste the following code:

\```
#!/bin/bash
docker start listenbrainz
\```

6. Click "Save Changes"
7. Click the schedule dropdown next to the script and select "Custom"
8. Enter a cron schedule (for example `0 9 * * 1` to run every Monday at 9am)
9. Click "Apply"

## Requirements

[Python 3.11](https://www.python.org/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)

[ListenBrainz API](https://listenbrainz.readthedocs.io/en/latest/users/api/index.html)
