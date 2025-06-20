from datetime import datetime
import json
import os

months = {
    "01": "Jan",
    "02": "Feb",
    "03": "March",
    "04": "Apr",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "Aug",
    "09": "Sept",
    "10": "Oct",
    "11": "Nov", 
    "12": "Dec"
    }

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def load_data(filename="schedule.json"):
    filename = os.path.join("data", filename)
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise RuntimeError(f"utils.py::load_data::{e}")
    
def dump_data(filename="schedule.json", data=[], type="w"):
    filename = os.path.join("data", filename)
    try:
        with open(filename, type) as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise RuntimeError(f"utils.py::dump_data::{e}")

def add_task(task_data:list):
    wholeData = load_data()
    wholeData.append(task_data)
    dump_data(data=wholeData)

def del_task(task_id:str):
    wholeData = load_data()
    try:
        for row in wholeData:
            if row[0] == task_id:
                wholeData.remove(row)
                break
    except KeyError:
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC}{bcolors.WARNING} No task found with id {task_id}, Not Possible to delete such task!{bcolors.ENDC}")
    dump_data(data=wholeData)

def init():
    try:
        os.makedirs("data", exist_ok=True)
        dump_data()
    except Exception as e:
        raise RuntimeError(f"utils.py::init::{e}")

def formatter(data: tuple):
    data = list(data)

    # Sort by deadline (row[2] assumed to be int like 202506201445)
    data.sort(key=lambda x: x[2])

    for row in data:
        date_time = str(row[2])  # e.g., "202506251030"

        # Convert to datetime object
        dt_obj = datetime.strptime(date_time, "%Y%m%d%H%M")

        # Format time to "02:30 PM"
        time_str = dt_obj.strftime("%I:%M %p")  # %I gives 12-hour, %p gives AM/PM

        # Format final date string like "25 June 2025 02:30 PM"
        day = dt_obj.strftime("%d")
        month_str = months.get(dt_obj.strftime("%m"), dt_obj.strftime("%B"))
        year = dt_obj.strftime("%Y")
        formatted_time = f"{day} {month_str} {year} {time_str}"

        # Day of the week (e.g. Monday)
        day_name = dt_obj.strftime("%A")

        # Update row
        row[2] = formatted_time
        row[1] = row[1].title()
        row.append(day_name)

    return data