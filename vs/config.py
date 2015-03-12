# ---
# Default Configuration
# ---

import os
import vs.database

# ---
# Flask
# ---
# This key MUST be changed before you make a site public, as it is used
# to sign the secure cookies used for sessions.
SECRET_KEY = 'ChangeMeOrGetHacked'

# ---
# Database
# ---
DATABASE = vs.database.Redis(
    host='localhost', port=6379, db=0
)

# ---
# Misc. Settings
# ---
# Default expiration setting in days (if expire tag is empty) (<= 0 infinite).
DEFAULT_EXPIRE = -1
# Maximum expiration in days (<= 0 infinite).
MAX_EXPIRE = -1
# Allow short-URL Ids
CUSTOM_IDS = True
# Disable deletion of short URLs
DISABLE_DELETE = False


try:
    from local_config import *
except ImportError:
    pass
