from setuptools import setup, find_packages
from pathlib import Path

def read_requirements(file_name):
    """
    Reads the requirements.txt file and returns a list of dependencies.
    """
    requirements_path = Path(file_name)
    if requirements_path.is_file():
        return requirements_path.read_text().splitlines()
    return []

setup(
    name="snakespawn",
    version="1.1.10",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "snakespawn=snakespawn.main:main",
        ],
    },
    python_requires=">=3.10",
    author="William L.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    description="A tool for initializing python packages.",
    license="MIT",
    install_requires=read_requirements("requirements.txt")
)
