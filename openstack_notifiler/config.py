"""
Use ConfigParser define all config, other module use config module get data.
"""

import ConfigParser


FILE_PATH = '/etc/openstack-notifier/openstack-notifier.conf'


class Config(object):
    """ Load config file"""
    def __init__(self):
        self.confp = ConfigParser.ConfigParser()
        self.read_file = self.read_config()

    def read_config(self, file_name=FILE_PATH):
        """define config file read"""
        self.confp.read(file_name)

    def get(self, section, option):
        """define config file data get"""
        return self.confp.get(section, option)


CONF = Config()
