import click
import json
from datetime import datetime
import os

@click.command()
@click.argument("description")
@click.pass_context
def add(ctx: click.Context, description:str):
    task_file_dir = str(ctx.obj["task_file_dir"])
    check_if_task_file_exists(task_file_dir)

    with open(task_file_dir, 'r') as outfile:
        data = json.loads(outfile.read())
        
    if len(data) == 0:
        id = 1
    else:
        id = int(data[len(data)-1]["id"]) + 1

    new_task = {
        "id":id,
        "description":description,
        "status":"to-do",
        "createdAt":get_current_time(),
        "updatedAt":get_current_time()
    }

    data.append(new_task)

    with open(task_file_dir, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    print("Task with ID [" + str(id) + "] with description \"" + description + "\" has been added")

@click.command()
@click.argument("id")
@click.argument("new_description")
@click.pass_context
def update(ctx: click.Context, id:str, new_description:str):
    task_file_dir = str(ctx.obj["task_file_dir"])
    check_if_task_file_exists(task_file_dir)

    with open(task_file_dir, 'r') as outfile:
        data = json.loads(outfile.read())

    found = False
    for i in data:
        if str(i["id"]) == str(id):
            i["description"] = new_description
            i["updatedAt"] = get_current_time()
            with open(task_file_dir, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print("Task with ID [" + id + "] description updated to " + new_description)
            found = True

    if not found:
        print("The task with ID [" + id + "] does not exist")

@click.command()
@click.argument("id")
@click.pass_context
def delete(ctx: click.Context, id:str):
    task_file_dir = str(ctx.obj["task_file_dir"])
    check_if_task_file_exists(task_file_dir)

    with open(task_file_dir, 'r') as outfile:
        data = json.loads(outfile.read())

    found = False
    for i in data:
        if str(i["id"]) == str(id):
            data.remove(i)
            with open(task_file_dir, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print("Task with ID [" + id + "] has been removed")
            found = True

    if not found:
        print("The task with ID [" + id + "] does not exist")


@click.command()
@click.argument("id")
@click.pass_context
def delete(ctx: click.Context, id:str):
    task_file_dir = str(ctx.obj["task_file_dir"])
    check_if_task_file_exists(task_file_dir)

    with open(task_file_dir, 'r') as outfile:
        data = json.loads(outfile.read())



def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def check_if_task_file_exists(task_file_dir:str):
    if not os.path.exists(task_file_dir):
        with open(task_file_dir, 'a') as outfile:
            json.dump([], outfile)