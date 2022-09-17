from setuptools import find_packages, setup

setup(
    name="tasks_tracker",
    include_package_data=True,
    version="0.1.0",
    author="Irene Nguyen",
    author_email="irenenguyen1017@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["tasks-tracker = tasks_tracker:main"]},
    url="http://pypi.python.org/pypi/tasks-tracker/",
    license="LICENSE.txt",
    description="A terminal CLI that can manage tasks.",
    install_requires=[
        "pytest",
    ],
)