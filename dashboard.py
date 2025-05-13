import streamlit as st
import pandas as pd
import sqlalchemy as sa
import os
import env
import time

from astropy import units as u
from astropy.time import Time
from hapsira.util import time_range
from hapsira.constants import J2000
from hapsira.bodies import Earth
from hapsira.twobody import Orbit
from hapsira.earth import EarthSatellite
from hapsira.plotting.orbit.backends import Plotly3D
from hapsira.plotting import OrbitPlotter
from hapsira.earth.plotting import GroundtrackPlotter
from sgp4.api import Satrec

@st.cache_data
def fetch_satellite_data():
    # load data from database
    db, schema, table = os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')
    df = pd.read_sql_table(table, sa.create_engine(db), schema=schema, index_col='catalog_number')
    return df
df = fetch_satellite_data()

# UI layout
with st.sidebar:
    st.write('Select Satellites')
    view = st.radio(
        'View',
        ['Groundtrack', 'Orbit', 'Data']
    )
    selected = st.multiselect(
        'Search Satellites',
        df.index,
        format_func=lambda i: df.loc[i]['name'],
        default=[25544], # ISS
    )
    live = st.toggle(
        'Live view',
        disabled= view=='Data',
        help='Plots will be re-rendered each interval'
    )
    interval = st.number_input(
        'Refresh interval (s)',
        disabled= view=='Data' or not live,
        min_value=5,
        max_value=600,
        value=10
    )
plot = st.empty()


# create Satrecs
df['satrec'] = df.apply(lambda s: Satrec.twoline2rv(*s[['l1','l2']]), axis=1)


# if data view, render once
if view == 'Data':
    pass
# if plot view, render once or forever
else:
    while True:
        plot.empty()
        gp = GroundtrackPlotter()
        op = OrbitPlotter(backend=Plotly3D())
        now = Time.now()
        jd, fr = now.jd1, now.jd2
        for s in selected:
            e, r, v = df.loc[s]['satrec'].sgp4(jd, fr)
            if e != 0:
                continue
            orbit = Orbit.from_vectors(Earth, r<<u.km, v<<(u.km/u.s), epoch=now)
            # groundtrack
            if view == 'Groundtrack':
                gp.plot(
                    EarthSatellite(orbit, None),
                    time_range(
                        now-1.5*u.h, num_values=150, end=now+1.5*u.h
                    ),
                    label=df.loc[s]['name'],
                    color='blue',
                    marker={
                        'size': 10,
                        'symbol': 'triangle-right',
                        'line': {'width': 1, 'color': 'black'},
                    },
                )
                with plot.container():
                    st.plotly_chart(gp.fig)
            # orbit
            elif view == 'Orbit':
                op.plot(
                    orbit,
                    label=df.loc[s]['name']
                )
                with plot.container():
                    st.plotly_chart(op.backend.figure)
        # break or sleep before next loop
        if not live:
            break
        time.sleep(interval)