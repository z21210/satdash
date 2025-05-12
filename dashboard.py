import streamlit as st
import pandas as pd
import sqlalchemy as sa
import os
import env

#db, schema, table = os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')
#df = pd.read_sql_table(table, sa.create_engine(db), schema=schema)

from astropy import units as u
from hapsira.earth import EarthSatellite
from hapsira.earth.plotting import GroundtrackPlotter
from hapsira.examples import iss
from hapsira.util import time_range
from hapsira.bodies import Earth, Sun
from hapsira.constants import J2000
from hapsira.plotting import OrbitPlotter
from hapsira.plotting.orbit.backends import Plotly3D
from hapsira.twobody import Orbit

iss_spacecraft = EarthSatellite(iss, None)
t_span = time_range(
    iss.epoch - 1.5 * u.h, num_values=150, end=iss.epoch + 1.5 * u.h
)
# Generate an instance of the plotter, add title and show latlon grid
gp = GroundtrackPlotter()
gp.update_layout(title="International Space Station groundtrack")

frame = OrbitPlotter(backend=Plotly3D())
frame.plot(iss)

with st.sidebar:
    st.write("Select Satellites")
    options = st.multiselect(
    "Select Satellites",
    ["ISS (ZARYA)"],
    default=["ISS (ZARYA)"],
)
tabGT, tabO = st.tabs(["Groundtrack", "Orbit"])

tabGT.plotly_chart(gp.plot(
    iss_spacecraft,
    t_span,
    label="ISS",
    color="red",
    marker={
        "size": 10,
        "symbol": "triangle-right",
        "line": {"width": 1, "color": "black"},
    },
))
tabO.plotly_chart(frame.backend.figure)
