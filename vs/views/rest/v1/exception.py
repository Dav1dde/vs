class MaxExpireException(Exception):
    def __init__(self, val, max_val, msg=None):
        if msg is None:
            msg = 'Expire set to {0}, maximum value is {1}'.format(
                val, max_val
            )

        Exception.__init__(self, msg)

    @classmethod
    def raise_if_required(cls, val, max_val):
        if max_val is not None and max_val > 0 and val > max_val:
            raise cls(val, max_val)
