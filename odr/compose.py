from odr.utils.discovery import build_compose_dependency_args


class DockerCompose(object):
    def __init__(self, path):
        self.path = path

    def cmd(self, *args):
        c = ["docker-compose", '-f', 'compose-data.yml']
        c.extend(build_compose_dependency_args(self.path))

        if args:
            c.extend(args)

        return c