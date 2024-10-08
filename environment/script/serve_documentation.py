#!/usr/bin/env python
import glob
import os.path
from pathlib import Path
import sys

import docopt
from livereload import Server, shell

# https://pypi.org/project/livereload/

# TODO
# - Extend file list to include all files used for building documentation


def serve_documentation(
    source_directory_path: Path, build_directory_path: Path, port: int
) -> None:

    documentation_source_prefix = f"{source_directory_path}/documentation"
    documentation_build_prefix = f"{build_directory_path}/documentation/_build/html"

    server = Server()

    pathnames_to_watch = glob.glob(
        f"{documentation_source_prefix}/**/*.md", recursive=True
    ) + [
        f"{documentation_source_prefix}/_config.yml.in",
        f"{documentation_source_prefix}/_toc.yml",
        f"{documentation_source_prefix}/*.md",
        f"{documentation_source_prefix}/CMakeLists.txt",
        f"{documentation_source_prefix}/references.bib",
    ]

    for pathname in pathnames_to_watch:
        server.watch(
            pathname,
            shell(f"cmake --build {build_directory_path} --target documentation.html"),
        )
    server.serve(port=port, root=documentation_build_prefix)


def main() -> None:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Serve documentation and refresh when source files change

Usage:
    {command} [--port=<port>] <source_directory> <build_directory>

Arguments:
    source_directory  Pathname of project's source directory
    build_directory   Pathname of project's build directory

Options:
    -h --help         Show this screen and exit
    --version         Show version and exit
    --port=<port>     Serve on this port [default: 5500]
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments)
    source_directory_path = Path(arguments["<source_directory>"])  # type: ignore
    build_directory_path = Path(arguments["<build_directory>"])  # type: ignore
    port = int(arguments["--port"])  # type: ignore

    serve_documentation(source_directory_path, build_directory_path, port)


if __name__ == "__main__":
    main()
