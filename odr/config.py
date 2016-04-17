from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Config(object):
    __config = None

    def __init__(self, path):
        self.file_path = path

    def load(self):
        self.__config = load(open(self.file_path), Loader=Loader)

        return self.__config

    def get(self):
        return self.__config

    def get_required_files(self):
        return self.__config['files'].get('required', []) or []

    def auto_discovery(self):
        ad = self.__config['files'].get('autodiscover')
        if ad:
            return ad['base_path']

        return False

    def get_commands(self):
        return self.__config['commands']
