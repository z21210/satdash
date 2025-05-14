import pytest
from unittest import mock
import pandas as pd

from extract import _tle2dict, _tles2dicts
from transform import _non_standard_form2float
from load import load

tles = [
    [
        'ISS (ZARYA)             ',
        '1 25544U 98067A   25134.41202909  .00008278  00000+0  15542-3 0  9996',
        '2 25544  51.6346 114.3865 0002299 108.9329 251.1909 15.49522137509920'
    ],
    [
        'TIANZHOU-8              ',
        '1 61983U 24211A   25133.68386206  .00028629  00000+0  32321-3 0  9990',
        '2 61983  41.4647 230.3574 0006465 265.0803  94.9298 15.61825384 24666'
    ]
]

dicts = [
    {
        'name':'ISS (ZARYA)             ',
        'l1':'1 25544U 98067A   25134.41202909  .00008278  00000+0  15542-3 0  9996',
        'l2':'2 25544  51.6346 114.3865 0002299 108.9329 251.1909 15.49522137509920',
        'catalog_number':'25544',
        'classification':'U',
        'launch_year':'98',
        'launch_number':'067',
        'piece': 'A  ',
        'year': '25',
        'day': '134.41202909',
        'velocity': ' .00008278',
        'acceleration': ' 00000+0',
        'drag': ' 15542-3',
        'ephemeris': '0',
        'set_number': ' 999',
        'inclination': ' 51.6346',
        'right_ascension': '114.3865',
        'eccentricity': '0002299',
        'periapsis_argument': '108.9329',
        'mean_anomaly': '251.1909',
        'revolution_rate': '15.49522137',
        'revolutions': '50992'
    },
    {
        'name': 'TIANZHOU-8              ',
        'l1': '1 61983U 24211A   25133.68386206  .00028629  00000+0  32321-3 0  9990',
        'l2': '2 61983  41.4647 230.3574 0006465 265.0803  94.9298 15.61825384 24666',
        'catalog_number': '61983',
        'classification': 'U',
        'launch_year': '24',
        'launch_number': '211',
        'piece': 'A  ',
        'year': '25',
        'day': '133.68386206',
        'velocity': ' .00028629',
        'acceleration': ' 00000+0',
        'drag': ' 32321-3',
        'ephemeris': '0',
        'set_number': ' 999',
        'inclination': ' 41.4647',
        'right_ascension': '230.3574',
        'eccentricity': '0006465',
        'periapsis_argument': '265.0803',
        'mean_anomaly': ' 94.9298',
        'revolution_rate': '15.61825384',
        'revolutions': ' 2466'
    }
]

def test_tle2dict():
    assert _tle2dict(*(tles[0])) == dicts[0]

def test_tles2dicts():
    assert _tles2dicts(tles) == dicts

def test_non_standard_form2float():
    assert _non_standard_form2float('-11606-4') == -0.11606*10**-4

def test_load():
    df = mock.MagicMock()
    with mock.patch.dict('os.environ', {'DB':'sqlite:///:memory:', 'SCHEMA':'', 'TABLE':'test'}):
        load(df)
    df.to_sql.assert_called_once_with('test', mock.ANY, schema='', if_exists='replace')