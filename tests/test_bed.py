from unittest import TestCase
from bed.bed import Bed
from bed.sensor.util.sensor_data_utils import load_sensor_dataframe
from body.body import Patient


class TestBed(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_file = "test_files/data.csv"
        cls.bed = Bed(patient=Patient())
        data_df = load_sensor_dataframe(cls.test_file)
        sensor = cls.bed.get_pressure_sensor()
        sensor.append_sensor_data(data_df)
        sensor.set_current_frame(data_df)

    def test_analyze_sensor_data(self):
        self.fail()

    def test_calculate_deflatable_regions(self):
        self.fail()

    def test_calculate_inflatable_regions(self):
        self.fail()

    def test_print_stats(self):
        self.fail()

    def test_generate_bed_status_json(self):
        bed = self.bed
        bed.generate_bed_status_json()
        return

