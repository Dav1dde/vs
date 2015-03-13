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
# Default domain configuration
# ---
DEFAULTS = {
    # Default expiration setting in days (if expire tag is empty)
    # (<= 0 infinite).
    'default_expiry': -1,
    # Maximum expiration in days (<= 0 infinite).
    'max_expiry': -1,
    # Allow short-URL Ids
    'custom_ids': True
}

# ---
# Misc
# ---
API_KEY = 'YouShouldChangeThisAsWell'


try:
    from local_config import *
except ImportError:
    pass
