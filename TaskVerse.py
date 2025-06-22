from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from uuid import uuid4
import webbrowser
import signal
import threading
import os
import time
import sys

# PyInstaller resource path resolver
def resource_path(relative_path):
    """Get absolute path to resource (works for dev and PyInstaller)"""
    try:
        base_path = sys._MEIPASS  # PyInstaller's temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Ensure 'lib' is found when bundled
sys.path.append(resource_path("lib"))

from lib import utils as util
from lib.utils import bcolors

# Flask app with bundled templates/static paths
template_dir = resource_path('templates')
static_dir = resource_path('static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Graceful shutdown function
def kill():
    time.sleep(2)
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

# Routes
@app.route("/")
def index():
    return redirect(url_for("home", endpt="tasks"))

@app.route("/home")
def home():
    endpt = request.args.get("endpt", "tasks")
    if endpt == "tasks":
        return render_template("homextasks.html")
    elif endpt == "stop":
        try:
            t1 = threading.Thread(target=kill)
            t1.start()
            return jsonify({"status": True})
        except:
            return jsonify({"status": False})
    else:
        return render_template("404.html")

@app.route("/api/tasks")
def api_tasks():
    task_data = util.formatter(util.load_data())
    return jsonify(task_data)

@app.route('/submitData', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        task_name = data.get('name')
        deadline_str = data.get('deadline')

        if not task_name or not deadline_str:
            return jsonify(success=False, error="Missing data")

        deadline_dt = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        deadline_int = int(deadline_dt.strftime('%Y%m%d%H%M'))
        task_data = [str(uuid4()), task_name, deadline_int]

        util.add_task(task_data)
        return jsonify(success=True)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

@app.route('/remove', methods=['DELETE'])
def remove_task():
    try:
        task_id = request.args.get('id')
        if not task_id:
            return jsonify(success=False)

        util.del_task(task_id)
        return jsonify(success=True)

    except Exception as e:
        print(f"Deletion error: {e}")
        return jsonify(success=False)

# Entry point
if __name__ == "__main__":
    parameters = sys.argv
    if len(parameters) <= 1:
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} No parameters provided! Try using 'help'.")
    elif parameters[1] == "init":
        util.init()
        print(f"{bcolors.OKBLUE}[INFO]{bcolors.ENDC}{bcolors.OKGREEN} Initialization complete!{bcolors.ENDC}")
    elif parameters[1] == "run":
        webbrowser.open("http://localhost:6767")
        app.run(host="localhost", port=6767, debug=False)
    elif parameters[1] == "help":
        print(f"{bcolors.OKBLUE}_____HELP_____{bcolors.ENDC}")
        print(f" {bcolors.OKBLUE}init ->{bcolors.ENDC}{bcolors.OKGREEN} To initialize the application{bcolors.ENDC}")
        print(f" {bcolors.OKBLUE}run  ->{bcolors.ENDC}{bcolors.OKGREEN} To run the Application{bcolors.ENDC}")
        print(f" {bcolors.OKBLUE}help ->{bcolors.ENDC}{bcolors.OKGREEN} To see help menu{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC}{bcolors.WARNING} Invalid Parameters!{bcolors.ENDC}")
