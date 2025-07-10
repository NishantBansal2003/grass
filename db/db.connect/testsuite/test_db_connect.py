from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.script.core import read_command, parse_command


class TestDbConnect(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runModule("db.connect", flags="c")

    def test_db_connect_plain(self):
        """Test plain text output"""
        result = read_command("db.connect", flags="p")
        self.assertIn("driver: ", result)
        self.assertIn("database: ", result)
        self.assertIn("schema: ", result)
        self.assertIn("group: ", result)

        # Repeat with explicit plain format
        result = read_command("db.connect", flags="p", format="plain")
        self.assertIn("driver: ", result)
        self.assertIn("database: ", result)
        self.assertIn("schema: ", result)
        self.assertIn("group: ", result)

    def test_db_connect_shell(self):
        """Test shell-format output"""
        result = read_command("db.connect", flags="g")
        self.assertIn("driver=", result)
        self.assertIn("database=", result)
        self.assertIn("schema=", result)
        self.assertIn("group=", result)

        # Repeat with explicit shell format
        result = read_command(
            "db.connect",
            flags="p",
            format="shell",
        )
        self.assertIn("driver=", result)
        self.assertIn("database=", result)
        self.assertIn("schema=", result)
        self.assertIn("group=", result)

    def test_db_connect_json(self):
        """Test JSON output"""
        result = parse_command(
            "db.connect",
            flags="p",
            format="json",
        )
        expected_keys = ["driver", "database", "schema", "group"]
        self.assertCountEqual(list(result.keys()), expected_keys)


if __name__ == "__main__":
    test()
