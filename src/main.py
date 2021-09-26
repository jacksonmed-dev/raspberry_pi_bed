import os
import sys
import threading
from bed.bed import Bed
from body.body import Patient
from bed.sensor.directory_monitor import OnMyWatch
from massage.massage import Massage
from server.flask_server import create_server
from bluetoothconnection import bluetooth_connection

if os.uname()[4][:3] == 'arm':
    path = "/home/pi/Desktop/sensor_data"
else:
    path = "/home/cjstanfi/Desktop/sensor_data"


if __name__ == "__main__":
    p = Patient()
    bed = Bed(patient=p)
    watch = OnMyWatch(bed=bed, path=path)
    bluetooth = bluetooth_connection.Bluetooth()
    app = create_server(bed=bed, bluetooth=bluetooth)
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
    # threading.Thread(target=bed.get_pressure_sensor().start_sse_client).start()
    threading.Thread(app.run(host='0.0.0.0', debug=False, use_reloader=False))
