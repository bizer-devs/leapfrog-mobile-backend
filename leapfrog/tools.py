from json import JSONEncoder


class ModelEncoder(JSONEncoder):
    """
    A bare-bones JSONEncoder that emulates JSONEncoder, but attempts to call `serializeable` first.  All models should
    have this method defined, allowing them to
    """

    def default(self, obj):
        try:
            return obj.serializeable()
        except AttributeError:
            return JSONEncoder.default(self, obj)