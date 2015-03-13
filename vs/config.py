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
    'custom_ids': True,
    # An aliased domain will share the short links of the alias, but
    # *NOT* its configuration!
    # If you do not want to use multi-domain support, set this value
    # (e.g. to 'default') and every domain will share the same short links,
    # This behaviour can be changed on a per domain basis via the API.
    # If a domain alias is set all previously configured
    # short URLs are ignored, but not deleted
    # (resetting the alias will "restore" the old links).
    'alias': None
}

# ---
# Misc
# ---
API_KEY = 'YouShouldChangeThisAsWell'


try:
    from local_config import *
except ImportError:
    pass
