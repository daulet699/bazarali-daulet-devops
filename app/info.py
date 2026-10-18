"""Student information from a local JSON configuration and Docker env vars."""
import json
import os
from pathlib import Path

FIELDS = {
    "name": "STUDENT_NAME",
    "surname": "STUDENT_SURNAME",
    "group": "STUDENT_GROUP",
    "student_id": "STUDENT_ID",
}


def get_student_info(environ=None):
    """Return student data, using environment variables when provided."""
    if environ is None:
        environ = os.environ
    path = Path(__file__).with_name("student.json")
    with path.open("r", encoding="utf-8") as file:
        defaults = json.load(file)
    return {
        field: str(environ.get(env_name) or defaults[field])
        for field, env_name in FIELDS.items()
    }


def format_student_info(info):
    return ("================================\n"
            "DevOps Student Application\n"
            "================================\n"
            f"Name: {info['name']}\n"
            f"Surname: {info['surname']}\n"
            f"Group: {info['group']}\n"
            f"Student ID: {info['student_id']}\n"
            "Application is running successfully!\n")
