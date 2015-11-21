import pickle
import unittest

from aleph.datastore.elasticsearch_escape import escape_doc


class ElasticsearchEscapeTestCase(unittest.TestCase):
    def testEscapeDoc(self):
        with open('test/data/malformed_doc.pickle', 'rb') as f:
            malformed_doc = pickle.load(f)

        encoded = escape_doc(malformed_doc)

        with open('test/data/escped_doc.pickle', 'rb') as f:
            sanitized_doc = pickle.load(f)

        assert encoded == sanitized_doc


if __name__ == '__main__':
    unittest.main()
