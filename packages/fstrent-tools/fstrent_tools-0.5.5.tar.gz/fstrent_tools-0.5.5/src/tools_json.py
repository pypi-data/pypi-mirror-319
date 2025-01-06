import json
import decimal
from tools_files import dir_val

__all__ = [
    'format_json',
    'merge_json',
    'read_json',
    'search_json',
    'validate_json',
    'write_json',
    'json_safe',
    'json_file_read',
    'json_file_write'
]

def json_safe(obj):
    """Convert object to JSON-safe format."""
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    return obj

def format_json(json_data, indent=4):
    """Format JSON data with specified indentation."""
    return json.dumps(json_data, indent=indent, default=json_safe)

def json_file_read(file_path):
    """Read JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def json_file_write(data, file_path, indent=4):
    """Write data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, default=json_safe)

def read_json(file_path):
    """Read and parse JSON data from a file."""
    try:
        return json_file_read(file_path)
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {str(e)}")
        return None

def write_json(data, file_path, indent=4):
    """Write data to a JSON file with error handling."""
    try:
        dir_val(file_path)  # Ensure directory exists
        json_file_write(data, file_path, indent)
        return True
    except Exception as e:
        print(f"Error writing JSON file {file_path}: {str(e)}")
        return False

def merge_json(json1, json2):
    """Merge two JSON objects."""
    if isinstance(json1, dict) and isinstance(json2, dict):
        result = json1.copy()
        for key, value in json2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_json(result[key], value)
            else:
                result[key] = value
        return result
    return json2

def validate_json(json_str):
    """Validate JSON string format."""
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def search_json(json_data, key, default=None):
    """Search for a key in nested JSON data."""
    if isinstance(json_data, dict):
        if key in json_data:
            return json_data[key]
        for value in json_data.values():
            result = search_json(value, key, default)
            if result != default:
                return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = search_json(item, key, default)
            if result != default:
                return result
    return default
