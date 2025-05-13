import streamlit as st
import pandas as pd
import sqlalchemy as sa
import os
import env

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

# load data from database
db, schema, table = os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')
df = pd.read_sql_table(table, sa.create_engine(db), schema=schema, index_col='catalog_number')
# create Satrecs
df['satrec'] = df.apply(lambda s: Satrec.twoline2rv(*s[['l1','l2']]), axis=1)
# create plotters
gp = GroundtrackPlotter()
op = OrbitPlotter(backend=Plotly3D())

# UI layout
with st.sidebar:
    st.write("Select Satellites")
    selected = st.multiselect(
        "Select Satellites",
        df.index,
        format_func=lambda i: df.loc[i]['name'],
        default=[25544], # ISS
    )
tabGT, tabO = st.tabs(["Groundtrack", "Orbit"])
tabGT.plotly_chart(gp.fig)
tabO.plotly_chart(op.backend.figure)

# plot selected satellites
now = Time.now()
jd, fr = now.jd1, now.jd2
for s in selected:
    e, r, v = df.loc[s]['satrec'].sgp4(jd, fr)
    if e != 0:
        continue
    orbit = Orbit.from_vectors(Earth, r<<u.km, v<<(u.km/u.s), epoch=now)

    gp.plot(
        EarthSatellite(orbit, None),
        time_range(
            now-1.5*u.h, num_values=150, end=now+1.5*u.h
        ),
        label=df.loc[s]['name'],
        color="blue",
        marker={
            "size": 10,
            "symbol": "triangle-right",
            "line": {"width": 1, "color": "black"},
        },
    )
    op.plot(orbit)