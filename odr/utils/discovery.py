from glob import glob


def locate_compose_files(base_path=''):
    """
    Finds `docker-compose.yml` files in this, and immediate subdirectories of the CWD
    :return: list of relative paths of `docker-compose.yml` files
    """
    if base_path and not base_path.endswith('/'):
        base_path += '/'

    return glob(base_path + '*/docker-compose.yml')


def build_compose_dependency_args(path):
    args = []
    compose_files = locate_compose_files(path)
    if not compose_files:
        raise Exception('Cannot locate any compose files')

    for cf in compose_files:
        args.append('-f')
        args.append(cf)

    return args
