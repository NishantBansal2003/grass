from grass.gunittest.case import TestCase
from grass.gunittest.gmodules import SimpleModule

import json


class TestRWhatColor(TestCase):
    input = "elevation"
    value = "50\n100\n135\n156\nbogus"

    @classmethod
    def setUpClass(cls):
        cls.use_temp_region()
        cls.runModule("g.region", raster=cls.input, flags="p")

    @classmethod
    def tearDownClass(cls):
        cls.del_temp_region()

    def test_r_what_color_plain(self):
        """Test r.what.color command for plain output format."""
        module = SimpleModule(
            "r.what.color", input=self.input, flags="i", stdin=self.value
        )
        self.runModule(module)
        result = module.outputs.stdout
        expected = [
            "50: *",
            "100: 255:229:0",
            "135: 195:127:59",
            "156: 23:22:21",
            "*: *",
        ]

        # Replacing '\r' because Windows uses '\r\n' for line endings, but we
        # want to remove the '\r' (carriage return) to standardize line endings
        result = result.replace("\r", "")
        result_lines = [line for line in result.split("\n") if line.strip() != ""]

        self.assertListEqual(result_lines, expected, "Mismatch in print output (plain)")

    def test_r_what_color_plain_with_format_option(self):
        """Test r.what.color command with format option for plain text output format."""
        module = SimpleModule(
            "r.what.color",
            input=self.input,
            flags="i",
            stdin=self.value,
            format="#%02X%02X%02X",
            output_format="plain",
        )
        self.runModule(module)
        result = module.outputs.stdout
        expected = ["50: *", "100: #FFE500", "135: #C37F3B", "156: #171615", "*: *"]

        # Replacing '\r' because Windows uses '\r\n' for line endings, but we
        # want to remove the '\r' (carriage return) to standardize line endings
        result = result.replace("\r", "")
        result_lines = [line for line in result.split("\n") if line.strip() != ""]

        self.assertListEqual(result_lines, expected, "Mismatch in print output (plain)")

    def test_r_what_color_json_with_triplet_option(self):
        """Test r.what.color command with triplet option for json output format."""
        module = SimpleModule(
            "r.what.color",
            input=self.input,
            flags="i",
            stdin=self.value,
            output_format="json",
            color_format="triplet",
        )
        self.runModule(module)
        result = json.loads(module.outputs.stdout)
        expected = [
            {"color": "*", "value": 50},
            {"color": "255:229:0", "value": 100},
            {"color": "195:127:59", "value": 135},
            {"color": "23:22:21", "value": 156},
            {"color": "*", "value": "*"},
        ]

        self.assertListEqual(result, expected, "Mismatch in print output (JSON)")

    def test_r_what_color_json_with_rgb_option(self):
        """Test r.what.color command with rgb option for json output format."""
        module = SimpleModule(
            "r.what.color",
            input=self.input,
            flags="i",
            stdin=self.value,
            output_format="json",
            color_format="rgb",
        )
        self.runModule(module)
        result = json.loads(module.outputs.stdout)
        expected = [
            {"color": "*", "value": 50},
            {"color": "rgb(255, 229, 0)", "value": 100},
            {"color": "rgb(195, 127, 59)", "value": 135},
            {"color": "rgb(23, 22, 21)", "value": 156},
            {"color": "*", "value": "*"},
        ]

        self.assertListEqual(result, expected, "Mismatch in print output (JSON)")

    def test_r_what_color_json_with_hex_option(self):
        """Test r.what.color command with hex option for json output format."""
        module = SimpleModule(
            "r.what.color",
            input=self.input,
            flags="i",
            stdin=self.value,
            output_format="json",
            color_format="hex",
        )
        self.runModule(module)
        result = json.loads(module.outputs.stdout)
        expected = [
            {"color": "*", "value": 50},
            {"color": "#FFE500", "value": 100},
            {"color": "#C37F3B", "value": 135},
            {"color": "#171615", "value": 156},
            {"color": "*", "value": "*"},
        ]

        self.assertListEqual(result, expected, "Mismatch in print output (JSON)")

    def test_r_what_color_json_with_hsv_option(self):
        """Test r.what.color command with hsv option for json output format."""
        module = SimpleModule(
            "r.what.color",
            input=self.input,
            flags="i",
            stdin=self.value,
            output_format="json",
            color_format="hsv",
        )
        self.runModule(module)
        result = json.loads(module.outputs.stdout)
        expected = [
            {"color": "*", "value": 50},
            {"color": "hsv(53, 100, 100)", "value": 100},
            {"color": "hsv(30, 69, 76)", "value": 135},
            {"color": "hsv(30, 8, 9)", "value": 156},
            {"color": "*", "value": "*"},
        ]

        self.assertListEqual(result, expected, "Mismatch in print output (JSON)")


if __name__ == "__main__":
    from grass.gunittest.main import test

    test()
