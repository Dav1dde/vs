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
DEFAULT_EXPIRE = -1
MAX_EXPIRE = -1
CUSTOM_IDS = True
DISABLE_DELETE = False


try:
    from local_config import *
except ImportError:
    pass
