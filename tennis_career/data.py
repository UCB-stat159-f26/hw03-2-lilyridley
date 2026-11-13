import requests

def _format_name(player_name):
    '''Formats the player's name to "FirstLast"'''
    words = str(player_name).split()
    return ''.join(word[0].upper() + word[1:] for word in words)

def _download_career_js(formatted_name):
    '''Return the raw career JS text or raise an error if the player is not found'''
    url = f'https://www.tennisabstract.com/jsmatches/{formatted_name}Career.js'
    response = requests.get(url, timeout=30)
    if response.status_code != 200:
        raise ValueError(f'Could not find a player named "{formatted_name}". Make sure to check the spelling.')
    return response.text

def get_player_career(player_name):
    '''Return a clean DataFrame of a player's career matches'''
    raise NotImplementedError