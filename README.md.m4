changequote(`[[[', `]]]')dnl
<!-- Do not edit `README.md` directly.  Instead, modify `README.md.m4` and run
     `make` to regenerate `README.md`.
  -->

![](protojson.png)

protojson
========
Convert protobuf schemas into JSON.

Why
---
I want to make stuff based on `.proto` schemas, like object relational mappers.
`protoc` is a perfectly good parser for `.proto` files, but I want to get out
of framework and into data as soon as possible.

What
----
`protojson` is a command line tool that uses the `protoc` protocol buffer
compiler to convert a specified (set of) protocol buffer schema(s) into a JSON
representation, which is readily consumed by other tools.

How
---
`protoc` has a "we'll call you" policy, which makes sense.  `protoc` handles
command line options, parsing, and dependency resolution.  Then it invokes a
"plugin," which is just a program, with a protobuf representation of the
compiled schemas, and the plugin prints a protobuf representation of the
resulting compiled artifacts (e.g. C++ source files) to standard output.

This repository contains such a plugin, `protoc-gen-json`, which produces a
single file, `request.json`, containing the JSON-ified input passed to
`protoc-gen-json` from `protoc`, but additionally with source location
information associated with the relevant AST nodes (this is helpful so that you
can see source code comments within the schema entities to which they refer).

More convenient, though, is the command line driver, `tool.py`, which invokes
`protoc` using the plugin, and prints the resulting JSON to standard output.

This repository is itself a python package, so the directory can be invoked as
if it were a python script.

```console
$ cat protojson/examples/hello.proto
include([[[example/hello.proto]]])dnl

$ python3 protojson protojson/example/hello.proto | jq '.'
esyscmd([[[cd ..; python3 protojson protojson/example/hello.proto | jq '.']]])dnl
```
