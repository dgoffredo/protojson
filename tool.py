#!/usr/bin/env python3

import os
import shutil
from subprocess import Popen, DEVNULL
import sys
import tempfile


def print_help(out):
    help = """
usage: protojson [args forwarded to protoc ...]

example: protojson myschema.proto

Print to standard output a JSON representation of the specified
protobuf schemas and their dependencies.

All command line arguments (such as the input protobuf schema)
are forwarded to protoc, the protocol buffer compiler.  The
protocol buffer compiler is invoked as "protoc" and is expected to
be in the path, unless the environment variable PROTOC is set, in
which case the value of PROTOC will be used as the path to the protoc
executable.
"""
    print(help, file=out)


def run(args):
    if args and args[0] in ('-h', '--help', '-help'):
        print_help(sys.stdout)
        return

    if 'PROTOC' in os.environ:
        compiler_path = os.environ['PROTOC']
    else:
        compiler_path = 'protoc'

    this_dir = os.path.dirname(__file__)

    with tempfile.TemporaryDirectory() as output_dir:
        filename = 'request.json'
        command = [
            compiler_path,
            '--plugin={}'.format(os.path.join(this_dir, 'protoc-gen-json')),
            '--json_out={}'.format(output_dir), *args
        ]
        compiler = Popen(command, stdout=sys.stderr, stdin=DEVNULL)
        compiler.wait()
        if compiler.returncode:
            return compiler.returncode

        with open(os.path.join(output_dir, filename)) as file:
            shutil.copyfileobj(file, sys.stdout)

    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv[1:]))
