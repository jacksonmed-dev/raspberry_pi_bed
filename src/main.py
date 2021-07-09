import os
import sys
import threading
from bed.bed import Bed
from body.body import Patient
from bed.sensor.directory_monitor import OnMyWatch
from homework.massage import Massage
from server.flask_server import create_server

if os.uname()[4][:3] == 'arm':
    path = "/home/pi/Desktop/sensor_data"
else:
    path = "/home/cjstanfi/Desktop/sensor_data"


if __name__ == "__main__":
    p = Patient()
    bed = Bed(patient=p)
    watch = OnMyWatch(bed=bed, path=path)
    app = create_server(bed=bed)

    if len(sys.argv) == 1:
        watch.run()
    elif sys.argv[1] == 'message':
        message = Massage()
        message.start()
        threading.Thread(message.start())
    else:
        print("Invalid argument passed")

    threading.Thread(app.run(host='0.0.0.0', debug=False, use_reloader=False))
