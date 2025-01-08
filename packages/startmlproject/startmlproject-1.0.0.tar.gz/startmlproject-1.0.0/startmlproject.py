import os
import sys

def create_ml_project(project_name, base_path="."):
    # Define the folder structure
    structure = {
        f"{project_name}": {
            "data": ["raw", "cleaned", "processed", "transformed"],
            "notebooks": ["01_data_exploration.ipynb"],
            "scripts": [],
            "artifacts": ["scalers", "encoders", "tokenizers", "logs", "evaluation"],
        },
        f"{project_name}/requirements.txt": None,
        f"{project_name}/README.md": None,
    }

    # Create the project folder and subfolders/files
    for key, value in structure.items():
        if isinstance(value, dict):  # Main project folder with subdirectories
            for folder, subfolders in value.items():
                folder_path = os.path.join(base_path, project_name, folder)
                os.makedirs(folder_path, exist_ok=True)

                # Create subfolders or default files within this folder
                for sub in subfolders:
                    if "." in sub:  # It's a file
                        file_path = os.path.join(folder_path, sub)
                        with open(file_path, "w") as f:
                            if sub.endswith(".ipynb"):
                                f.write("{\n  \"cells\": [], \"metadata\": {}, \"nbformat\": 4, \"nbformat_minor\": 4\n}")
                    else:  # It's a directory
                        subfolder_path = os.path.join(folder_path, sub)
                        os.makedirs(subfolder_path, exist_ok=True)
        else:  # Root-level files
            file_path = os.path.join(base_path, key)
            with open(file_path, "w") as f:
                if key.endswith("README.md"):
                    f.write(f"# {project_name}\n\nGenerated ML project structure.\n")
                elif key.endswith("requirements.txt"):
                    f.write("# Add your dependencies here\n")

    print(f"Machine Learning project '{project_name}' created at {base_path}/{project_name}.")

def main():
    if len(sys.argv) < 2:
        print("Usage: startmlproject <project_name> [--path <base_path>]")
        sys.exit(1)
    
    project_name = sys.argv[1]
    base_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--path" else "."
    create_ml_project(project_name, base_path=base_path)

if __name__ == "__main__":
    main()
