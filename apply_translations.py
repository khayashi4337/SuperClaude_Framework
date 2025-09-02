import json
import os

def apply_translations_to_file(filepath, translations):
    """
    Applies translations to a single file by replacing original English strings
    with their Japanese counterparts.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file {filepath} to apply translations.")
        return

    # Sort translations by length of the original string, descending.
    # This prevents issues where a shorter string is a substring of a longer one.
    sorted_translations = sorted(translations.items(), key=lambda item: len(item[0]), reverse=True)

    modified_content = content
    changes_made = 0
    for original, translated in sorted_translations:
        # A simple, but potentially risky replacement.
        # The is_user_facing heuristic should have filtered out most code strings.
        if original in modified_content:
            # We must be careful not to replace parts of already translated strings.
            # This is a simple check.
            if translated not in modified_content:
                 modified_content = modified_content.replace(original, translated)
                 changes_made += 1

    if changes_made > 0:
        print(f"Applying {changes_made} translation(s) to {filepath}...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
    else:
        print(f"No changes needed for {filepath}.")


def main():
    """
    Main function to apply translations from translated_strings.json.
    """
    translations_filename = 'translated_strings.json'
    if not os.path.exists(translations_filename):
        print(f"Error: {translations_filename} not found. Please run steps 2 and 3 first.")
        return

    with open(translations_filename, 'r', encoding='utf-8') as f:
        all_translations = json.load(f)

    for filepath, translations in all_translations.items():
        if not os.path.exists(filepath):
            print(f"Warning: Source file not found, skipping: {filepath}")
            continue
        apply_translations_to_file(filepath, translations)

    print("\nTranslation application complete.")

if __name__ == '__main__':
    main()
