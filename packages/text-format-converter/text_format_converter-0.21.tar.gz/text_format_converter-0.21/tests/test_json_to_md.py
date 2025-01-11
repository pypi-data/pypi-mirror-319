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



class TestJsonToMd_2(unittest.TestCase):
    def test_json_to_md_2(self):
        data = {
            "document": {
                "Project Documentation": {
                    "value": "\nThis is an introduction paragraph with {\"bold\":\"bold text\"}, {\"italic\":\"italic text\"}, and {\"bold\":\"{\"italic\":\"bold italic text\"}\"}.",
                    "Installation Guide": {
                        "value": [
                            "\nFollow these steps to install the project:",
                            [
                                "API_KEY",
                                "DATABASE_URL",
                                "SECRET_KEY"
                            ]
                        ]
                    },
                    "Usage Examples": {
                        "Basic Usage": {
                            "value": [
                                "\nHere's a simple example of how to use the main function:",
                                [
                                    "Import the module",
                                    "Initialize the class",
                                    "Call the process() method"
                                ]
                            ]
                        },
                        "Advanced Features": {
                            "value": [
                                "\nThe system supports multiple configurations:",
                                [
                                    "Detailed logging",
                                    "Performance metrics",
                                    "Stack traces"
                                ]
                            ]
                        }
                    },
                    "Subtitle": {
                        "value": [
                            "",
                            [
                                "Item 1",
                                "Item 2"
                            ]
                        ]
                    }
                }
            }
        }
                
        print(json_to_md(data))

if __name__ == "__main__":
    unittest.main()

