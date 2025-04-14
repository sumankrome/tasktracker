import click
import json
from datetime import datetime
import os
from tabulate import tabulate

## Command to add new tasks
@click.command()
@click.argument("description")
@click.pass_context
def add(ctx: click.Context, description:str):
    "Add a new task"
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

## Command to update task's description or status
@click.command()
@click.argument("id")
@click.option("-d", "--description", help="Update the description\n")
@click.option("-ip", "--in-progress", is_flag=True, help="Update status to \"In Progress\"")
@click.option("-do", "--done", is_flag=True, help="Update status to \"Done\"")
@click.option("-td", "--to-do", is_flag=True, help="Update status to \"To-Do\"")
@click.pass_context
def update(ctx: click.Context, id:str, description:str, in_progress:bool, done:bool, to_do:bool):
    "Update task's description or status"
    if description == None and not in_progress and not done and not to_do:
        print("--description, --to_do, --in-progress or --done is required\n")
        return

    task_file_dir = str(ctx.obj["task_file_dir"])
    check_if_task_file_exists(task_file_dir)

    with open(task_file_dir, 'r') as outfile:
        data = json.loads(outfile.read())

    found = False
    for i in data:
        if str(i["id"]) == str(id):
            if description != None:
                i["description"] = description
                print("Task with ID [" + id + "] description updated to " + description + "\n")
            if in_progress:
                i["status"] = "in-progress"
                print("Task with ID [" + id + "] updated to \"In-Progress\"\n")
            if done:
                i["status"] = "done"
                print("Task with ID [" + id + "] updated to \"Done\"\n")
            if to_do:
                i["status"] = "done"
                print("Task with ID [" + id + "] updated to \"To-Do\"\n")
            i["updatedAt"] = get_current_time()
            with open(task_file_dir, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            found = True

    if not found:
        print("The task with ID [" + id + "] does not exist\n")

## Command to delete tasks
@click.command()
@click.argument("id")
@click.pass_context
def delete(ctx: click.Context, id:str):
    "Delete task by ID"
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
            print("Task with ID [" + id + "] has been removed\n")
            found = True

    if not found:
        print("The task with ID [" + id + "] does not exist\n")

## Command to list tasks. Can specify --done or --in-progress to only show tasks with specific tasks.
@click.command()
@click.pass_context
@click.option("-ip", "--in-progress", is_flag=True, help="Lists all tasks with status \"In Progress\"")
@click.option("-do", "--done", is_flag=True, help="Lists all tasks with status \"Done\"")
@click.option("-td", "--to-do", is_flag=True, help="Lists all tasks with status \"To-Do\"")
def list(ctx: click.Context, in_progress: bool, done: bool, to_do: bool):
    "List tasks"
    task_file_dir = str(ctx.obj["task_file_dir"])
    check_if_task_file_exists(task_file_dir)

    with open(task_file_dir, 'r') as outfile:
        data = json.loads(outfile.read())
    
    if len(data) == 0:
        print("There are no tasks in the tracker\n")
        return

    if not in_progress and not done and not to_do:
        print(tabulate(data, headers="keys", tablefmt="simple_outline"))
        print("\n")

    if in_progress:
        in_progress_list = []
        for i in data:
            if i["status"] == "in-progress":
                in_progress_list.append(i)
        if len(in_progress_list) == 0:
            print("There are no tasks in the tracker with status \"In-Progress\"\n")
        print(tabulate(in_progress_list, headers="keys", tablefmt="simple_outline"))
        print("\n")

    if done:
        done_list = []
        for i in data:
            if i["status"] == "done":
                done_list.append(i)
        if len(done_list) == 0:
            print("There are no tasks in the tracker with status \"Done\"\n")
        print(tabulate(done_list, headers="keys", tablefmt="simple_outline"))
        print("\n")
    
    if to_do:
        to_do_list = []
        for i in data:
            if i["status"] == "to-do":
                to_do_list.append(i)
        if len(to_do_list) == 0:
            print("There are no tasks in the tracker with status \"To-Do\"\n")
        print(tabulate(to_do_list, headers="keys", tablefmt="simple_outline"))
        print("\n")


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def check_if_task_file_exists(task_file_dir:str):
    if not os.path.exists(task_file_dir):
        with open(task_file_dir, 'a') as outfile:
            json.dump([], outfile)