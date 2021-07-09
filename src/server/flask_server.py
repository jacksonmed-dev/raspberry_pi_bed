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


def create_server(bed):
    app = Flask(__name__)

    app.register_blueprint(server_endpoints)

    app.config["bed"] = bed
    return app
