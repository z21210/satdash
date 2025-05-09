from dotenv import load_dotenv
import sys
import os
import errno
from extract import extract
from transform import transform
from load import load

try:
    env = sys.argv[1]
    assert load_dotenv(f'.env.{env}', override=True)
    assert all(e is not None for e in [os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')])
except IndexError:
    print('You must specify environment')
    sys.exit(errno.EINVAL)
except AssertionError:
    print(f'You must provide .env.{env} with DB, SCHEMA, and TABLE')
    sys.exit(errno.EINVAL)
except Exception as e:
    sys.exit(e.errno)

load(transform(extract()))