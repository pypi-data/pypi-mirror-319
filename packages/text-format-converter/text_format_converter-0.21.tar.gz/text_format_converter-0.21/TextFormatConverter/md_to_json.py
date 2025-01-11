import json
import re
import os

def md_to_json(md_text):
    # Validate input
    if not isinstance(md_text, str):
        raise ValueError("Input must be a string")
    if not md_text.strip():
        raise ValueError("Input cannot be empty")
        
    try:
        # Split the markdown text into sections based on headers
        sections = parse_markdown_sections(md_text)
        
        # Convert to JSON structure
        json_data = {
            "document": sections
        }
        
        # Validate that the data is JSON serializable
        try:
            return json.dumps(json_data, indent=4)
        except (TypeError, OverflowError) as e:
            raise ValueError(f"Generated data is not JSON serializable: {str(e)}")
            
    except Exception as e:
        raise RuntimeError(f"Failed to process markdown: {str(e)}")

def parse_markdown_sections(md_text):
    sections = {"value": ""}
    section_stack = [(0, sections)]
    current_list = None
    list_indent_stack = []
    previous_indent = 0
    lines = md_text.split('\n')
    
    def get_indent_level(line):
        return len(line) - len(line.lstrip())
        
    def process_list_item(line, indent):
        content = line.lstrip('- *+').strip()
        content = parse_formatting(content)
        
        if not list_indent_stack or indent > list_indent_stack[-1]:
            list_indent_stack.append(indent)
            new_list = [content]
            if current_list:
                if isinstance(current_list[-1], list):
                    current_list[-1].append(new_list)
                else:
                    current_list[-1] = [current_list[-1], new_list]
            return new_list
        elif indent < list_indent_stack[-1]:
            while list_indent_stack and indent < list_indent_stack[-1]:
                list_indent_stack.pop()
            return current_list
        else:
            if current_list:
                current_list.append(content)
            return current_list
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.rstrip()
        current_indent = get_indent_level(line)
        line = line.strip()
        
        if not line:
            if current_list is not None:
                next_is_list = False
                for next_line in lines[i+1:]:
                    if next_line.strip():
                        next_is_list = next_line.strip().startswith(('- ', '* ', '+ '))
                        break
                
                if not next_is_list:
                    if section_stack:
                        current_dict = section_stack[-1][1]
                        # Store list separately from text
                        if "value" not in current_dict:
                            current_dict["value"] = current_list
                        elif isinstance(current_dict["value"], str):
                            current_dict["value"] = [current_dict["value"], current_list]
                        elif isinstance(current_dict["value"], list):
                            current_dict["value"].append(current_list)
                    current_list = None
                    list_indent_stack = []
            continue
            
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            if current_list is not None:
                if section_stack:
                    current_dict = section_stack[-1][1]
                    # Store list separately from text
                    if "value" not in current_dict:
                        current_dict["value"] = current_list
                    elif isinstance(current_dict["value"], str):
                        current_dict["value"] = [current_dict["value"], current_list]
                    elif isinstance(current_dict["value"], list):
                        current_dict["value"].append(current_list)
                current_list = None
                list_indent_stack = []
            
            level = len(header_match.group(1))
            title = parse_formatting(header_match.group(2))
            
            new_section = {"value": ""}
            
            while section_stack and section_stack[-1][0] >= level:
                section_stack.pop()
                
            current_dict = section_stack[-1][1]
            current_dict[title] = new_section
            section_stack.append((level, new_section))
            
        elif line.startswith(('- ', '* ', '+ ')):
            if current_list is None:
                current_list = []
            
            current_list = process_list_item(original_line, current_indent)
                
        else:
            if current_list is not None:
                if current_indent > previous_indent:
                    last_item = current_list[-1]
                    if isinstance(last_item, str):
                        current_list[-1] = last_item + "\n" + parse_formatting(line)
                    continue
                else:
                    if section_stack:
                        current_dict = section_stack[-1][1]
                        # Store list separately from text
                        if "value" not in current_dict:
                            current_dict["value"] = current_list
                        elif isinstance(current_dict["value"], str):
                            current_dict["value"] = [current_dict["value"], current_list]
                        elif isinstance(current_dict["value"], list):
                            current_dict["value"].append(current_list)
                    current_list = None
                    list_indent_stack = []
            
            text = parse_formatting(line)
            current_dict = section_stack[-1][1]
            
            # Handle mixed content by converting to array
            if "value" not in current_dict:
                current_dict["value"] = text
            elif isinstance(current_dict["value"], str):
                if text:  # Only append non-empty text
                    current_dict["value"] = current_dict["value"] + "\n" + text
            elif isinstance(current_dict["value"], list):
                current_dict["value"].append(text)
        
        previous_indent = current_indent
    
    if current_list is not None:
        if section_stack:
            current_dict = section_stack[-1][1]
            if "value" not in current_dict:
                current_dict["value"] = current_list
            elif isinstance(current_dict["value"], str):
                current_dict["value"] = [current_dict["value"], current_list]
            elif isinstance(current_dict["value"], list):
                current_dict["value"].append(current_list)
    
    def cleanup(d):
        if isinstance(d, dict):
            result = {}
            for k, v in d.items():
                if k == "value":
                    if v:
                        result[k] = v
                else:
                    cleaned = cleanup(v)
                    if cleaned:
                        result[k] = cleaned
            return result
        return d
    
    return cleanup(sections)

def parse_formatting(text):
    # Convert bold
    text = re.sub(r'\*\*(.+?)\*\*', r'{"bold":"\1"}', text)
    # Convert italic
    text = re.sub(r'\*(.+?)\*', r'{"italic":"\1"}', text)
    return text

# Example usage
if __name__ == "__main__":
    md_text = """
    # Project Documentation

    This is an introduction paragraph with **bold text**, *italic text*, and ***bold italic text***.

    ## Installation Guide

    Follow these steps to install the project:

    - Install Python 3.8 or higher
    - Run `pip install requirements.txt`
    - Configure your *.env* file with the following:
        - API_KEY
        - DATABASE_URL
        - SECRET_KEY

    ## Usage Examples

    ### Basic Usage

    Here's a simple example of how to use the main function:
    
    - Import the module
    - Initialize the class
    - Call the process() method

    ### Advanced Features

    The system supports multiple configurations:

    - **High Performance Mode**
        - Enables multi-threading
        - Optimizes memory usage
        - *Requires* 8GB RAM minimum
    
    - **Debug Mode**
        - Detailed logging
        - Performance metrics
        - Stack traces

    ## Subtitle

    - Item 1
    - Item 2
    """
    print(md_to_json(md_text))
