from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.script.core import read_command, parse_command

points = [
    "1 1",
    "2 1",
    "3 1",
    "4 1",
    "5 1",
    "1 2",
    "2 2",
    "3 2",
    "4 2",
    "5 2",
    "1 3",
    "2 3",
    "3 3",
    "4 3",
    "5 3",
    "1 4",
    "2 4",
    "3 4",
    "4 4",
    "5 4",
    "1 5",
    "2 5",
    "3 5",
    "4 5",
    "5 5",
]


class TestVWhatRast(TestCase):
    """Unit tests for the v.what.rast module"""

    test_raster = "test_raster"
    float_raster = "float_raster"
    test_vector = "test_vector"
    ascii_points = "\n".join(points)

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
        cls.runModule(
            "v.in.ascii",
            input="-",
            output=cls.test_vector,
            separator="space",
            stdin=cls.ascii_points,
        )

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
            "24|*",
            "23|4",
            "22|3",
            "21|2",
            "17|3",
            "19|*",
            "16|2",
            "18|4",
            "13|4",
            "11|2",
            "12|3",
            "14|*",
            "6|2",
            "9|*",
            "8|4",
            "7|3",
            "2|3",
            "4|*",
            "3|4",
            "1|2",
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
            "24,*",
            "23,4",
            "22,3",
            "21,2",
            "17,3",
            "19,*",
            "16,2",
            "18,4",
            "13,4",
            "11,2",
            "12,3",
            "14,*",
            "6,2",
            "9,*",
            "8,4",
            "7,3",
            "2,3",
            "4,*",
            "3,4",
            "1,2",
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
            "24|*",
            "23|4",
            "22|3",
            "21|2",
            "17|3",
            "19|*",
            "16|2",
            "18|4",
            "13|4",
            "11|2",
            "12|3",
            "14|*",
            "6|2",
            "9|*",
            "8|4",
            "7|3",
            "2|3",
            "4|*",
            "3|4",
            "1|2",
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
            {"category": 24, "value": None},
            {"category": 23, "value": 4},
            {"category": 22, "value": 3},
            {"category": 21, "value": 2},
            {"category": 17, "value": 3},
            {"category": 19, "value": None},
            {"category": 16, "value": 2},
            {"category": 18, "value": 4},
            {"category": 13, "value": 4},
            {"category": 11, "value": 2},
            {"category": 12, "value": 3},
            {"category": 14, "value": None},
            {"category": 6, "value": 2},
            {"category": 9, "value": None},
            {"category": 8, "value": 4},
            {"category": 7, "value": 3},
            {"category": 2, "value": 3},
            {"category": 4, "value": None},
            {"category": 3, "value": 4},
            {"category": 1, "value": 2},
        ]
        self.assertEqual(result, expected)

    def test_plain_output_float(self):
        """Verify plain text output with float map."""
        result = read_command(
            "v.what.rast", map=self.test_vector, raster=self.float_raster, flags="p"
        ).splitlines()
        expected = [
            "24|4.5",
            "23|2",
            "22|1.5",
            "21|1",
            "17|1.5",
            "19|4.5",
            "16|1",
            "18|2",
            "13|2",
            "11|1",
            "12|1.5",
            "14|4.5",
            "6|1",
            "9|4.5",
            "8|2",
            "7|1.5",
            "2|1.5",
            "4|4.5",
            "3|2",
            "1|1",
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
            "24,4.5",
            "23,2",
            "22,1.5",
            "21,1",
            "17,1.5",
            "19,4.5",
            "16,1",
            "18,2",
            "13,2",
            "11,1",
            "12,1.5",
            "14,4.5",
            "6,1",
            "9,4.5",
            "8,2",
            "7,1.5",
            "2,1.5",
            "4,4.5",
            "3,2",
            "1,1",
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
            "24|4.5",
            "23|2",
            "22|1.5",
            "21|1",
            "17|1.5",
            "19|4.5",
            "16|1",
            "18|2",
            "13|2",
            "11|1",
            "12|1.5",
            "14|4.5",
            "6|1",
            "9|4.5",
            "8|2",
            "7|1.5",
            "2|1.5",
            "4|4.5",
            "3|2",
            "1|1",
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
            {"category": 24, "value": 4.5},
            {"category": 23, "value": 2},
            {"category": 22, "value": 1.5},
            {"category": 21, "value": 1},
            {"category": 17, "value": 1.5},
            {"category": 19, "value": 4.5},
            {"category": 16, "value": 1},
            {"category": 18, "value": 2},
            {"category": 13, "value": 2},
            {"category": 11, "value": 1},
            {"category": 12, "value": 1.5},
            {"category": 14, "value": 4.5},
            {"category": 6, "value": 1},
            {"category": 9, "value": 4.5},
            {"category": 8, "value": 2},
            {"category": 7, "value": 1.5},
            {"category": 2, "value": 1.5},
            {"category": 4, "value": 4.5},
            {"category": 3, "value": 2},
            {"category": 1, "value": 1},
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    test()
