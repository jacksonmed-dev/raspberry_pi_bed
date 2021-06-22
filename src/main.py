from bed.bed import Bed
from src.directory_monitor import OnMyWatch
from body.body import Patient

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = "/home/pi/Desktop/sensor"
    p = Patient()
    bed = Bed(patient=p)
    watch = OnMyWatch(bed=bed, path=path)
    watch.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
