# a curse upon NORAD for this format
# may a thousand years of drive failures befall you
_non_standard_form2float = lambda s: (-1 if s[0]=='-' else 1) * float('.'+s[1:6]) *10**int(s[6:8])

def transform(df):
	# strip whitespace from name
	df['name'] = df['name'].str.strip()
	# last two digits of year; range is 1957 to 2056: y=1957+(y-57)%100
	df['launch_year'] = df['launch_year'].astype(int).sub(57).mod(100).radd(1957)
	# unusual number format
	df['acceleration'] = df['acceleration'].map(_non_standard_form2float)
	df['drag'] = df['drag'].map(_non_standard_form2float)
	# assumed decimal point
	df['eccentricity'] = df['eccentricity'].radd('.').astype(float)
	# trivial casts
	df = df.astype({
		'catalog_number':int,
		'launch_number':int,
		'year':int,
		'day':float,
		'velocity':float,
		'set_number':int,
		'right_ascension':float,
		'periapsis_argument':float,
		'mean_anomaly':float,
		'revolution_rate':float,
		'revolutions':int
	})
	df = df.set_index('catalog_number')
	return df