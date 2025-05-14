from dotenv import load_dotenv
import sys
import os
import errno

try:
    if len(sys.argv) > 1:
        env = sys.argv[1]
        load_dotenv(f'.env.{env}', override=True)
    assert all(e is not None for e in [os.getenv('DB'), os.getenv('SCHEMA'), os.getenv('TABLE')])
except AssertionError:
    print(f'You must provide .env.{env} with DB, SCHEMA, and TABLE')
    sys.exit(errno.EINVAL)
except Exception as e:
    sys.exit(e.errno)