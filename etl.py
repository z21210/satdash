from extract import extract
from transform import transform
from load import load

import env

load(transform(extract()))