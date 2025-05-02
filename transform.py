from sgp4.api import Satrec, SatrecArray, jday
from time import gmtime

_gmt2jday = lambda t: jday(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
_json2sat = lambda j: Satrec.twoline2rv(j['line1'], j['line2'])

def transform(jsons):
	return SatrecArray([
		_json2sat(j)
	for j in jsons])
