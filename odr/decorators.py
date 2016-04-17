from __future__ import unicode_literals
from os import environ
from click import echo
from functools import update_wrapper
from odr.utils import os as os_utils


def verify_docker_machine(f):
    def new_func(*args, **kwargs):
        docker_machine_status = os_utils.output_from_cmd(['docker-machine', 'status'], join_result='')
        if docker_machine_status == 'Stopped':
            echo("Docker machine is not running. Starting it now...")
            os_utils.run_cmd(["docker-machine", 'start'])

        docker_envars = os_utils.output_from_cmd(["docker-machine", "env"])

        for var in docker_envars:
            if var.startswith("export"):
                key, value = var.replace('export ', '').split('=')

                environ[key] = value.replace('"', '')

        return f(*args, **kwargs)
    return update_wrapper(new_func, f)
