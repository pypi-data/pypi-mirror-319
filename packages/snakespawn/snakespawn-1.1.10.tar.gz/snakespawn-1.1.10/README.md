# snakespawn

`snakespawn` is a command line tool for initializing python packages.  Run `snakespawn` without any arguments to for usage details.

```
usage: snakespawn.exe  (package-directory(Path))  (package-name(str))

---------------------------------------------------------

A command line tool for initializing new python projects.

---------------------------------------------------------

Flags:

    -docs                      -force-y                   -examples                  -no-requirements

    -utils-folder              -git-ignore                -core-folder               -create-project-directory

    -force-yes                 -no-deps                   -no-readme                 -tests

    -testing                   -documentation             -manifest


Keyword Arguments:

    --author(Required str)        --version(VersionStr)         --build-tool(str)

    --python-version(str)         --license(str)                --license-year(int)

    --license-path(ExistingPath)  --sub-modules(ListStr)
```

This module using a command line argument verification package I wrote called [cli_veripy](https://pypi.org/project/cli-veripy/).