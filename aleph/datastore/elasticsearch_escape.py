import re

"""
ElasticSearch >= 2.0.0 has declared some characters as illegal in field names. As such, we must escape field
names before storing a document or before searching (trickier) and unescape them before sending the results
back to the requesting method.

More details: https://github.com/elastic/elasticsearch/issues/6736

"""
ILLEGAL_CHARS = ('\\', '/', '*', '?', '"', '<', '>', '|', ' ', '.')

IC = re.compile(r'[%s]' % ''.join(ILLEGAL_CHARS))
ICE = re.compile(r'[\\][%s]' % ''.join(ILLEGAL_CHARS))

def escape(s):
    """
    :param s: string to escape
    :return: string with `aleph.utils.elasticsearch.ILLEGAL_CHARS` backslash escaped (e.g., '.' -> '\.')

    >>> escape('fi<>le"*name.|exe') == 'fi\<\>le\"\*name\.\|exe'
    True
    >>> escape('fi\<\>le\"\*name\.\|exe') == 'fi\<\>le\"\*name\.\|exe'
    True
    """
    L = len(s)
    escaped = ''
    for i in xrange(L):
        if IC.match(s[i]):
            if i == 0 or s[i] != '\\':
                escaped += '\\{}'.format(s[i])
        else:
            escaped += s[i]
    return escaped

def unescape(s):
    """
    :param s: string to escape
    :return: string with escaped `aleph.utils.elasticsearch.ILLEGAL_CHARS` unescaped (e.g., '\.' -> '.')

    >>> unescape('fi\<\>le\"\*name\.\|exe') == 'fi<>le"*name.|exe'
    True
    >>> unescape('fi<>le"*name.|exe') == 'fi<>le"*name.|exe'
    True
    """
    return s.replace('\\', '')

def escape_doc(doc):
    """
    Recursively descent a dictionary an escape the keys if necessary.
    :param doc: a dictionary
    :return: a dictionary with field names escaped as per `aleph.utils.elasticsearch.escape`
    escape_doc({'doc': {'fi<>le"*name.|exe': ['fi<>le"*name.|exe'], ''}})
    """
    return escaped_doc