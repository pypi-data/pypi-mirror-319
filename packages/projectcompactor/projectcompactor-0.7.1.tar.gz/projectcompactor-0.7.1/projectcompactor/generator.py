# projectcompactor/generator.py

import os
import argparse
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProjectCompactor:
    def __init__(
        self, 
        start_path=None, 
        output_file='project_structure.txt',
        text_extensions=None, 
        exclude_dirs=None,  # now used for names (not extensions)
        exclude_files=None, # now used for names (not extensions)
        include_dirs=None,  # new
        include_files=None, # new
        verbose=False
    ):
        """
        Initializes the ProjectCompactor.

        Args:
            start_path (str, optional): Path to start traversal. Defaults to current directory.
            output_file (str, optional): Name of the output file. Defaults to 'project_structure.txt'.
            text_extensions (set, optional): File extensions to treat as text for content extraction.
            exclude_dirs (set, optional): Set of directory NAMES to exclude.
            exclude_files (set, optional): Set of file NAMES to exclude.
            include_dirs (set, optional): Set of directory NAMES to include if using "include" mode.
            include_files (set, optional): Set of file NAMES to include if using "include" mode.
            verbose (bool, optional): Enable verbose logging. Defaults to False.
        """
        self.start_path = os.path.abspath(start_path) if start_path else os.getcwd()
        self.output_file = output_file
        # Default text file extensions for content extraction
        self.text_file_extensions = text_extensions if text_extensions else {
            '.txt', '.py', '.html', '.css', '.js', '.md', '.json',
            '.xml', '.csv', '.yaml', '.yml', '.ini', '.cfg', '.bat', '.sh',
            '.java', '.c', '.cpp', '.rb', '.go', '.ts', '.jsx', '.tsx'
        }
        self.exclude_dirs = exclude_dirs if exclude_dirs else set()
        self.exclude_files = exclude_files if exclude_files else set()
        self.include_dirs = include_dirs if include_dirs else set()
        self.include_files = include_files if include_files else set()

        self.verbose = verbose
        # Set up logging
        logging.basicConfig(
            level=logging.DEBUG if self.verbose else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def is_text_file(self, file_path):
        """
        Determines if a file is a text file by attempting to read its content.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)  # Try reading a chunk
            return True
        except (UnicodeDecodeError, PermissionError, IsADirectoryError):
            return False

    def should_skip_dir(self, dir_name):
        """
        Decide if a directory should be skipped.
        
        If 'include_dirs' is non-empty, we only keep directories in that set.
        Otherwise, we skip them. If 'include_dirs' is empty, we skip directories
        that appear in 'exclude_dirs'.
        """
        # If we have an include_dirs set, any directory not in it is skipped
        if self.include_dirs:
            return dir_name not in self.include_dirs
        # Otherwise, skip if dir_name in exclude_dirs
        return dir_name in self.exclude_dirs

    def should_skip_file(self, file_name):
        """
        Decide if a file should be skipped.
        
        If 'include_files' is non-empty, we only keep files in that set.
        Otherwise, skip if file_name in exclude_files.
        """
        # If we have an include_files set, only keep those
        if self.include_files:
            return file_name not in self.include_files
        # Otherwise, skip if file_name in exclude_files
        return file_name in self.exclude_files

    def generate_tree(self):
        """
        Generates the project tree (directory listing) as a string,
        respecting our include/exclude rules by name.
        """
        tree_lines = []
        for root, dirs, files in os.walk(self.start_path):
            # We only want to keep directories that pass should_skip_dir
            dirs[:] = [d for d in dirs if not self.should_skip_dir(d)]
            # Figure out indentation level
            level = root.replace(self.start_path, '').count(os.sep)
            indent = ' ' * 4 * level
            dir_name = os.path.basename(root) if os.path.basename(root) else root
            tree_lines.append(f"{indent}{dir_name}/")
            sub_indent = ' ' * 4 * (level + 1)

            # Filter out files that we should skip
            filtered_files = [f for f in files if not self.should_skip_file(f)]

            for file in filtered_files:
                tree_lines.append(f"{sub_indent}{file}")

        return '\n'.join(tree_lines)

    def process_file(self, file_path, relative_path):
        """
        Processes a single file to extract its content or indicate binary.
        """
        details = [f"## {relative_path}"]

        _, ext = os.path.splitext(file_path)
        # If it's a recognized text extension and passes `is_text_file`, include content
        if ext.lower() in self.text_file_extensions and self.is_text_file(file_path):
            details.append(f"### Contents of {os.path.basename(file_path)}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                details.append(contents)
            except Exception as e:
                details.append(f"[Error reading file: {e}]")
        else:
            # Otherwise, consider it binary or non-text
            details.append(f"[Binary or Non-text file: {os.path.basename(file_path)}]")
        
        details.append("\n")  # spacing
        return '\n'.join(details)

    def generate_file_details(self):
        """
        Generates detailed information for each file that isn't skipped.
        Uses multi-threading for faster reading.
        """
        details = []
        file_paths = []
        relative_paths = []

        # Collect all file paths that pass the directory & file name filters
        for root, dirs, files in os.walk(self.start_path):
            # Filter out directories
            dirs[:] = [d for d in dirs if not self.should_skip_dir(d)]
            # Filter out files
            keep_files = [f for f in files if not self.should_skip_file(f)]
            for file in keep_files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.start_path)
                file_paths.append(file_path)
                relative_paths.append(relative_path)
        
        logging.info(f"Processing {len(file_paths)} files...")

        # Use ThreadPoolExecutor for concurrent file processing
        with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as executor:
            future_to_file = {
                executor.submit(self.process_file, fp, rp): rp
                for fp, rp in zip(file_paths, relative_paths)
            }
            for future in tqdm(as_completed(future_to_file), total=len(file_paths), desc="Processing files"):
                file_detail = future.result()
                details.append(file_detail)
        
        return '\n'.join(details)

    def generate(self):
        """
        Generate the project structure and file details, then write to the output file.
        """
        logging.info("Generating project tree...")
        tree = self.generate_tree()
        logging.info("Generating file details...")
        details = self.generate_file_details()

        with open(self.output_file, 'w', encoding='utf-8') as output:
            # Write the project tree at the top
            output.write("# Project Structure\n\n")
            output.write(tree)
            output.write("\n\n# File Details\n\n")
            # Write detail info for each file
            output.write(details)
        
        logging.info(f"Project structure has been saved to '{self.output_file}'.")


def run_interactive_mode(args):
    """
    Ask user if they want to INCLUDE or EXCLUDE. 
    Then show top-level items, let them select which to keep or skip by name.
    """
    start_path = os.path.abspath(args.path)
    all_items = os.listdir(start_path)

    # Separate directories vs files for clarity
    dirs = sorted([d for d in all_items if os.path.isdir(os.path.join(start_path, d))])
    files = sorted([f for f in all_items if os.path.isfile(os.path.join(start_path, f))])

    # Ask user: Include or Exclude?
    print("\nWould you like to (I)nclude only selected items, or (E)xclude selected items?")
    mode = input("[I/E]? ").strip().lower()
    if mode not in ['i', 'e']:
        print("Invalid choice. Skipping interactive mode.\n")
        return

    print("\nDetected top-level directories and files:\n")
    index = 1
    index_map = {}  # Maps index -> (is_dir, name)
    for d in dirs:
        print(f"{index}. (Dir)  {d}")
        index_map[index] = ('dir', d)
        index += 1
    for f in files:
        print(f"{index}. (File) {f}")
        index_map[index] = ('file', f)
        index += 1

    print(
        "\nEnter the indices of items you want to select, comma-separated (e.g., 1,3,5). "
        "Press Enter to skip."
    )
    user_input = input("Your selection: ").strip()
    if not user_input:
        print("No selection made. Nothing will change.\n")
        return

    try:
        chosen_indices = [int(i.strip()) for i in user_input.split(',')]
    except ValueError:
        print("Invalid input. Skipping interactive mode.\n")
        return

    # Build sets of chosen directory/file names
    chosen_dirs = set()
    chosen_files = set()

    for i in chosen_indices:
        meta = index_map.get(i)
        if meta is None:
            continue
        kind, name = meta
        if kind == 'dir':
            chosen_dirs.add(name)
        else:
            chosen_files.add(name)

    if mode == 'i':
        # "Include" mode: We keep ONLY the chosen items. 
        # So set the "include_dirs" and "include_files" in args; everything else is implicitly excluded.
        args.include_dirs = list(chosen_dirs)
        args.include_files = list(chosen_files)
        print(f"\nYou chose INCLUDE mode.")
        print(f"Including only directories: {args.include_dirs}")
        print(f"Including only files: {args.include_files}\n")

    elif mode == 'e':
        # "Exclude" mode: We skip the chosen items, keep the rest.
        args.exclude_dirs = list(chosen_dirs)
        args.exclude_files = list(chosen_files)
        print(f"\nYou chose EXCLUDE mode.")
        print(f"Excluding directories: {args.exclude_dirs}")
        print(f"Excluding files: {args.exclude_files}\n")


def main():
    parser = argparse.ArgumentParser(
        description='ProjectCompactor: Generate a project tree and file contents.'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to the directory to analyze (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output',
        default='project_structure.txt',
        help='Output file name (default: project_structure.txt)'
    )
    parser.add_argument(
        '-e', '--extensions',
        nargs='*',
        help='Additional file extensions to treat as text files (e.g., .md .rst)'
    )
    parser.add_argument(
        '--exclude-dirs',
        nargs='*',
        default=[],
        help='Directory NAMES to exclude (e.g., venv node_modules)'
    )
    parser.add_argument(
        '--exclude-files',
        nargs='*',
        default=[],
        help='File NAMES to exclude (e.g., secrets.json .env)'
    )
    # New: let user specify includes via command line as well
    parser.add_argument(
        '--include-dirs',
        nargs='*',
        default=[],
        help='Directory NAMES to include (excludes all others if set)'
    )
    parser.add_argument(
        '--include-files',
        nargs='*',
        default=[],
        help='File NAMES to include (excludes all others if set)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Enable interactive mode (select include or exclude by name)'
    )
    args = parser.parse_args()

    # Combine default text extensions with user-specified extensions
    text_extensions = set()
    if args.extensions:
        for ext in args.extensions:
            if not ext.startswith('.'):
                ext = '.' + ext
            text_extensions.add(ext)

    # If interactive, prompt user to pick items
    if args.interactive:
        run_interactive_mode(args)

    compactor = ProjectCompactor(
        start_path=args.path,
        output_file=args.output,
        text_extensions=text_extensions if text_extensions else None,
        exclude_dirs=set(args.exclude_dirs),
        exclude_files=set(args.exclude_files),
        include_dirs=set(args.include_dirs),
        include_files=set(args.include_files),
        verbose=args.verbose
    )
    compactor.generate()


if __name__ == '__main__':
    main()
