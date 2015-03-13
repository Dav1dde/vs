from flask import g, current_app, abort, url_for
from flask.ext.restful import reqparse
from flask.ext import restful


class Domain(restful.Resource):
    CONFIG_KEYS = ('default_expiry', 'max_expiry', 'custom_ids', 'alias')

    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            'api_key', type=str, required=True,
            help='API-Key'
        )

        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument(
            'api_key', type=str, required=True,
            help='API-Key'
        )
        self.put_parser.add_argument(
            'default_expiry', type=int,
            help='Set default expiry.'
        )
        self.put_parser.add_argument(
            'max_expiry', type=int,
            help='Set max expiry'
        )
        self.put_parser.add_argument(
            'custom_ids', type=bool,
            help='Allow or disallow custom Ids'
        )
        self.put_parser.add_argument(
            'alias', type=str,
            help='Set a domain alias for this domain'
        )

        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument(
            'api_key', type=str, required=True,
            help='API-Key'
        )

    def get(self):
        """
        Returns the long url for a given short url.
        """
        args = self.get_parser.parse_args(strict=True)
        if not args['api_key'] == current_app.config['API_KEY']:
            return abort(403)

        ret = dict()
        for key in self.CONFIG_KEYS:
            ret[key] = g.database.config_get(key)
        return ret

    def put(self):
        """
        Creates a new short url.
        """
        args = self.put_parser.parse_args(strict=True)
        if not args['api_key'] == current_app.config['API_KEY']:
            return abort(403)

        for key in self.CONFIG_KEYS:
            value = args.get(key)
            if value is not None:
                g.database.config_set(key, value)

    def delete(self):
        """
        Deletes a short url.
        """
        args = self.delete_parser.parse_args(strict=True)
        if not args['api_key'] == current_app.config['API_KEY']:
            return abort(403)

        success = g.database.config_delete()
