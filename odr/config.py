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

    def get_daemonise_files(self):
        try:
            if self.__config['files']['daemonise_required']:
                return self.get_required_files()
        except KeyError:
            pass

        return []

    def get_command(self, command_name):
        cmd_configuration = self.__config.get('commands').get(command_name)
        if not cmd_configuration:
            raise Exception('{0} is not a recognised command'.format(command_name))

        conf = {}
        if cmd_configuration.get('file'):
            conf['files'] = [cmd_configuration.get('file')]

        conf['args'] = [cmd_configuration['docker-command'], cmd_configuration['container']]

        try:
            conf['args'].extend(cmd_configuration['command'].split())
        except KeyError:
            pass

        return conf

    def get_commands(self):
        return self.__config.get('commands', {}).iterkeys()
