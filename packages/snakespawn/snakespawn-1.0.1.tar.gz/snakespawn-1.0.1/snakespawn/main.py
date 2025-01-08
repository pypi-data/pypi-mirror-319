from dataclasses import dataclass
import sys
from cli_veripy import CLIArguments, CLIError, ExistingPath
from pathlib import Path
from licenses import get_license
import shutil
import string

def snake_caseify(name:str) -> str:
    ret = ""
    name = name[0].lower() + name[1::]
    prev_char = ""
    for c in name:
        if c in " \n\t":
            prev_char = ' '
            continue
        new_c = c
        if c.isupper():
            if prev_char == " ":
                new_c = f"_{new_c.lower()}"
            else:
                new_c = new_c.lower()
        ret += new_c
        prev_char = c

    return ret

def handle_cli_error(e:CLIError):
    sys.stderr.write('\n' + e.message + '\n')
    sys.stderr.write("\n" + e.cli_arguments.usage_string + '\n\n')
    sys.stderr.flush()
    exit(1)

def title_caseify(name:str) -> str:
    ret = ""
    name = name[0].upper() + name[1::]
    prev_char = ""

    for c in name:
        new_c = c
        if new_c in " _":
            prev_char = new_c
            continue
        if prev_char in " _":
            new_c = new_c.upper()
        ret += new_c
        prev_char = c

    return ret

def ListStrFactory(valid_chars:str = string.ascii_letters + '_ ', delimiter:str = ','):
    valid_chars += delimiter
    class ListStr(list):
        def __init__(self, value:str):
            for c in value:
                if c not in valid_chars:
                    raise TypeError(f"List argument must contain valid characters '{valid_chars}'.\nInvalid character found '{c}'.", c)
            super().__init__(value.split(delimiter))
    return ListStr

class VersionStr(str):
    def __new__(cls, value:str):
        valid_chars = string.digits + string.ascii_letters + ' ._-~()+'
        for c in value:
            if c not in valid_chars:
                raise TypeError(f"Version argument must contain valid version '{valid_chars}'.\nInvalid character found '{c}'.", c)
        
        # Remove words from version number
        validateable_value = value
        for c in ' ._-~()+':
            validateable_value = validateable_value.replace(c, "")
        validateable_value = validateable_value.lower()
        for word in [
            "alpha", 'a',
            "development", "dev", "devel", "d",
            'b', 'beta',
            'release','rel','r',
            'restricted','res','test', 't', 'first', 'f', 'unknown','u'
        ]:
            validateable_value = validateable_value.replace(word, "")

        ver_parts = validateable_value.split(".")
        
        for ver_p in ver_parts:
            if not ver_p.isnumeric() or ver_p == "":
                raise TypeError(f"Version argument '{value}' is in an invalid format.", value)

        return super().__new__(cls, value)

