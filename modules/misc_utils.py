from datetime import datetime, timedelta


def get_weekly_playlist_title(username: str):
    """
    Gets the date of the most recent Monday and formats it for the title to search for
    :param username: The username for the playlist
    :return: The formatted title to search for
    """
    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in days between the current day and Monday (weekday 0)
    days_to_monday = (current_date.weekday() - 0) % 7

    # Subtract the difference to get the date of the most recent Monday
    most_recent_monday = current_date - timedelta(days=days_to_monday)

    # Format the date as 'YYYY-MM-DD'
    formatted_date = most_recent_monday.strftime('%Y-%m-%d')

    title = f"Weekly Jams for {username}, week of {formatted_date} Mon"

    return title


def get_daily_playlist_title(username: str):
    """
    Gets the date of the most recent Monday and formats it for the title to search for
    :param username: The username for the playlist
    :return: The formatted title to search for
    """
    # Get the current date
    current_date = datetime.now()

    # Get the abbreviated weekday name
    day_abbreviation = current_date.strftime("%a")

    # Format the date as 'YYYY-MM-DD'
    formatted_date = current_date.strftime('%Y-%m-%d')

    title = f"Daily Jams for {username}, {formatted_date} {day_abbreviation}"

    return title


def normalize_characters(title: str):
    """
    Swaps certain mapped characters in a title in order to get a better match
    :param title: The original track title
    :return: The normalized title
    """
    char_mapping = {
        '...': chr(8230),
        '“': '"',
        '”': '"',
        '’': "'",
        '‐': ' ',
    }

    for key, value in char_mapping.items():
        title = title.replace(key, value)

    return title
