from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.script.core import read_command, parse_command


class TestVWhatRast(TestCase):
    """Unit tests for the v.what.rast module"""

    test_raster = "test_raster"
    float_raster = "float_raster"
    test_vector = "test_vector"

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.use_temp_region()
        cls.runModule("g.region", s=0, n=5, w=0, e=5, res=1)
        cls.runModule(
            "r.mapcalc",
            expression=(f"{cls.test_raster} = if(col() < 5, col(), null())"),
        )
        cls.runModule(
            "r.mapcalc",
            expression=(f"{cls.float_raster} = if(col() < 5, col() / 2., 4.5)"),
        )
        cls.runModule("v.mkgrid", map=f"{cls.test_vector}", grid=[5, 5], type="point")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        cls.del_temp_region()
        cls.runModule(
            "g.remove",
            flags="f",
            type="raster",
            name=[cls.test_raster, cls.float_raster],
        )
        cls.runModule(
            "g.remove",
            flags="f",
            type="vector",
            name=[cls.test_vector],
        )

    def test_plain_output_int(self):
        """Verify plain text output with integer map."""
        result = read_command(
            "v.what.rast", map=self.test_vector, raster=self.test_raster, flags="p"
        ).splitlines()
        expected = [
            "25|*",
            "24|4",
            "23|3",
            "22|2",
            "21|1",
            "17|2",
            "20|*",
            "16|1",
            "19|4",
            "18|3",
            "13|3",
            "11|1",
            "12|2",
            "14|4",
            "15|*",
            "6|1",
            "10|*",
            "9|4",
            "8|3",
            "7|2",
            "2|2",
            "5|*",
            "4|4",
            "3|3",
            "1|1",
        ]
        self.assertEqual(result, expected)

        # Verify with explicit plain format
        result = read_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.test_raster,
            flags="p",
            format="plain",
        ).splitlines()
        self.assertEqual(result, expected)

    def test_csv_output_int(self):
        """Verify CSV style output with integer map."""
        result = read_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.test_raster,
            flags="p",
            format="csv",
        ).splitlines()
        expected = [
            "cat,value",
            "25,*",
            "24,4",
            "23,3",
            "22,2",
            "21,1",
            "17,2",
            "20,*",
            "16,1",
            "19,4",
            "18,3",
            "13,3",
            "11,1",
            "12,2",
            "14,4",
            "15,*",
            "6,1",
            "10,*",
            "9,4",
            "8,3",
            "7,2",
            "2,2",
            "5,*",
            "4,4",
            "3,3",
            "1,1",
        ]
        self.assertEqual(result, expected)

        # Verify with pipe separator
        result = read_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.test_raster,
            flags="p",
            format="csv",
            separator="pipe",
        ).splitlines()
        expected = [
            "cat|value",
            "25|*",
            "24|4",
            "23|3",
            "22|2",
            "21|1",
            "17|2",
            "20|*",
            "16|1",
            "19|4",
            "18|3",
            "13|3",
            "11|1",
            "12|2",
            "14|4",
            "15|*",
            "6|1",
            "10|*",
            "9|4",
            "8|3",
            "7|2",
            "2|2",
            "5|*",
            "4|4",
            "3|3",
            "1|1",
        ]
        self.assertEqual(result, expected)

    def test_json_output_int(self):
        """Verify JSON style output with integer map."""
        result = parse_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.test_raster,
            flags="p",
            format="json",
        )
        expected = [
            {"category": 25, "value": None},
            {"category": 24, "value": 4},
            {"category": 23, "value": 3},
            {"category": 22, "value": 2},
            {"category": 21, "value": 1},
            {"category": 17, "value": 2},
            {"category": 20, "value": None},
            {"category": 16, "value": 1},
            {"category": 19, "value": 4},
            {"category": 18, "value": 3},
            {"category": 13, "value": 3},
            {"category": 11, "value": 1},
            {"category": 12, "value": 2},
            {"category": 14, "value": 4},
            {"category": 15, "value": None},
            {"category": 6, "value": 1},
            {"category": 10, "value": None},
            {"category": 9, "value": 4},
            {"category": 8, "value": 3},
            {"category": 7, "value": 2},
            {"category": 2, "value": 2},
            {"category": 5, "value": None},
            {"category": 4, "value": 4},
            {"category": 3, "value": 3},
            {"category": 1, "value": 1},
        ]
        self.assertEqual(result, expected)

    def test_plain_output_float(self):
        """Verify plain text output with float map."""
        result = read_command(
            "v.what.rast", map=self.test_vector, raster=self.float_raster, flags="p"
        ).splitlines()
        expected = [
            "25|4.5",
            "24|2",
            "23|1.5",
            "22|1",
            "21|0.5",
            "17|1",
            "20|4.5",
            "16|0.5",
            "19|2",
            "18|1.5",
            "13|1.5",
            "11|0.5",
            "12|1",
            "14|2",
            "15|4.5",
            "6|0.5",
            "10|4.5",
            "9|2",
            "8|1.5",
            "7|1",
            "2|1",
            "5|4.5",
            "4|2",
            "3|1.5",
            "1|0.5",
        ]
        self.assertEqual(result, expected)

        # Verify with explicit plain format
        result = read_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.float_raster,
            flags="p",
            format="plain",
        ).splitlines()
        self.assertEqual(result, expected)

    def test_csv_output_float(self):
        """Verify CSV style output with float map."""
        result = read_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.float_raster,
            flags="p",
            format="csv",
        ).splitlines()
        expected = [
            "cat,value",
            "25,4.5",
            "24,2",
            "23,1.5",
            "22,1",
            "21,0.5",
            "17,1",
            "20,4.5",
            "16,0.5",
            "19,2",
            "18,1.5",
            "13,1.5",
            "11,0.5",
            "12,1",
            "14,2",
            "15,4.5",
            "6,0.5",
            "10,4.5",
            "9,2",
            "8,1.5",
            "7,1",
            "2,1",
            "5,4.5",
            "4,2",
            "3,1.5",
            "1,0.5",
        ]
        self.assertEqual(result, expected)

        # Verify with pipe separator
        result = read_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.float_raster,
            flags="p",
            format="csv",
            separator="pipe",
        ).splitlines()
        expected = [
            "cat|value",
            "25|4.5",
            "24|2",
            "23|1.5",
            "22|1",
            "21|0.5",
            "17|1",
            "20|4.5",
            "16|0.5",
            "19|2",
            "18|1.5",
            "13|1.5",
            "11|0.5",
            "12|1",
            "14|2",
            "15|4.5",
            "6|0.5",
            "10|4.5",
            "9|2",
            "8|1.5",
            "7|1",
            "2|1",
            "5|4.5",
            "4|2",
            "3|1.5",
            "1|0.5",
        ]
        self.assertEqual(result, expected)

    def test_json_output_float(self):
        """Verify JSON style output with float map."""
        result = parse_command(
            "v.what.rast",
            map=self.test_vector,
            raster=self.float_raster,
            flags="p",
            format="json",
        )
        expected = [
            {"category": 25, "value": 4.5},
            {"category": 24, "value": 2},
            {"category": 23, "value": 1.5},
            {"category": 22, "value": 1},
            {"category": 21, "value": 0.5},
            {"category": 17, "value": 1},
            {"category": 20, "value": 4.5},
            {"category": 16, "value": 0.5},
            {"category": 19, "value": 2},
            {"category": 18, "value": 1.5},
            {"category": 13, "value": 1.5},
            {"category": 11, "value": 0.5},
            {"category": 12, "value": 1},
            {"category": 14, "value": 2},
            {"category": 15, "value": 4.5},
            {"category": 6, "value": 0.5},
            {"category": 10, "value": 4.5},
            {"category": 9, "value": 2},
            {"category": 8, "value": 1.5},
            {"category": 7, "value": 1},
            {"category": 2, "value": 1},
            {"category": 5, "value": 4.5},
            {"category": 4, "value": 2},
            {"category": 3, "value": 1.5},
            {"category": 1, "value": 0.5},
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    test()
