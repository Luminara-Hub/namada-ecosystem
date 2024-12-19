import os
import json
import shutil

def remove_existing_markdown_files(base_dir, gitbook_dir, subdirs):
    """Remove all existing markdown files in the gitbook directories."""
    for subdir in subdirs:
        md_dir = os.path.join(base_dir, gitbook_dir, subdir)
        if os.path.exists(md_dir):
            shutil.rmtree(md_dir)
        os.makedirs(md_dir, exist_ok=True)

def generate_summary_file(base_dir, gitbook_dir, subdirs, resources_links):
    """Generate the SUMMARY.md file."""
    summary_path = os.path.join(base_dir, gitbook_dir, "SUMMARY.md")
    summary_content = "# Summary\n\n## About\n\n* [Home](./README.md)\n* [FAQ](./faq.md)\n\n## Resources\n"

    for subdir, links in resources_links.items():
        summary_content += f"* [{subdir.title()} Resources](./{subdir}/README.md)\n"
        for title, path in links:
            summary_content += f"    * [{title}](./{path})\n"

    try:
        with open(summary_path, "w") as summary_file:
            summary_file.write(summary_content)
        print(f"Generated {summary_path}")
    except IOError as e:
        print(f"Error writing to {summary_path}: {e}")

def generate_markdown_files(files_keys_exclude):
    """
    Generate markdown files from the Json input files.
    Takes a list of files and their keys to exclude from the generated markdown.
    """
    subdirs = ["mainnet", "testnet"]
    base_dir = "user-and-dev-tools"
    gitbook_dir = "gitbook"
    base_url = "https://luminara-namada.gitbook.io/namada-ecosystem/resources"

    # Remove any existing markdown files
    remove_existing_markdown_files(base_dir, gitbook_dir, subdirs)

    resources_links = {subdir: [] for subdir in subdirs}

    for subdir in subdirs:
        json_dir = os.path.join(base_dir, subdir)
        md_dir = os.path.join(base_dir, gitbook_dir, subdir)
        os.makedirs(md_dir, exist_ok=True)

        readme_content = f"# {subdir.title()} Resources\n\n"

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
                    if idx != 1:
                        markdown_content += f"---\n"
                    for key, value in obj.items():
                        if key in excluded_keys:
                            continue
                        markdown_content += f"- **{key}**: {value if value else 'N/A'}\n"
                    markdown_content += "\n"

            # Write markdown file
            md_file_name = file_name.replace(".json", ".md")
            md_file_path = os.path.join(md_dir, md_file_name)
            try:
                with open(md_file_path, "w") as md_file:
                    md_file.write(markdown_content)
                print(f"Generated {md_file_path}")

                # Add link to README content
                link = f"{base_url}/{subdir}/{md_file_name.replace('.md', '')}"
                readme_content += f"- [{md_file_name.replace('.md', '').title()}]({link})\n"

                # Add link to resources for SUMMARY.md
                resources_links[subdir].append((md_file_name.replace('.md', '').title(), f"{subdir}/{md_file_name}"))
            except IOError as e:
                print(f"Error writing to {md_file_path}: {e}")

        # Write README.md file
        readme_file_path = os.path.join(md_dir, "README.md")
        try:
            with open(readme_file_path, "w") as readme_file:
                readme_file.write(readme_content)
            print(f"Generated {readme_file_path}")
        except IOError as e:
            print(f"Error writing to {readme_file_path}: {e}")

    # Generate the SUMMARY.md file
    generate_summary_file(base_dir, gitbook_dir, subdirs, resources_links)

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
