import json
import sys


def console(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs)


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def string2json(string):
    parsed = json.loads(string)
    print(json.dumps(parsed, indent=4, sort_keys=True))


def object2json(object):
    print(json.dumps(object, indent=4, sort_keys=True))

