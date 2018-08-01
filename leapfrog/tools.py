from json import JSONEncoder
from random import random
import math


class ModelEncoder(JSONEncoder):
    """
    A bare-bones JSONEncoder that emulates JSONEncoder, but attempts to call `serializeable` first.  All models should
    have this method defined, allowing them to
    """

    def default(self, obj):
        """
        WTF, why doesn't JSONEncoder already try str(obj) ??
        """
        try:
            return obj.serializeable()
        except AttributeError:
            pass

        try:
            return JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


def new_transfer_code(l):
    """
    Creates a code used to authenticate transfers, consisting of upper- and lowercase alphanumerics.  Technically this
    doesn't guarantee uniqueness between codes, but at l = 30 the chance of two codes colliding is 1 in 5.9 x 10^53.  If
    this fails, I'm moving to Vegas.

    Args:
        l: code length

    Returns:
        code: transfer code

    """
    code = ''
    for x in range(l):
        r = math.floor(random() * 62)  # 26 Uppercase + 26 Lowercase + 10 digits
        if r < 26:
            code += chr(r + 65)
        elif r < 52:
            code += chr(r + 71)
        else:
            code += chr(r - 4)
    return code