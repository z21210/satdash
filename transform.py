from astropy import units as u
from astropy.constants import GM_earth as mu
from math import tau

# a curse upon NORAD for this format
# may a thousand years of drive failures befall you
_non_standard_form2float = lambda s: (-1 if s[0]=='-' else 1) * float('.'+s[1:6]) *10**int(s[6:8])

def transform(df):
	# strip whitespace from name
	df['name'] = df['name'].str.strip()
	# last two digits of year; range is 1957 to 2056: y=1957+(y-57)%100
	df['launch_year'] = df['launch_year'].astype(int).sub(57).mod(100).radd(1957)
	# last two digits of year; range is 1957 to 2056: y=1957+(y-57)%100
	df['year'] = df['year'].astype(int).sub(57).mod(100).radd(1957)
	# unusual number format
	df['acceleration'] = df['acceleration'].map(_non_standard_form2float)
	df['drag'] = df['drag'].map(_non_standard_form2float)
	# assumed decimal point
	df['eccentricity'] = df['eccentricity'].radd('.').astype(float)
	# trivial casts
	df = df.astype({
		'catalog_number':int,
		'launch_number':int,
		'day':float,
		'velocity':float,
		'set_number':int,
		'inclination':float,
		'right_ascension':float,
		'periapsis_argument':float,
		'mean_anomaly':float,
		'revolution_rate':float,
		'revolutions':int
	})
	# datetime as decimal
	df['epoch'] = df['year'] + df['day'].div(365)
	# semi-major axis = Mu**(1/3) / (Tau * n / secs in day)**(2/3)
	df['semi-major_axis'] = df['revolution_rate'].mul(tau).div((1<<u.d << u.s).value).pow(2/3).rdiv(mu.value**(1/3))
	# drop ephemeris, year, and day
	df = df.drop(['ephemeris', 'year', 'day'], axis='columns')
	# set index
	df = df.set_index('catalog_number')
	return df