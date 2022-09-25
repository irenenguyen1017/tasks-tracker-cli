from setuptools import find_packages, setup

setup(
    name="tasks_tracker",
    include_package_data=True,
    version="0.1.0",
    author="Irene Nguyen",
    author_email="irenenguyen1017@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={"console_scripts": ["tasks-tracker = tasks_tracker:main"]},
    url="http://pypi.python.org/pypi/tasks-tracker/",
    license="LICENSE.txt",
    description="A simple CLI application that can manage and track multiple tasks.",
    install_requires=[
        "rich >= 12.5.1",
        "nanoid >= 2.0.0",
        "typer >= 0.6.1",
        "pytest",
    ],
)
