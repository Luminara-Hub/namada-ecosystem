import os
import json
import shutil

def remove_existing_markdown_files(base_dir, subdirs):
    """Remove all existing markdown files in the 'MD' directories."""
    for subdir in subdirs:
        md_dir = os.path.join(base_dir, subdir, "MD")
        if os.path.exists(md_dir):
            shutil.rmtree(md_dir)
        os.makedirs(md_dir, exist_ok=True)

def generate_markdown_files(files_keys_exclude):
    """
    Generate markdown files from the Json input files.
    Takes a list of files and their keys to exclude from the generated markdown.
    """
    subdirs = ["mainnet", "testnet"]
    base_dir = "user-and-dev-tools"

    # Remove any existing markdown files
    remove_existing_markdown_files(base_dir, subdirs)

    for subdir in subdirs:
        json_dir = os.path.join(base_dir, subdir)
        md_dir = os.path.join(json_dir, "MD")
        os.makedirs(md_dir, exist_ok=True)

        for file_name in os.listdir(json_dir):
            if not file_name.endswith(".json"):
                continue

            json_path = os.path.join(json_dir, file_name)

            # If a file is passed with exclude equals "*", skip it entirely
            if file_name in files_keys_exclude and "*" in files_keys_exclude[file_name]:
                print(f"Skipping entire file: {file_name}")
                continue

            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding {json_path}: {e}")
                continue

            # Generate markdown content
            markdown_content = f"# {file_name.replace('.json', '').title()}\n\n"
            excluded_keys = files_keys_exclude.get(file_name, [])

            # Iterate over each object in JSON array
            if isinstance(data, list):
                for idx, obj in enumerate(data, start=1):
                    #markdown_content += f"## Entry {idx}\n"
                    if idx is not 1:
                      markdown_content += f"---\n"
                    for key, value in obj.items():
                        if key in excluded_keys:
                            continue
                        markdown_content += f"- **{key}**: {value if value else 'N/A'}\n"
                    markdown_content += "\n"

            # Write markdown file
            md_file_path = os.path.join(md_dir, file_name.replace(".json", ".md"))
            try:
                with open(md_file_path, "w") as md_file:
                    md_file.write(markdown_content)
                print(f"Generated {md_file_path}")
            except IOError as e:
                print(f"Error writing to {md_file_path}: {e}")

if __name__ == "__main__":
    # Load the list of files and keys to exclude from the markdown
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_file_path = os.path.join(script_dir, "files_keys_exclude.json")

    try:
        with open(exclude_file_path, "r") as f:
            files_keys_exclude = json.load(f)
    except FileNotFoundError:
        print(f"Error: {exclude_file_path} not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding {exclude_file_path}: {e}")
        exit(1)

    generate_markdown_files(files_keys_exclude)