def main():
    args:CLIArguments = CLIArguments(
        valid_pargs=[Path, str],
        pargs_names=["package-directory", "package-name"],
        valid_flags={
            "no-requirements", "no-deps", "git-ignore", "tests",
            "testing", "no-readme", "utils-folder", "core-folder",
            "examples", "docs", "documentation", "manifest", "force-yes",
            "force-y", "create-project-directory"
        },
        valid_kwargs={
            "version":VersionStr, "build-tool":str, "python-version":str,
            "author":str, "license":str, "license-year":int,
            "license-path":ExistingPath, "sub-modules":ListStrFactory()
        },
        required_kwargs=["author"],
        exit_on_invalid=True,
        description="A command line tool for initializing new python projects."
    )

    # TODO make it able tp take a tuple (type, function) where the function returns a boolean and acts as a verification filter

    args["version"] = args["version"] if args["version"] else "0.0.0-ALPHA1"
    args["build-tool"] = args["build-tool"] if args["build-tool"] else "setuptools"
    args["python-version"] = args["python-version"] if args["python-version"] else ">=3.10"
    force_yes = args["force-yes"] or args["force-y"]

    if not args["package-directory"].exists():
        if not force_yes and not args["create-project-directory"]:
            print(f"\nThe specified package-directory '{args['package-directory']}' does not exist.  Would you like to create it?\n\n * Tip: You can use -create-project-directory or -force-y to skip this prompt in the future.\n")
        continue_prompt = force_yes or args["create-project-directory"] or input(f"y/n(default is no):").lower() in {"yes", 'y', 'true'}
        if continue_prompt:
            args["package-directory"].mkdir()
        else:
            print("\nPython project initialization canceled.\n\nexiting...")
            exit(0)

    # Package
    
    package_path = args["package-directory"] / snake_caseify(args["package-name"])
    package_path.mkdir()
    (mod_init_path:=package_path/"__init__.py").touch()
    if args["core-folder"]:
        core_path = package_path / "core"
        core_path.mkdir()
        (core_path_init:=core_path/"__init__.py").touch()
        with open(mod_init_path, "a") as fp:
            fp.write(f'from {snake_caseify(args["package-name"])}.core import *\n')
        if args["sub-modules"] is not None:
            with open(core_path_init, "a") as fp:
                for mod in args["sub-modules"]:
                    if mod == "":
                        continue
                    mod = snake_caseify(mod)
                    (core_path/f"{mod}.py").touch()
                    fp.write(f'from {snake_caseify(args["package-name"])}.core.{mod} import *\n')


    if args["utils-folder"]:
        utils_path = package_path / "utils"
        utils_path.mkdir()
        (utils_path/"__init__.py").touch()

    # Examples
    if args["examples"]:
        (args["package-directory"]/"examples").mkdir()

    # Tests
    if args["tests"] or args["testing"]:
        tests_path = args["package-directory"] / "tests"
        tests_path.mkdir()
        
        if args["core-folder"]:
            core_path = tests_path / "core"
            core_path.mkdir()
            core_path.touch(py_file:=f'test_{snake_caseify(args["package-name"])}_core.py')
            with open(core_path / py_file, 'w') as fp:
                fp.write(
f"""from {snake_caseify(args["package-name"])}.core import *
import unittest

class Test{title_caseify(args['package-name'])}Core:
    ...
"""
                )
        else:
            tests_path.touch(py_file:=f'test_{snake_caseify(args["package-name"])}.py')
            with open(tests_path / py_file, 'w') as fp:
                fp.write(
f"""from {snake_caseify(args["package-name"])} import *
import unittest

class Test{title_caseify(args['package-name'])}(unittest.TestCase):
    ...
"""
                )

        if args["utils-folder"]:
            utils_path = tests_path / "utils"
            utils_path.mkdir()
            utils_path.touch(py_file:=f'test_{snake_caseify(args["package-name"])}_utils.py')
            with open(utils_path / py_file, 'w') as fp:
                fp.write(
f"""from {snake_caseify(args["package-name"])}.utils import *
import unittest

class Test{title_caseify(args['package-name'])}Utils(unittest.TestCase):
    ...
"""
                )

    # Docs
    
    if args["docs"] or args["documentation"]:
        docs_path = args["package-directory"] / "docs"
        docs_path.mkdir()
        (docs_path/"index.md").touch()
        with open(docs_path / "index.md", 'w') as fp:
            fp.write(f"# {args["package-name"]} Documentation")

    # Readme

    if not args["no-readme"]:
        (args["package-directory"]/"README.md").touch()
        with open(args["package-directory"] / "README.md", 'w') as fp:
            fp.write(f"# {args["package-name"]}")

    # Requirements / Dependencies
    if not (args["no-requirements"] or args["no-deps"]):
        (args["package-directory"]/"requirements.txt").touch()

    # Manifest
    if args["manifest"]:
        (args["package-directory"]/"MANIFEST.in").touch()

    # License
    if args["license"]:
        if args["license-path"]:
            handle_cli_error(CLIError(args, "Cannot specify both a --license and --license-path.", args["license"], args["license-path"]))
        (args["package-directory"]/"LICENSE").touch()
        with open(args["package-directory"] / "LICENSE", 'w') as fp:
            try:
                fp.write(get_license(args["license"], args))
            except CLIError as e:
                handle_cli_error(e)
    
    if args["license-path"]:
        shutil.copy(args["license-path"], args["package-directory"] / "LICENSE")
        args["license"] = args["license"] if args["license"] else args["license-path"].name.split('.',1)[0]
        

    # Setuptools
    if args["build-tool"] == "setuptools":
        (args["package-directory"]/"setup.py").touch()
        with open(args["package-directory"] / "setup.py", 'w') as fp:
            fp.write(
f"""
from setuptools import setup, find_packages

description = {'""' if args["no-readme"] else '(fp:=open("README.md")).read()'}
fp.close()

setup(
    name="{snake_caseify(args["package-name"])}",
    version="{args["version"]}",
    packages=find_packages(),
    python_requires="{args["python-version"]}",
    author="{args["author"]}",
    description=description,
    {f'license=\'{args["license"]}\',' if args["license"] else ''}
)
"""
            )
    print(f"\nFinished:\n    '{args['package-name']}' package created at '{args['package-directory']}'.")
    
    
if __name__ == "__main__":
    main()