import requests as r
import logging

_sat_count = lambda j: j['parameters']['page-size'] * (j['parameters']['page'] - 1) + len(j['member'])
_sat_total = lambda j: j['totalItems']
_progress  = lambda j: f'{_sat_count(j)}/{_sat_total(j)}'

def fetch_sats():
	logging.warning('Fetching satellite data from API (if this is running frequently, something is misconfigured)')
	logging.info('This may take some time...')
	# get first page
	page = r.get('https://tle.ivanstanojevic.me/api/tle?page-size=100', headers={"User-Agent":"Mozilla/5.0"})
	sats = page.json()['member']
	logging.info(_progress(page.json()))
	while 'next' in page.json()['view']:
		# get next page
		page = r.get(page.json()['view']['next'], headers={"User-Agent":"Mozilla/5.0"})
		sats.extend(page.json()['member'])
		logging.info(_progress(page.json()))
	return sats

