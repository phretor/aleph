import ntpath
import os
import shutil
import tarfile
from tempfile import mkdtemp

from aleph.base import PluginBase, plugin_registry
from aleph.settings import SAMPLE_TEMP_DIR


class TarGzipArchivePlugin(PluginBase):
    """Extract files from TAR GZIP"""
    name = 'archive_tar-gzip'
    default_options = {'enabled': True}
    mimetypes = ['application/x-tar', 'application/gzip', 'application/x-gzip']

    def extract_file(self, path, dest):
        """Extract TAR/GZIP file to a temp folder"""
        nl = []

        with tarfile.open(str(path), 'r') as tarf:
            tarf.extractall(str(dest))
            nl = tarf.getnames()

        return nl

    def process(self):

        temp_dir = mkdtemp(dir=SAMPLE_TEMP_DIR)

        targzip_contents = []

        self.logger.debug("Uncompressing gzip/tar file %s" % self.sample.path)
        targzip_contents = self.extract_file(self.sample.path, temp_dir)
        for fname in targzip_contents:
            fpath = os.path.join(temp_dir, fname)
            if os.path.isfile(fpath):
                head, tail = ntpath.split(fpath)
                self.create_sample(fpath, tail)
        shutil.rmtree(temp_dir)

        ret = {}

        if len(targzip_contents) == 0:
            self.logger.error('Unable to uncompress %s. Corrupted file?' % self.sample.path)
            return ret

        ret['contents'] = targzip_contents

        # Add general tags
        self.sample.add_tag('archive')
        self.sample.add_tag('tar-gzip')

        return ret


@plugin_registry.connect
def _(queue, *args, **kwargs):
    return TarGzipArchivePlugin(queue, *args, **kwargs)
