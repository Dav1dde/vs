from flask import g, current_app, abort, url_for
from flask.ext.restful import reqparse
from flask.ext import restful


def req_boolean(val):
    val = val.strip().lower()
    if val not in ('true', 'false'):
        raise ValueError()
    return val in ('true',)


def min_length_str(length):
    def validator(s):
        if len(set(s)) < length:
            raise ValueError()
        return str(s)
    return validator


class Domain(restful.Resource):
    CONFIG_KEYS = (
        'default_expiry', 'max_expiry',
        'custom_ids', 'alias', 'alphabet'
    )

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
            'custom_ids', type=req_boolean,
            help='Allow or disallow custom Ids'
        )
        self.put_parser.add_argument(
            'alias', type=str,
            help='Set a domain alias for this domain'
        )
        self.put_parser.add_argument(
            'alphabet', type=min_length_str(3),
            help='Set the Id alphabet'
        )

        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument(
            'api_key', type=str, required=True,
            help='API-Key'
        )

    def get(self):
        """
        Returns the configuration for the current domain.
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
        Sets the configuration for the current domain.
        """
        args = self.put_parser.parse_args(strict=True)
        if not args['api_key'] == current_app.config['API_KEY']:
            return abort(403)

        for key in self.CONFIG_KEYS:
            value = args.get(key)
            if value is not None:
                g.database.config_set(key, value)
    post = put

    def delete(self):
        """
        Resets the configuration for this domain to defaults.
        """
        args = self.delete_parser.parse_args(strict=True)
        if not args['api_key'] == current_app.config['API_KEY']:
            return abort(403)

        success = g.database.config_delete()
