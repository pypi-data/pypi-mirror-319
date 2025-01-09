#!/usr/bin/env python3
# projectcompactor/cli.py

import os
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Attempt to use python-magic for MIME detection if available
try:
    import magic
    MAGIC_AVAILABLE = True
    _magic_mime = magic.Magic(mime=True)
except ImportError:
    MAGIC_AVAILABLE = False

DEFAULT_OUTPUT = "project_structure.txt"

# Fallback text extensions if python-magic isn't available or fails
FALLBACK_TEXT_EXTENSIONS = {
    '.txt', '.py', '.html', '.css', '.js', '.md', '.json',
    '.xml', '.csv', '.yaml', '.yml', '.ini', '.cfg', '.bat', '.sh',
    '.java', '.c', '.cpp', '.rb', '.go', '.ts', '.jsx', '.tsx'
}


def main():
    """
    Main entry point for the ProjectCompactor tool.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("\nWelcome to the Interactive Project Compactor v6.9420!\n")

    start_path = os.getcwd()

    # 1) Gather the full directory tree, skipping project_compactor files
    tree_data = gather_tree(start_path)

    # 2) Flatten with hierarchical numbering
    flattened, unique_extensions = build_numbered_listing(tree_data)

    # 3) Display them to the user
    index_map, next_index = display_items(flattened)
    ext_index_map = display_extensions(unique_extensions, next_index)
    combined_index_map = {**index_map, **ext_index_map}

    # 4) Prompt user to pick items to include
    chosen_indices = prompt_for_selection(combined_index_map)

    # 5) Compute final sets of included directories and files
    included_dirs, included_files = resolve_inclusions(chosen_indices, combined_index_map, start_path)

    # 6) Decide output file name
    output_file = handle_output_file_name(DEFAULT_OUTPUT)

    # 7) Generate final output
    generate_output(start_path, included_dirs, included_files, output_file)

    print(f"\nDone! The output has been saved to '{output_file}'.\n")


def gather_tree(start_path):
    """
    Recursively gather directories/files from start_path, skipping:
      - this cli.py
      - any file named 'project_structure*.txt'
    """
    items = []

    # We'll skip the main script name, if found in the top-level
    # since we don't want the script to appear in the summary
    def should_skip(name):
        # skip any project_structure*.txt files
        if name.startswith("project_structure") and name.endswith(".txt"):
            return True
        # skip if file is named exactly like this script
        # if you want to skip exact "cli.py" or "generator.py", do that:
        if name == "cli.py":
            return True
        return False

    for entry in sorted(os.listdir(start_path)):
        if should_skip(entry):
            continue
        full_path = os.path.join(start_path, entry)
        if os.path.isdir(full_path):
            items.append({
                "name": entry,
                "path": full_path,
                "is_dir": True,
                "children": gather_tree(full_path)
            })
        else:
            _, ext = os.path.splitext(entry)
            items.append({
                "name": entry,
                "path": full_path,
                "is_dir": False,
                "ext": ext if ext else None
            })
    return items


def build_numbered_listing(tree_data):
    """
    Creates a list of items with hierarchical numbering:
      1, 1.1, 1.2, 2, 2.1, etc.
    Returns:
      flattened: list of (display_num, indent_level, is_dir, name, path, ext)
      unique_extensions: set of all file extensions
    """
    flattened = []
    unique_extensions = set()

    def dfs(items, prefix, indent_level):
        counter = 1
        for i in items:
            display_num = prefix + str(counter) if prefix else str(counter)
            if i["is_dir"]:
                flattened.append((display_num, indent_level, True, i["name"], i["path"], None))
                dfs(i["children"], display_num + ".", indent_level + 1)
            else:
                ext = i["ext"]
                if ext:
                    unique_extensions.add(ext)
                flattened.append((display_num, indent_level, False, i["name"], i["path"], ext))
            counter += 1

    dfs(tree_data, prefix="", indent_level=0)
    return flattened, unique_extensions


def display_items(flattened):
    """
    Show the directories/files with indentation and hierarchical numbering.
    Return an index_map and the next integer index for filetype listing.
    """
    print("Discovered directories and files:\n")
    index_map = {}
    max_top_level_num = 0

    for (disp_num, indent, is_dir, name, path, ext) in flattened:
        index_map[disp_num] = {
            "kind": "dir" if is_dir else "file",
            "path": path,
            "ext": ext
        }
        indent_str = "    " * indent
        label = "(Dir)" if is_dir else "(File)"
        print(f"{disp_num}. {indent_str}{label} {name}")

        # track the integer portion of the display_num to see how high it goes
        top_int = int(disp_num.split(".")[0])
        max_top_level_num = max(max_top_level_num, top_int)

    print()
    return index_map, max_top_level_num + 1


def display_extensions(unique_extensions, start_index):
    """
    Display each unique extension with a numeric index (start_index, start_index+1, ...).
    Return a dict that maps these indexes to extension info.
    """
    ext_map = {}
    if not unique_extensions:
        print("No unique file extensions detected.\n")
        return ext_map

    print("Unique file extensions detected:\n")
    i = start_index
    for ext in sorted(unique_extensions):
        disp_num = str(i)
        ext_map[disp_num] = {
            "kind": "extension",
            "ext": ext,
            "path": None
        }
        print(f"{disp_num}. (Filetype) {ext}")
        i += 1

    print()
    return ext_map


def prompt_for_selection(index_map):
    """
    Ask the user for indices to INCLUDE.
    Returns a set of chosen index strings.
    """
    print("Please enter the indices of items you want to INCLUDE, comma-separated (e.g., 1,2.1,3).")
    print(" - Including a directory includes all sub-items.")
    print(" - Including a file includes only that file.")
    print(" - Including a filetype (e.g. .py) includes all files with that extension.")
    print("Enter `*` to include everything, or press Enter to include none.\n")

    user_input = input("Your selection: ").strip()
    if not user_input:
        print("No selection made, so no items will be included.\n")
        return set()
    if user_input == "*":
        print("You chose to include everything.\n")
        return set(index_map.keys())

    chosen = set()
    for chunk in user_input.split(","):
        chunk = chunk.strip()
        if chunk in index_map:
            chosen.add(chunk)
        else:
            # If user typed something that doesn't exist in index_map, ignore it
            pass

    if chosen:
        print(f"You chose indices: {sorted(list(chosen))}\n")
    else:
        print("No valid indices recognized.\n")
    return chosen


def resolve_inclusions(chosen_indices, index_map, start_path):
    """
    From the chosen indices, gather included directories and files.
    - If 'kind' is 'dir', recursively include everything under that directory.
    - If 'kind' is 'file', include that single file.
    - If 'kind' is 'extension', include all files with that extension.
    """
    included_dirs = set()
    included_files = set()
    chosen_extensions = set()

    for disp_num in chosen_indices:
        info = index_map[disp_num]
        kind = info["kind"]
        if kind == "extension":
            chosen_extensions.add(info["ext"])
        elif kind == "dir":
            gather_dir_contents(info["path"], included_dirs, included_files)
        elif kind == "file":
            included_files.add(os.path.abspath(info["path"]))

    # Add all files that match chosen extensions
    if chosen_extensions:
        for root, dirs, files in os.walk(start_path):
            for f in files:
                abs_fp = os.path.abspath(os.path.join(root, f))
                _, ext = os.path.splitext(f)
                if ext in chosen_extensions:
                    included_files.add(abs_fp)

    # Ensure parent directories of included files are also included
    for file_path in list(included_files):
        parent = os.path.dirname(file_path)
        while parent.startswith(start_path):
            included_dirs.add(parent)
            parent = os.path.dirname(parent)

    return included_dirs, included_files


def gather_dir_contents(dir_path, included_dirs, included_files):
    """
    Recursively add everything under dir_path to included_dirs/files.
    """
    for root, dirs, files in os.walk(dir_path):
        included_dirs.add(os.path.abspath(root))
        for f in files:
            included_files.add(os.path.abspath(os.path.join(root, f)))


def handle_output_file_name(default_name):
    """
    If default_name exists, prompt whether to Overwrite (O), Increment (I), or Rename (R).
    """
    if not os.path.exists(default_name):
        return default_name

    print(f"File '{default_name}' already exists. Overwrite (O), Increment (I), or Rename (R)?")
    choice = input("[O/I/R]? ").strip().lower()
    if choice == 'o':
        return default_name
    elif choice == 'i':
        base, ext = os.path.splitext(default_name)
        counter = 1
        while True:
            new_name = f"{base}_{counter}{ext}"
            if not os.path.exists(new_name):
                return new_name
            counter += 1
    elif choice == 'r':
        new_name = input("Enter new filename: ").strip()
        if not new_name:
            return default_name
        return new_name
    else:
        return default_name


def generate_output(start_path, included_dirs, included_files, output_file):
    """
    Create the final output with:
      # Project Structure
      # File Details
    """
    logging.info("Generating final project structure...")
    tree_str = generate_tree_string(start_path, included_dirs, included_files)

    logging.info("Generating file details...")
    details_str = generate_file_details(included_files, start_path)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# Project Structure\n\n")
        out.write(tree_str)
        out.write("\n\n# File Details\n\n")
        out.write(details_str)


def generate_tree_string(start_path, included_dirs, included_files):
    """
    Builds a hierarchical listing of included dirs/files with indentation.
    """
    lines = []
    for root, dirs, files in os.walk(start_path):
        root_abs = os.path.abspath(root)
        if root_abs not in included_dirs:
            dirs[:] = []
            continue

        level = root_abs.replace(os.path.abspath(start_path), "").count(os.sep)
        indent_str = " " * 4 * level
        name = os.path.basename(root_abs) if os.path.basename(root_abs) else root_abs
        lines.append(f"{indent_str}{name}/")

        dirs[:] = [d for d in dirs if os.path.abspath(os.path.join(root_abs, d)) in included_dirs]
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            fp = os.path.abspath(os.path.join(root_abs, f))
            if fp in included_files:
                lines.append(f"{sub_indent}{f}")

    return "\n".join(lines)


def generate_file_details(included_files, start_path):
    """
    For each included file, produce a section with contents (if text) or mark binary.
    """
    file_paths = sorted(list(included_files))
    logging.info(f"Processing {len(file_paths)} files...")

    output_blocks = []
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as exe:
        futures = [exe.submit(process_single_file, fp, start_path) for fp in file_paths]
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Processing files"):
            output_blocks.append(fut.result())

    return "\n".join(output_blocks)


def process_single_file(absolute_path, start_path):
    """
    Decide if it's text (via python-magic if available) or fallback check.
    Then read if text, else mark as binary.
    """
    relative_path = os.path.relpath(absolute_path, start_path)
    details = [f"## {relative_path}"]

    if is_text_file(absolute_path):
        details.append(f"### Contents of {os.path.basename(absolute_path)}")
        try:
            with open(absolute_path, 'r', encoding='utf-8') as f:
                details.append(f.read())
        except Exception as e:
            details.append(f"[Error reading file: {e}]")
    else:
        details.append(f"[Binary or Non-text file: {os.path.basename(absolute_path)}]")

    details.append("")  # extra newline
    return "\n".join(details)


def is_text_file(file_path):
    """
    Use python-magic if available to check for 'text/*'.
    Otherwise fallback to known text extensions or a quick read test.
    """
    if MAGIC_AVAILABLE:
        try:
            mime = _magic_mime.from_file(file_path)
            return mime.startswith("text/")
        except Exception:
            pass

    # Fallback
    _, ext = os.path.splitext(file_path)
    if ext.lower() in FALLBACK_TEXT_EXTENSIONS:
        return True

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, PermissionError, IsADirectoryError):
        return False
