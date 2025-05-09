import requests as r
import pandas as pd

def _tle2dict(name, l1, l2):
	return {
		'name':name,
		'catalog_number':l1[2:7],
		'classification':l1[7:8],
		'launch_year':l1[9:11],
		'launch_number':l1[11:14],
		'piece':l1[14:17],
		'year':l1[18:20],
		'day':l1[20:32],
		'velocity':l1[33:43],
		'acceleration': l1[44:52],
		'drag':l1[53:61],
		'ephemeris':l1[62:63],
		'set_number':l1[64:68],
		'inclination':l2[8:16],
		'right_ascension':l2[17:25],
		'eccentricity':l2[26:33],
		'periapsis_argument':l2[34:42],
		'mean_anomaly':l2[43:51],
		'revolution_rate':l2[52:63],
		'revolutions':l2[63:68]
	}

_tles2dicts = lambda a: [_tle2dict(n,l1,l2) for n,l1,l2 in a]

def extract():
	resp = r.get('https://celestrak.org/NORAD/elements/gp.php?GROUP=active')
	lines = resp.text.split('\r\n')
	tles = [lines[i:i+3] for i in range(0, len(lines)-1, 3)]
	return pd.DataFrame(_tles2dicts(tles))
