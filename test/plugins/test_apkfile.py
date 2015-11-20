import unittest
from mock import Mock
from aleph.plugins.apkfile_plugin import _ as setup
from aleph.plugins.apkfile_plugin import APKFilePlugin

class APKFilePEInfoPluginTestCase(unittest.TestCase):

    def test_it_is_initializable(self):
        queue = Mock()
        apk = APKFilePlugin(queue)
        self.assertIsNotNone(apk)
        self.assertIsInstance(apk, APKFilePlugin)

    def test_it_get_apk_data(self):
        queue = Mock()
        sample = Mock()
        apk = setup(queue)
        sample.path = 'test/data/cld.navi.mainframe.apk'
        apk.set_sample(sample)
        data = apk.process()
        import pprint; pprint.pprint(data)

    def test_it_setup(self):
        queue = Mock()
        apk = setup(queue)
        self.assertIsNotNone(apk)
        self.assertIsInstance(apk, APKFilePlugin)

if __name__ == '__main__':
    unittest.main()