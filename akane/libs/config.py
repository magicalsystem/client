import os.path
from ConfigParser import ConfigParser

class ConfigProvider(object):
    def __getitem__(self, key):
        pass

class FileConfigProvider(ConfigProvider):
    
    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read(['akane.conf', os.path.expanduser('~/.akane.conf')])

    def __getitem__(self, key):
       return self.cfg._sections[key] 


def read_config():
    return FileConfigProvider()
