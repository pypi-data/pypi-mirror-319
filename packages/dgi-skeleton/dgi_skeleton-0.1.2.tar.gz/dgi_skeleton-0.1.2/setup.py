from setuptools import setup, find_packages, find_namespace_packages
import os

current_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dgi-skeleton",
    version="0.1.2",
    packages=find_namespace_packages(where='src'),
    install_requires=[""],
    package_dir={
        '': 'src',
    },
    package_data={
        '': [
            'project_name/.env',
            'project_name/.gitignore',
            'project_name/requirements.txt',
            'project_name/Dockerfile',
        ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": {
            "dgi-skeleton=skeleton.cli:main",
        },
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A CLI tool to generate Django project skeletons.",
    author="PT Dayagagas Internasional",
    license="MIT",
)
