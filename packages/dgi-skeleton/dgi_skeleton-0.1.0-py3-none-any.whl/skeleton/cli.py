import os
import shutil
import argparse

TEMPLATE_DIR = os.path.dirname(__file__)

def create_project(name: str, destination: str = "."):
    project_dir = os.path.join(destination, name)
    if os.path.exists(project_dir):
        print(f"Error: project '{name}' already exists!")
        return

    os.makedirs(project_dir)
    template_path = TEMPLATE_DIR + os.sep + 'project_name'
    output_path = os.path.join(project_dir)
    copy_directory_structure(template_path, output_path)

def create_app(name: str, destination: str = "."):
    app_dir = os.path.join(destination, name)
    if os.path.exists(app_dir):
        print(f"Error: app '{name}' already exists!")
        return

    os.makedirs(app_dir)
    template_path = TEMPLATE_DIR + os.sep + 'app_name'
    output_path = os.path.join(app_dir)
    copy_directory_structure(template_path, output_path)

def copy_directory_structure(src, dst):
    for dirpath, dirnames, filenames in os.walk(src):
        dest_dir = dirpath.replace(src, dst, 1)
        os.makedirs(dest_dir, exist_ok=True)

        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            dst_file = os.path.join(dest_dir, filename)
            shutil.copy2(src_file, dst_file)

def create_project_command(args):
    create_project(args.project_name, args.destination)

def create_app_command(args):
    create_app(args.app_name, args.destination)

def main():
    parser = argparse.ArgumentParser(description='Generate a Django skeleton.')

    subparsers = parser.add_subparsers(dest="command")

    create_project_parser = subparsers.add_parser('startproject', help='Create a Django skeleton project.')
    create_project_parser.add_argument("project_name", help="The name of the new Django project.")
    create_project_parser.add_argument('--destination', type=str, default='.', help='The destination')
    create_project_parser.set_defaults(func=create_project_command)

    create_app_parser = subparsers.add_parser('startapp', help='Create a Django app.')
    create_app_parser.add_argument('app_name', help='The name of the new Django app.')
    create_app_parser.add_argument('--destination', type=str, default='.', help='The destination')
    create_app_parser.set_defaults(func=create_app_command)
    
    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
