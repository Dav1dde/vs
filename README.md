VS
==

Simple URL-Shortner service


## API ##

| Endpoint | Method | Arguments                                                                                                  | Returns                                                                                     | Notes                                                                |
|----------|--------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| /api     | GET    | `{'id': 'Short URL Id'}`                                                                                   | `{'url': 'Returns URL the Id points to'}`                                                   |                                                                      |
| /api     | PUT    | `{'url': 'URL to shorten', 'expire': 'Days until the short URL expires', 'id': 'Custom Id for short URL'}` | `{'id': 'Id of the short URL', 'url': 'Short URL', 'rel_url': 'Relative URL from service'}` | `id` might not be available, depending on service-configuration. |
| /api     | DELETE | `{'id': 'Id to delete', 'secret': 'Secret required for deletion'}`                                         | `{'success': 'True'}`                                                                       | Deletion might not be possible, depending on service-configuration.  |


Successful API-Calls will return HTTP-Statuscode 200.
Unsuccessful calls return: `{'message': 'Short description why the call failed', 'status': 400}`
(status varies).


## Configuration ##

Copy `vs/config.py` to `local_config.py`, it will automatically be loaded (if it exists).

If your local configuration does not get loaded, make sure it is available for Python (`$PYTHONPATH`).


### Commandline ###

```
usage: vs [-h] [--port PORT] [--host HOST] [--debug]

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  Port to listen on.
  --host HOST  Host to bind to.
  --debug      TESTING ONLY
```


## Issues ##

* Secrets (deletion) don't change for the same Id/Url