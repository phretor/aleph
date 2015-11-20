# -*- coding: utf8 -*-

from aleph.base import PluginBase, plugin_registry


class YaraPlugin(PluginBase):
    """Use Yara to match patterns into the sample"""
    name = 'yara'
    default_options = {'enabled': True}
    required_options = ['rules_path']

    rules = None

    def setup(self):
        try:
            self.rules = yara.compile(filepath=self.options['rules_path'])
        except Exception, e:
            self.logger.warning('YARA could not read the rules: %s ' % (str(self.options['rules_path'])))

    def process(self):
        try:
            matches = self.rules.match(self.sample.path)
        except Exception, e:
            self.logger.warning('Error matching: %s ' % (str(e)))
        return {
            'yara_rules': self.options['rules_path'],
            'matches': matches
        }


@plugin_registry.connect
def _(queue, *args, **kwargs):
    return YaraPlugin(queue)
