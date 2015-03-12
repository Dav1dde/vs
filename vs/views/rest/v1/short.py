from flask import g, current_app, abort, url_for
from flask.ext.restful import reqparse
from flask.ext import restful


class ShortUrl(restful.Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument(
            'id', type=str, required=True,
            help='URL-Id to resolve for the full url'
        )

        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument(
            'url', type=str, required=True,
            help='URL to shorten.'
        )
        expire = current_app.config['DEFAULT_EXPIRE']
        self.put_parser.add_argument(
            'expire', type=int, default=expire,
            help=(
                'Days after which the url will expire, '
                'defaults to {0} days'.format(expire)
            )
        )
        if current_app.config['CUSTOM_IDS']:
            self.put_parser.add_argument(
                'id', type=str,
                help='Request custom id for the url'
            )

        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument(
            'id', type=str, required=True,
            help='URL-Id to delete'
        )
        self.delete_parser.add_argument(
            'secret', type=str, required=True,
            help='Secret to delete this url'
        )

    def get(self):
        """
        Returns the long url for a given short url.
        """
        args = self.get_parser.parse_args(strict=True)
        url = g.database.get(args['id'])
        return {'url': url}

    def put(self):
        """
        Creates a new short url.
        """
        # strict is important, if config disabled custom urls
        args = self.put_parser.parse_args(strict=True)

        MaxExpireException.raise_if_required(
            args['expire'], current_app.config['MAX_EXPIRE']
        )

        id, secret = g.database.create(
            args['url'], id=args.get('id'), expire=args.get('expire')
        )
        return {
            'id': id, 'secret': secret,
            'url': url_for('url.resolve', id=id, _external=True),
            'rel_url': url_for('url.resolve', id=id)
        }

    def delete(self):
        """
        Deletes a short url.
        """
        if current_app.config['DISABLE_DELETE']:
            return abort(405)

        args = self.delete_parser.parse_args(strict=True)
        success = g.database.delete(args['id'], args['secret'])

        return {'success': success}
