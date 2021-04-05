from django_redis import get_redis_connection


def parse_redis(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, set):
        return set(x.decode('utf-8') for x in obj)
    elif isinstance(obj, list):
        return [x.decode('utf-8') for x in obj]
    else:
        return obj


def tocontainer(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return parse_redis(result)

    return wrapper


class Redis(object):
    def __init__(self, conf='default'):
        self.conn = get_redis_connection(conf)

    def __getattr__(self, func):
        return tocontainer(getattr(self.conn, func))

