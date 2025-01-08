def json_to_md(data, depth=1):
    """
    Convert a JSON-like Python object (dict/list/scalar) to a Markdown string.

    :param data: The data to convert (typically a dict or list).
    :param depth: Current heading depth (starts at 1).
    :return: A Markdown string.
    """

    valid_types = (dict, list, str, int, float, bool, type(None))
    if not isinstance(data, valid_types):
        raise TypeError(f"Input data must be a JSON-serializable type, got {type(data).__name__}")

    # For containers, validate all nested elements
    if isinstance(data, (dict, list)):
        try:
            import json
            json.dumps(data)  # This will raise TypeError if data contains non-JSON-serializable types
        except TypeError as e:
            raise TypeError(f"Input contains non-JSON-serializable types: {str(e)}")


    if not isinstance(data, (dict, list)):
        raise TypeError(f"Input data must be a JSON-serializable type, got {type(data).__name__}")

    md_lines = []

    if isinstance(data, dict):
        # For each key, add a heading and then recurse on its value
        for key, value in data.items():
            md_lines.append(f"{'#' * depth} {key}")
            md_lines.append(json_to_markdown(value, depth + 1))

    elif isinstance(data, list):
        # Check if it's a list of dictionaries
        if all(isinstance(item, dict) for item in data) and data:
            # Collect *all* keys across the entire list of dicts
            # in the order they first appear
            header_keys = []
            for item in data:
                for k in item.keys():
                    if k not in header_keys:
                        header_keys.append(k)

            # Construct table header
            header_row = "| " + " | ".join(header_keys) + " |"
            separator_row = "| " + " | ".join("---" for _ in header_keys) + " |"
            md_lines.append(header_row)
            md_lines.append(separator_row)

            # Add each row
            for item in data:
                row_values = [str(item.get(k, "")) for k in header_keys]
                row_line = "| " + " | ".join(row_values) + " |"
                md_lines.append(row_line)

        else:
            # Otherwise, render as bullet points (or recursively handle items)
            for item in data:
                # Recursively convert item to markdown
                item_md = json_to_markdown(item, depth + 1)
                item_lines = item_md.split("\n")

                if len(item_lines) == 1:
                    # A simple scalar or one-line item
                    md_lines.append(f"* {item_lines[0]}")
                else:
                    # Multi-line item, bullet the first line, then indent subsequent lines
                    first_line = item_lines[0]
                    md_lines.append(f"* {first_line}")
                    for line in item_lines[1:]:
                        md_lines.append(f"  {line}")
    else:
        # Scalar (string, int, float, bool, None)
        md_lines.append(str(data))

    return "\n".join(md_lines)


# -------------- Example usage --------------

if __name__ == "__main__":
    # Sample JSON-like data
    sample_data = {
        "title": "Example JSON",
        "metadata": {
            "author": "John Doe",
            "version": 1.2,
            "tags": ["sample", "json", "markdown", "converter"]
        },
        "records": [
            {"name": "Alice", "age": 30, "city": "London"},
            {"name": "Bob", "age": 25, "city": "New York"},
        ],
        "recording": [
            {"Country": "Yes"},
            {"Pop": "No"},
            {"Classic": "No"}
        ],
        "notes": [
            "This is a bullet point list.",
            "Another bullet point.",
            {"nested_note": "Even deeper data"}
        ]
    }

    md_output = json_to_markdown(sample_data)
    print(md_output)