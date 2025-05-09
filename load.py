import pandas as pd
import sqlalchemy as sa
import os

def load(df):
    db, schema, table = os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')
    engine = sa.create_engine(db)
    df.to_sql(table, engine, schema=schema, if_exists='replace')