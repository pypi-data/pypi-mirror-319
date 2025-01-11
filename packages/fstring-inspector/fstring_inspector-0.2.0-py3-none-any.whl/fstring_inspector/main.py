import re
from pathlib import Path


def inspect_fstring(line):
    # Regular expression to find f-strings
    fstring_pattern = re.compile(r'f["\'].*?["\']')

    matches = fstring_pattern.findall(line)

    if line.count('"') > 2 or line.count("'") > 2:
        for fstring in matches:
            # Check if there are nested quotes of the same type
            if (fstring.count('"') > 1 and fstring.count("'") == 0) or (fstring.count("'") > 1 and fstring.count('"') == 0):
                return line


def inspect_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    problematic_lines = []

    for line_number, line in enumerate(lines, start=1):
        result = inspect_fstring(line)
        if result:
            problematic_lines.append((line_number, result.strip()))

    return problematic_lines


def inspect_directory(directory_path):
    results = {}
    directory = Path(directory_path)
    
    # Recursively find all python files
    for file_path in directory.rglob(f"*.py"):
        try:
            problematic_lines = inspect_file(file_path)
            if problematic_lines:
                results[str(file_path)] = problematic_lines
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return results
