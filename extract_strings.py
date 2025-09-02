import ast
import json
import re
import os

def contains_japanese(s):
    """Checks if a string contains Japanese characters."""
    return any(
        '\u3040' <= char <= '\u309F' or  # Hiragana
        '\u30A0' <= char <= '\u30FF' or  # Katakana
        '\u4E00' <= char <= '\u9FFF'      # Kanji
        for char in s
    )

def is_user_facing(s):
    """
    Heuristic to determine if a string is likely user-facing and needs translation.
    """
    if contains_japanese(s):
        return False

    # Must contain at least one space and one letter.
    if ' ' not in s or not any(c.isalpha() for c in s):
        return False

    # Filter out short strings, paths, formats, etc.
    if len(s) < 5:
        return False
    if '/' in s or '\\' in s or '.py' in s or '.js' in s:
        return False
    if s.startswith('%') or s.startswith('='):
        return False
    # Filter out things that look like code snippets
    if '{' in s and '}' in s:
        return False
    # Filter out all-caps constants
    if s.isupper():
        return False

    return True

def extract_from_python(filepath):
    """
    Extracts user-facing strings from a Python file using AST.
    """
    strings = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
            tree = ast.parse(content, filename=filepath)
        except (SyntaxError, ValueError) as e:
            print(f"Could not parse Python file {filepath}: {e}")
            return []

    for node in ast.walk(tree):
        # For Python 3.8+, string constants are ast.Constant
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value
            if is_user_facing(val):
                strings.add(val)
        # For older Python versions
        elif isinstance(node, ast.Str):
            val = node.s
            if is_user_facing(val):
                strings.add(val)

    return sorted(list(strings))

def extract_from_js(filepath):
    """
    Extracts user-facing strings from a JavaScript file using regex.
    This is a simplification and might not cover all edge cases.
    """
    strings = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find single and double quoted strings, ignoring template literals for now.
    pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\''
    for match in re.finditer(pattern, content):
        # The matched string is in group 1 (double quotes) or 2 (single quotes)
        s = match.group(1) if match.group(1) is not None else match.group(2)
        if is_user_facing(s):
            strings.add(s)

    return sorted(list(strings))

def main():
    """
    Main function to extract strings from files listed in files_to_translate.txt
    """
    all_strings = {}
    input_filename = 'files_to_translate.txt'

    if not os.path.exists(input_filename):
        print(f"Error: {input_filename} not found. Please run step 1 first.")
        return

    with open(input_filename, 'r', encoding='utf-8') as f:
        filepaths = [line.strip() for line in f if line.strip()]

    for filepath in filepaths:
        if not os.path.exists(filepath):
            print(f"Warning: File not found, skipping: {filepath}")
            continue

        print(f"Processing {filepath}...")
        extracted = []
        if filepath.endswith('.py'):
            extracted = extract_from_python(filepath)
        elif filepath.endswith('.js'):
            extracted = extract_from_js(filepath)

        if extracted:
            all_strings[filepath] = extracted

    output_filename = 'translatable_strings.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_strings, f, indent=2, ensure_ascii=False)

    print(f"\nExtraction complete. Found strings in {len(all_strings)} files.")
    print(f"Output written to {output_filename}")

if __name__ == '__main__':
    main()
