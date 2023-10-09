import requests
import json


def get_groups():
    r = requests.get('http://127.0.0.1:8000/api/groups')
    data = r.json()
    return data


def get_students(group_id):
    r = requests.get(f'http://127.0.0.1:8000/api/students/{group_id}/')
    data = r.json()
    return data


def start_attendance(group_id):
    r = requests.get(f'http://127.0.0.1:8000/api/attendance/{group_id}/')
    data = r.json()
    return data


def change_status(attendance_id):
    r = requests.get(f'http://127.0.0.1:8000/api/attendance/student/{attendance_id}/')
    data = r.json()
    return data


# print(get_students())
