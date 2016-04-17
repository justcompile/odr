from __future__ import unicode_literals
from odr.utils.discovery import build_compose_dependency_args


class DockerCompose(object):
    def __init__(self, config):
        self.config = config

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
