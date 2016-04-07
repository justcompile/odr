import click
from odr.compose import DockerCompose


@click.group()
@click.option('-f', 'path', default='.odr.cfg')
@click.pass_context
def cli(ctx, path):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['FILE_PATH'] = path


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def up(ctx, args):
    """Brings up one or more services"""
    cmd = DockerCompose(path=ctx.obj['FILE_PATH']).cmd('up', *args)

    click.echo('Executing: {}'.format(cmd))


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def down(ctx, args):
    """Brings down one or more services"""
    cmd = DockerCompose(path=ctx.obj['FILE_PATH']).cmd('down', *args)

    click.echo('Executing: {}'.format(cmd))


@cli.command()
@click.argument('task', required=False)
@click.option('-l', 'list_tasks', is_flag=True)
@click.pass_context
def run(ctx, task, list_tasks):
    """Runs task specified in the configuration file"""

    if not task or list_tasks:
        click.echo("Displaying tasks...")
    else:
        click.echo("Should run something")
    #cmd = DockerCompose(path=ctx.obj['FILE_PATH']).cmd('down', *args)

    #click.echo('Executing: {}'.format(cmd))

if __name__ == "__main__":
    cli(obj={})
