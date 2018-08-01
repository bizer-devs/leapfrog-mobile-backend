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


# deprecated for now
def jsonify_safe(object):
    """
    attempts to jsonify an object, discarding anything that cannot be jsonified

    Args:
        object: Object to be jsonified

    """
    d = [row.__dict__ for row in object]

    for row in d:
        delkeys = []
        for key in row:
            try:
                jsonify(row[key])
            except TypeError:
                delkeys.append(key)

        for key in delkeys:
            del row[key]
    return jsonify(d)