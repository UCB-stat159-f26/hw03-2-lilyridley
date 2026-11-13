import pandas as pd
import requests
import json
import re

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

def _parse_matches(js_text):
    '''Turn the raw JS text into a list of match rows'''
    array_text = js_text[js_text.index('['): js_text.rindex(']') + 1]
    return json.loads(array_text)

def _select_columns(matches):
    '''Select only the necessary columns'''
    df = pd.DataFrame(matches)[[0, 1, 2, 4, 11, 16]].copy()
    df.columns = ['date', 'tournament', 'surface', 'result', 'opponent', 'opp_dob_or_age']
    return df

def _get_player_dob(formatted_name):
    '''Read the player's date of birth from their tennisabstract page'''
    url = f'https://www.tennisabstract.com/cgi-bin/player.cgi?p={formatted_name}'
    match = re.search(r'var dob = (\d{8});', requests.get(url, timeout=30).text)
    if match is None:
        raise ValueError(f'Could not find a birth date for "{formatted_name}".')
    return pd.to_datetime(match.group(1), format='%Y%m%d')

def _get_opp_age(df):
    '''Opponent age in years: given directly (men) or computed from the DOB (women)'''
    values = pd.to_numeric(df['opp_dob_or_age'], errors='coerce')
    dob = pd.to_datetime(df['opp_dob_or_age'], format='%Y%m%d', errors='coerce')
    age_from_dob = (df['date'] - dob).dt.days / 365.25
    return values.where(values < 1000, age_from_dob)

def _add_ages(df, player_dob):
    '''Convert dates, then add player_age, opp_age, and age_diff'''
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['player_age'] = (df['date'] - player_dob).dt.days / 365.25
    df['opp_age'] = _get_opp_age(df)
    df['age_diff'] = df['player_age'] - df['opp_age']
    return df.drop(columns='opp_dob_or_age')

def get_player_career(player_name):
    '''Return a clean DataFrame of a player's career matches'''
    name = _format_name(player_name)
    matches = _parse_matches(_download_career_js(name))
    return _add_ages(_select_columns(matches), _get_player_dob(name))