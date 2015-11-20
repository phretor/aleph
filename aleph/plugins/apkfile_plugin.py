# -*- coding: utf8 -*-

from aleph.base import PluginBase
from aleph.base import plugin_registry

from androguard.core.bytecodes.apk import APK

class APKFilePlugin(PluginBase):
    """Plugin that analyze APK files and extracts static properties including:

        * manifest properties (e.g., permissions, activities)
        * class hierarchy

        Requires androguard
    """
    name = 'apkfile'
    default_options = {'enabled': True}

    def get_permissions(self):
        try:
            perms = self.apk.get_permissions()

            self.logger.info('Getting perms for file %s', self.sample.path)
            return perms
        except Exception as ex:
            self.logger.warning('Could not get permissions from %s because of %s', self.sample.path, ex)

    def parse_apk(self):
        self.apk = None
        try:
            self.apk = APK(self.sample.path)
        except Exception as ex:
            self.logger.warning('Could not parse %s because of %s', self.sample.path, ex)

    def process(self):
        data = {}
        self.parse_apk()

        if self.apk:
            data.update({'permissions': self.get_permissions()})

        return data

@plugin_registry.connect
def _(queue, *args, **kwargs):
    return APKFilePlugin(queue, *args, **kwargs)