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
    host='localhost', port=4999, db=0
)

# ---
# Misc. Settings
# ---
DEFAULT_EXPIRE = 10
MAX_EXPIRE = 100
CUSTOM_IDS = True
DISABLE_DELETE = False
