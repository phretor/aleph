# -*- coding: utf8 -*-

from aleph.base import PluginBase, plugin_registry
from aleph.settings import SAMPLE_TEMP_DIR
from aleph.constants import MIMETYPES_ARCHIVE
import tempfile, hashlib

class UrlExtractorPlugin(PluginBase):
    """Extract URL from the sample"""
    name = 'urlextractor'
    default_options = { 'enabled': True }
    mimetypes_except = MIMETYPES_ARCHIVE + ['text/url']
    depends = [ 'strings' ]

    def process(self):
        """Try to extract URL from the sample"""

        if not 'strings' in self.sample.data:
            return {} 

        strs = self.sample.data['strings']

        if 'url' in strs and len(strs['url']) > 0:
            for url in strs['url']:
                url_text = "[InternetShortcut]\nURL=%s" % url
                
                filename = "%s.url" % hashlib.sha256(url).hexdigest()

                temp_file = tempfile.NamedTemporaryFile(dir=SAMPLE_TEMP_DIR, suffix='_%s' % filename, delete=False)
                temp_file.write(url_text)
                temp_file.close()

                self.create_sample(temp_file.name, filename, mimetype="text/url")

@plugin_registry.connect
def _(queue, *args, **kwargs):
    return UrlExtractorPlugin(queue, *args, **kwargs)