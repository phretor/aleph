"""
ElasticSearch >= 2.0.0 has declared some characters as illegal in field names. As such, we must escape field
names before storing a document or before searching (trickier) and unescape them before sending the results
back to the requesting method.

We squash all the special characters to `_` (underscore).

More details: https://github.com/elastic/elasticsearch/issues/6736
"""

import re

ILLEGAL_CHARS = (
    chr(0x5c),  # \ backslash
    chr(0x2f),  # / slash
    chr(0x2a),  # * star
    chr(0x3f),  # ? question mark
    chr(0x22),  # " double quote
    chr(0x3c),  # < less than
    chr(0x3e),  # > greater than
    chr(0x7c),  # | pipe
    chr(0x20),  # space
    chr(0x2e)   # . dot
)
IC = re.compile('[{}]'.format(''.join(ILLEGAL_CHARS)))
SQUASH = '_'


def escape(s):
    res = ''
    for c in s:
        if IC.match(c):
            res += SQUASH
        else:
            res += c
    return res


def escape_doc(doc):
    """
    Recursively descent a dictionary an escape the keys.

    :param doc: a dictionary
    :return: a dictionary with field names escaped as per `aleph.utils.elasticsearch.escape`
    """
    ret = {}
    for k, v in doc.iteritems():
        if IC.match(k):
            K = escape(k)
        else:
            K = k
        if isinstance(v, dict):
            v = escape_doc(v)

        ret[K] = v
    return ret
