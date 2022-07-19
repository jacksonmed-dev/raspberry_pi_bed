import os
import sys
import threading
from bed.bed import Bed
from body.body import Patient
# from bed.sensor.directory_monitor import OnMyWatch
from massage.massage import Massage
from server.flask_server import create_server

# from bluetoothconnection import bluetooth_connection

from os.path import isfile, join, realpath, dirname
import configparser

dir_path = dirname(realpath(__file__))
file = join(dir_path, '../config.ini')
config = configparser.ConfigParser()
config.read(file)
config_paths = config['PATHS']

if os.uname()[4][:3] == 'arm' and "Linux" in os.uname().nodename:
    path = config_paths['MAIN_ARM']
    from bluetoothconnection.bluetooth_connection import Bluetooth as Bluetooth

else:
    path = config_paths['MAIN_MAC']
    from bluetoothconnection.bluetooth_connection_dummy import Bluetooth as Bluetooth

if __name__ == "__main__":

    # watch = OnMyWatch(bed=bed, path=path)
    bluetooth = Bluetooth()
    p = Patient(bluetooth=bluetooth)
    bed = Bed(patient=p, bluetooth=bluetooth)
    app = create_server(bed=bed, bluetooth=bluetooth)

    # Register Bluetooth callback
    bed.get_pressure_sensor().register_bluetooth_callback(bluetooth.enqueue_bluetooth_data)
    bluetooth.register_gpio_callback(bed.get_gpio().set_relay)
    bluetooth.register_bed_status_callback(bed.send_bed_status_bluetooth)
    bluetooth.register_bed_status_automatic(bed.set_bed_stats_automatic)
    # Adding Bluetooth Feature

    # if len(sys.argv) == 1:
    #     threading.Thread(bed.get_pressure_sensor().start_sse_client())
    #     # watch.run()
    #     x = 5
    # elif sys.argv[1] == 'message':
    #     message = Massage()
    #     message.start()
    #     threading.Thread(message.start())
    # else:
    #     print("Invalid argument passed")
    bluetooth.run(send_dummy_data=False)
    threading.Thread(target=bed.get_pressure_sensor().start_sse_client).start()
    # threading.Thread(app.run(host='0.0.0.0', debug=False, use_reloader=False))
