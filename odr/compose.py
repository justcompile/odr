from __future__ import unicode_literals
from odr.utils.discovery import build_compose_dependency_args


class DockerCompose(object):
    def __init__(self, config):
        self.config = config

    def daemonised_containers(self, execution_command):
        c = ["docker-compose"]

        files_to_daemonise = self.config.get_daemonise_files()
        if not files_to_daemonise:
            return []

        for required_file in files_to_daemonise:
            c.extend(['-f', required_file])

        c.extend([execution_command, '-d'])
        return c

    def cmd(self, *args):
        c = ["docker-compose"]

        for required_file in self.config.get_required_files():
            c.extend(['-f', required_file])

        auto_discovery = self.config.auto_discovery()
        if auto_discovery:
            c.extend(build_compose_dependency_args(auto_discovery))

        if args:
            c.extend(args)

        return c

    def custom(self, command_name):
        custom_command_data = self.config.get_command(command_name)

        args = []

        for f in custom_command_data.get('files', []):
            args.extend(['-f', f])

        args.extend(custom_command_data['args'])

        return self.cmd(*args)
