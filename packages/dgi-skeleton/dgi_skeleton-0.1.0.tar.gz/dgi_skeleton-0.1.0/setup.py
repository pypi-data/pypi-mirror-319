from setuptools import setup, find_packages, find_namespace_packages

setup(
    name="dgi-skeleton",
    version="0.1.0",
    packages=find_namespace_packages(where='src'),
    install_requires=[""],
    package_dir={
        '': 'src',
    },
    include_package_data=True,
    entry_points={
        "console_scripts": {
            "dgi-skeleton=skeleton.cli:main",
        },
    },
    description="A CLI tool to generate Django project skeletons.",
    author="PT Dayagagas Internasional",
    license="MIT",
)
