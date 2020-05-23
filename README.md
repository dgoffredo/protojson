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
syntax = "proto3";

enum Greeting {
    NONE = 0;
    MR = 1;
    MRS = 2;
    MISS = 3;  // we're missing "MS"
}

// Are these leading_detached_comments?
// What determines how they're listed?

// Maybe like this?

// Hello blah blah blah
message Hello {
    Greeting greeting = 1;  // on the side
    // above
    string name = 2;
}

service GreeterService {
    // Here I document the Greet method.
    rpc Greet (Hello) returns (Hello);
}  // What is this considered?
// Is this trailing?

// What about this?

// And this?

$ python3 protojson protojson/example/hello.proto | jq '.'
{
  "fileToGenerate": [
    "example/hello.proto"
  ],
  "compilerVersion": {
    "major": 3,
    "minor": 11,
    "patch": 4,
    "suffix": ""
  },
  "protoFile": [
    {
      "name": "example/hello.proto",
      "messageType": [
        {
          "name": "Hello",
          "field": [
            {
              "name": "greeting",
              "number": 1,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_ENUM",
              "typeName": ".Greeting",
              "jsonName": "greeting",
              "location": {
                "span": [
                  16,
                  4,
                  26
                ],
                "trailingComments": " on the side\n"
              }
            },
            {
              "name": "name",
              "number": 2,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_STRING",
              "jsonName": "name",
              "location": {
                "span": [
                  18,
                  4,
                  20
                ],
                "leadingComments": " above\n"
              }
            }
          ],
          "location": {
            "span": [
              15,
              0,
              19,
              1
            ],
            "leadingComments": " Hello blah blah blah\n",
            "leadingDetachedComments": [
              " Are these leading_detached_comments?\n What determines how they're listed?\n",
              " Maybe like this?\n"
            ]
          }
        }
      ],
      "enumType": [
        {
          "name": "Greeting",
          "value": [
            {
              "name": "NONE",
              "number": 0,
              "location": {
                "span": [
                  3,
                  4,
                  13
                ]
              }
            },
            {
              "name": "MR",
              "number": 1,
              "location": {
                "span": [
                  4,
                  4,
                  11
                ]
              }
            },
            {
              "name": "MRS",
              "number": 2,
              "location": {
                "span": [
                  5,
                  4,
                  12
                ]
              }
            },
            {
              "name": "MISS",
              "number": 3,
              "location": {
                "span": [
                  6,
                  4,
                  13
                ],
                "trailingComments": " we're missing \"MS\"\n"
              }
            }
          ],
          "location": {
            "span": [
              2,
              0,
              7,
              1
            ]
          }
        }
      ],
      "service": [
        {
          "name": "GreeterService",
          "method": [
            {
              "name": "Greet",
              "inputType": ".Hello",
              "outputType": ".Hello",
              "location": {
                "span": [
                  23,
                  4,
                  38
                ],
                "leadingComments": " Here I document the Greet method.\n"
              }
            }
          ],
          "location": {
            "span": [
              21,
              0,
              24,
              1
            ]
          }
        }
      ],
      "syntax": "proto3",
      "location": {
        "span": [
          0,
          0,
          24,
          1
        ]
      }
    }
  ]
}
```
