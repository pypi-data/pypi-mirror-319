import unittest
from TextFormatConverter import json_to_md


class TestJsonToMd(unittest.TestCase):
    def test_json_to_md(self):
        data = {
            "key1": "value1",
            "key2": "value2",
            "key3": {
                "key3.1": "value3.1",
                "key3.2": "value3.2",
                "key3.3": ["value3.3.1", "value3.3.2"]
            },
            "key4": [
                {"key4.1": "value4.1"},
                {"key4.2": "value4.2"}
            ]
        }

        expected = """# key1
value1
# key2
value2
# key3
## key3.1
value3.1
## key3.2
value3.2
## key3.3
* value3.3.1
* value3.3.2
# key4
| key4.1 | key4.2 |
| --- | --- |
| value4.1 |  |
|  | value4.2 |"""
        self.assertEqual(json_to_md(data), expected)

    def test_illegal_input(self):
        data = "This is a string, not a dictionary"
        self.assertEqual(json_to_md(data), "This is a string, not a dictionary")




if __name__ == "__main__":
    unittest.main()

