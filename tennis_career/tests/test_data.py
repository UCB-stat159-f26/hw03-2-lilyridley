import pandas as pd
import pytest

from tennis_career import data
from tennis_career.data import _add_ages, _download_career_js, _format_name, _parse_matches, _select_columns

female_js = '''var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"],
  ["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0", "", "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"],
  ["19970804", "Manhattan Beach", "Hard", "W", "L", "", "", "WC", "Q3", "7-6 4-6 6-3", "3", "Magui Serna", "54", "6", "", "L", "19790301", "167", "ESP", "0", "", "", "", "", "", "", "1997-W-WT-USA-07A-1997-026"]]'''
male_js = '''var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-M-FU-ESP-10A-2001-002", "", "1", "1"],
  ["20010917", "Seville CH", "Clay", "C", "L", "", "", "WC", "R16", "3-6 6-1 6-3", "3", "Stefano Galvani", "161", "2", "", "R", "24.2902121834", "178", "ITA", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2", "", "", "", "2001-784-024", "", "2", "2"],
  ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", "18.7597535934", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-784-015", "", "1", "1"]]'''

def _clean_js(js_text, player_dob):
    df = _select_columns(_parse_matches(js_text))
    return _add_ages(df, pd.Timestamp(player_dob))

def test_format_name():
    # Test that the _format_name function accepts all styles
    for name in ['serena williams', 'Serena Williams', 'SerenaWilliams']:
        assert _format_name(name) == 'SerenaWilliams'

def test_female_opp_age_from_dob():
    # Test that the opponent's age in the female file comes from their date of birth
    df = _clean_js(female_js, '1981-09-26')
    assert len(df) == 3
    assert df.loc[0, 'opp_age'] == pytest.approx(18.78, abs=0.01)
    assert df.loc[0, 'age_diff'] == pytest.approx(-4.68, abs=0.01)

def test_male_opp_age_used_directly():
    # Test that the opponent's age in the male file is used directly
    df = _clean_js(male_js, '1986-06-03')
    assert len(df) == 3
    assert df.loc[0, 'opp_age'] == pytest.approx(22.26, abs=0.01)
    assert df.loc[0, 'age_diff'] == pytest.approx(-6.99, abs=0.01)

def test_unknown_player(monkeypatch):
    # Test that a clear error is raised for an unknown player
    class NotFound:
        status_code = 404
    monkeypatch.setattr(data.requests, 'get', lambda url, timeout=None: NotFound())
    with pytest.raises(ValueError, match='Could not find a player'):
        _download_career_js('LilyRidley')