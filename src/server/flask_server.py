import threading

from flask import Blueprint, Flask, current_app
import json

server_endpoints = Blueprint("server_endpoints", __name__)


def get_bed():
    bed = current_app.config["bed"]
    if bed is None:
        return None
    return bed


@server_endpoints.route('/patient/pressure', methods=["GET"])
def get_patient_pressure():
    bed = get_bed()
    patient = bed.get_patient()
    return patient.get_body_stats_df_json()


@server_endpoints.route('/patient/info', methods=["GET"])
def get_patient_info():
    bed = get_bed()
    patient = bed.get_patient()
    return patient.get_patient_info_json()

# There needs to be checks in place here. Is there already a thread???
@server_endpoints.route('/massage/start', methods=["GET"])
def start_message():
    massage = get_bed().get_massage()
    massage.set_message(True)
    massage.start()
    return json.dumps({"status": "massage started"})


@server_endpoints.route('/massage/stop', methods=["GET"])
def stop_message():
    massage = get_bed().get_massage()
    massage.set_message(False)
    return json.dumps({"status": "massage stopped"})



def create_server(bed):
    app = Flask(__name__)

    app.register_blueprint(server_endpoints)

    app.config["bed"] = bed
    return app
