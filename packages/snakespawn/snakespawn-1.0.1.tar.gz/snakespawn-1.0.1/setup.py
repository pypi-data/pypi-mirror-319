from setuptools import setup, find_packages

setup(
    name="snakespawn",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "snakespawn=snakespawn.main:main",
        ],
    },
    python_requires=">=3.10",
    author="William L.",
    long_description=open("README.md").read(),
    description="A tool for initializing python packages.",
    license="MIT",
)
