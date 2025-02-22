import os

import jsonl
import pydantic
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project, Task


api = TodoistAPI(os.environ["TODOIST_API_KEY"])


class OutputableTaskFields(pydantic.BaseModel):
    content: str
    created_at: str
    description: str
    due_date: str
    labels: list[str]
    priority: int
    project_name: str
    url: str


def get_all_projects() -> dict[str, Project]:
    return {project.id: project for project in api.get_projects()}


def get_all_today_tasks() -> dict[str, Task]:
    tasks: list[Task] = api.get_tasks(filter="today")
    return {task.id: task for task in tasks}


def format_tasks_to_jsonl(tasks: dict[str, Task], projects: dict[str, Project]) -> str:
    output = []
    for task in tasks.values():
        outputable_task_fields = OutputableTaskFields(
            content=task.content,
            created_at=task.created_at,
            description=task.description,
            due_date=task.due.date,
            labels=task.labels,
            priority=task.priority,
            project_name=projects[task.project_id].name,
            url=task.url,
        )
        output.append(dict(outputable_task_fields))
    return jsonl.dumps(output)


def format_tasks_to_simple_bulleted_list(tasks, projects) -> str:
    output = ""
    for task in tasks.values():
        output += f"- {task.content}\n"
    return output


if __name__ == "__main__":
    projects = get_all_projects()
    tasks = get_all_today_tasks()
    # jsonl_output = format_tasks_to_jsonl(tasks, projects)
    # print(jsonl_output)
    print(format_tasks_to_simple_bulleted_list(tasks, projects))
