import click
import crud
import os
import configparser
from pathlib import Path

@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """A CLI task tracker"""
    config = configparser.ConfigParser()
    dir = Path(__file__).parent.resolve()
    config.read(str(dir) + "/config.ini")
    task_folder = dir

    if config.get('DEFAULT', 'task_folder') != "0":
        task_folder = (str(dir) + "/" + config.get('DEFAULT', 'task_folder'))
        if not os.path.exists(task_folder):
            os.mkdir(task_folder)
    task_filename = config.get('DEFAULT', 'task_filename')

    task_file_dir = str(task_folder) + "/" + str(task_filename)

    ctx.obj = {"task_file_dir": task_file_dir}

cli.add_command(crud.add)
cli.add_command(crud.update)
cli.add_command(crud.delete)
