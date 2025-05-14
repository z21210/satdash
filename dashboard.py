import streamlit as st
import pandas as pd
import numpy as np
import sqlalchemy as sa
import os
import env
import time
import plotly.express as px

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
from plotly.colors import qualitative as colours
from sgp4.api import Satrec, SatrecArray

@st.cache_data
def fetch_satellite_data():
    # load data from database
    db, schema, table = os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')
    df = pd.read_sql_table(table, sa.create_engine(db), schema=schema, index_col='catalog_number')
    return df
df = fetch_satellite_data()


# UI layout
with st.sidebar:
    view = st.radio(
        'View',
        ['Data', 'Orbit', 'Groundtrack', 'Satellite']
    )
    if view in ['Orbit', 'Groundtrack']:
        selected = st.multiselect(
            'Search Satellites',
            df.index,
            format_func=lambda i: df.loc[i]['name'],
            default=[25544], # ISS
        )
        live = st.toggle(
            'Live view',
            disabled= view in ['Data', 'Satellite'],
            help='Plots will be re-rendered each interval'
        )
        interval = st.number_input(
            'Refresh interval (s)',
            disabled= view in ['Data', 'Satellite'] or not live,
            min_value=5,
            max_value=600,
            value=10
        )
    elif view == 'Satellite':
        selected = st.selectbox(
            'Search Satellites',
            df.index,
            format_func=lambda i: df.loc[i]['name'],
            index=df.index.get_loc(25544) # ISS
        )
plot = st.empty()

# if data view, render once
if view == 'Data':
    # cumulative satellite launches
    years = range(df['launch_year'].min(), df['launch_year'].max()+1)
    sats = [df[df['launch_year']<=y]['name'].nunique() for y in years]
    data = pd.DataFrame({'year':years, 'satellites':sats}).astype({'year':str})
    st.plotly_chart(px.line(data, x='year', y='satellites', title='Cumulative satellite launches'))
    # eccentricity histogram
    st.plotly_chart(px.histogram(df['eccentricity'], nbins=20, title='Eccentricity distribution'))
    # inclination histogram
    st.plotly_chart(px.histogram(df['inclination'], nbins=20, title='Inclination distribution'))
    # semi-major axis vs velocity plot
    st.plotly_chart(px.scatter(df, x='revolution_rate', y='semi-major_axis', title='Daily revolutions vs semi-major axis'))

elif view == 'Satellite':
    df.loc[selected]

# if plot view, render once or forever
else:
    while True:
        # initialise plotting variables
        plot.empty()
        gp = GroundtrackPlotter()
        op = OrbitPlotter(backend=Plotly3D())
        now = Time.now()
        jd, fr = now.jd1, now.jd2
        # calculate orbits
        satrecs = SatrecArray([Satrec.twoline2rv(*df.loc[s][['l1','l2']]) for s in selected])
        errs, poss, vels = satrecs.sgp4(np.array([jd]), np.array([fr]))
        for i in range(len(selected)):
            s = selected[i]
            if errs[i][0] != 0:
                continue
            orbit = Orbit.from_vectors(Earth, poss[i][0]<<u.km, vels[i][0]<<(u.km/u.s), epoch=now)
            colour = colours.Light24[i%len(colours.Light24)] # cycle through 24 colours
            # groundtrack
            if view == 'Groundtrack':
                gp.plot(
                    EarthSatellite(orbit, None),
                    time_range(
                        now-1.5*u.h, num_values=150, end=now+1.5*u.h
                    ),
                    label=df.loc[s]['name'],
                    color=colour,
                    line_style={
                        'color':colour
                    },
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
                    label=df.loc[s]['name'],
                    color=colour
                )
                with plot.container():
                    st.plotly_chart(op.backend.figure)
        # break or sleep before next loop
        if not live:
            break
        time.sleep(interval)