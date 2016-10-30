import subprocess

import sys

import click
from odr.compose import DockerCompose
from odr.config import Config
from odr.decorators import verify_docker_machine
from odr.utils.os import run_cmd


@click.group()
@click.option('-f', 'path', default='odr.cfg', type=click.Path())
@click.pass_context
#@verify_docker_machine
def cli(ctx, path):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['FILE_PATH'] = path
    cfg = Config(path)
    cfg.load()

    ctx.obj['config'] = cfg


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def up(ctx, args):
    """Brings up one or more services"""
    cmd = DockerCompose(config=ctx.obj['config']).cmd('up', *args)

    click.echo('Executing: {}'.format(cmd))
    subprocess.call(cmd)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def down(ctx, args):
    """Brings down one or more services"""
    cmd = DockerCompose(config=ctx.obj['config']).cmd('down', *args)

    click.echo('Executing: {}'.format(cmd))
    subprocess.call(cmd)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def logs(ctx, args):
    """Displays log out put for all or one service"""
    cmd = DockerCompose(config=ctx.obj['config']).cmd('logs', *args)

    click.echo('Executing: {}'.format(cmd))
    subprocess.call(cmd)


@cli.command()
@click.argument('cmd', required=False)
@click.option('-l', 'list_commands', is_flag=True)
@click.pass_context
def run(ctx, cmd, list_commands):
    """Runs task specified in the configuration file"""

    if not cmd or list_commands:
        click.echo("Tasks:\n")
        for custom_cmd in ctx.obj['config'].get_commands():
            click.echo(custom_cmd)
    else:
        command = DockerCompose(config=ctx.obj['config']).custom(cmd)
        subprocess.call(command)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def ps(ctx, args):
    cmd = DockerCompose(config=ctx.obj['config']).cmd('ps', *args)
    run_cmd(cmd)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def build(ctx, args):
    cmd = DockerCompose(config=ctx.obj['config']).cmd('build', *args)
    run_cmd(cmd)

if __name__ == "__main__":
    cli(obj={})
