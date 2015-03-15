import vs.database
import string

SECRET_KEY = 'SECRET_KEY'
API_KEY = 'API_KEY'

DATABASE = vs.database.Redis(
    host='localhost', port=4999, db=0
)

DEFAULTS = {
    'default_expiry': -1,
    'max_expiry': -1,
    'custom_ids': True,
    'alias': None,
    'alphabet': string.ascii_letters + string.digits + '-_'
}
