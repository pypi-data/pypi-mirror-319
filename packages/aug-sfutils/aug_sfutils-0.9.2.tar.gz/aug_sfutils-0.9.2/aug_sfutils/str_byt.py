import sys

def to_byt(str_or_byt):
    """
    Converts a plain string to a byte string (python2/3 compatibility)
    """

    str_out = str_or_byt.encode('utf8') if not isinstance(str_or_byt, bytes) else str_or_byt

    return str_out


def to_str(str_or_byt, strip=True):
    """
    Converts a byte string to a plain string (python2/3 compatibility)
    """

    if sys.version_info >= (3, 0, 0):
        if isinstance(str_or_byt, bytes):
#            str_out = str_or_byt.decode('utf8')
            str_out = str_or_byt.decode('iso-8859-1').replace('\x00', '')
        else:
            str_out = str_or_byt
    else:
        if isinstance(str_or_byt, unicode):
            str_out = str(str_or_byt)
        else:
            str_out = str_or_byt

    if strip:
        return str_out.strip()
    else:
        return str_out
