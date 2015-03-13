import vs.database

SECRET_KEY = 'ChangeMeOrGetHacked'

DATABASE = vs.database.Redis(
    host='localhost', port=4999, db=0
)

