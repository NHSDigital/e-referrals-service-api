#!/usr/bin/env python3
'''
update_version.py

Calculates the current version of the repository, then uses this to update the version stored in the project's packaging files
'''
import json
import toml
from calculate_version import calculate_version


def update_poetry_version(version):
    print('Updating poetry version....')
    with open("pyproject.toml", "r") as inFile:
        poetry_data = toml.load(inFile)
    poetry_data["tool"]["poetry"]["version"] = version

    with open("pyproject.toml", "w") as out:
        toml.dump(poetry_data, out)


def update_npm_version(version):
    print('Updating npm version....')
    with open("package.json", "r") as inFile:
        npm_data = json.load(inFile)
    npm_data["version"] = version

    with open("package.json", "w") as outFile:
        json.dump(npm_data, outFile, indent=2)


if __name__ == "__main__":
    version = str(calculate_version())

    print('Updating packaging version to: ' + version)

    update_npm_version(version)
    update_poetry_version(version)

    print('Packing version updated')
