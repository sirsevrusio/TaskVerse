from flask import Flask, render_template, request, redirect, url_for, jsonify
from lib import utils as util
from datetime import datetime
from lib.utils import bcolors 
from uuid import uuid4
import webbrowser
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("home", endpt="tasks"))

@app.route("/home")
def home():
    endpt = request.args.get("endpt", "tasks")
    if endpt == "tasks":
        task_data = util.formatter(util.load_data())
        return render_template("homextasks.html", task_data=task_data)
    else:
        return render_template("404.html")

@app.route('/submitData', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        task_name = data.get('name')
        deadline_str = data.get('deadline')  # Format: YYYY-MM-DDTHH:MM

        # Validate required fields
        if not task_name or not deadline_str:
            return jsonify(success=False, error="Missing data")

        # Parse datetime
        deadline_dt = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')

        # Convert to "YYYYMMDDHHMM" integer (e.g. 202506201230)
        # Clean way: use strftime instead of re.split
        deadline_int = int(deadline_dt.strftime('%Y%m%d%H%M'))

        # Create task data
        task_data = [str(uuid4()), task_name, deadline_int]

        # Save the task
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

        result = True  # Simulate success for now

        return jsonify(success=result)
    except Exception as e:
        print(f"Deletion error: {e}")
        return jsonify(success=False)

if __name__ == "__main__":
    parameters = sys.argv
    if len(parameters) <= 1:
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} No parameters provided! try using 'help'.")
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