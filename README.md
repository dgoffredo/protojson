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
syntax = "proto3";

package sassafras.sassafras;

option go_package = "blah/blah/blah;blah";

import "google/protobuf/timestamp.proto";

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
    repeated Greeting greeting = 1;  // on the side
    // above
    string name = 2;

    // I don't know like whatever lol.
    google.protobuf.Timestamp when = 3;

    fixed64 snake_case = 4;
    fixed64 camelCase = 5;
    fixed64 SHOUTING_CASE = 6;
    fixed64 PascalCase = 7;
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
    "protojson/example/hello.proto"
  ],
  "compilerVersion": {
    "major": 3,
    "minor": 6,
    "patch": 1,
    "suffix": ""
  },
  "protoFile": [
    {
      "name": "google/protobuf/timestamp.proto",
      "package": "google.protobuf",
      "messageType": [
        {
          "name": "Timestamp",
          "field": [
            {
              "name": "seconds",
              "number": 1,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_INT64",
              "jsonName": "seconds",
              "location": {
                "span": [
                  127,
                  2,
                  20
                ],
                "leadingComments": " Represents seconds of UTC time since Unix epoch\n 1970-01-01T00:00:00Z. Must be from 0001-01-01T00:00:00Z to\n 9999-12-31T23:59:59Z inclusive.\n"
              }
            },
            {
              "name": "nanos",
              "number": 2,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_INT32",
              "jsonName": "nanos",
              "location": {
                "span": [
                  133,
                  2,
                  18
                ],
                "leadingComments": " Non-negative fractions of a second at nanosecond resolution. Negative\n second values with fractions must still have non-negative nanos values\n that count forward in time. Must be from 0 to 999,999,999\n inclusive.\n"
              }
            }
          ],
          "location": {
            "span": [
              122,
              0,
              134,
              1
            ],
            "leadingComments": " A Timestamp represents a point in time independent of any time zone\n or calendar, represented as seconds and fractions of seconds at\n nanosecond resolution in UTC Epoch time. It is encoded using the\n Proleptic Gregorian Calendar which extends the Gregorian calendar\n backwards to year one. It is encoded assuming all minutes are 60\n seconds long, i.e. leap seconds are \"smeared\" so that no leap second\n table is needed for interpretation. Range is from\n 0001-01-01T00:00:00Z to 9999-12-31T23:59:59.999999999Z.\n By restricting to that range, we ensure that we can convert to\n and from  RFC 3339 date strings.\n See [https://www.ietf.org/rfc/rfc3339.txt](https://www.ietf.org/rfc/rfc3339.txt).\n\n # Examples\n\n Example 1: Compute Timestamp from POSIX `time()`.\n\n     Timestamp timestamp;\n     timestamp.set_seconds(time(NULL));\n     timestamp.set_nanos(0);\n\n Example 2: Compute Timestamp from POSIX `gettimeofday()`.\n\n     struct timeval tv;\n     gettimeofday(&tv, NULL);\n\n     Timestamp timestamp;\n     timestamp.set_seconds(tv.tv_sec);\n     timestamp.set_nanos(tv.tv_usec * 1000);\n\n Example 3: Compute Timestamp from Win32 `GetSystemTimeAsFileTime()`.\n\n     FILETIME ft;\n     GetSystemTimeAsFileTime(&ft);\n     UINT64 ticks = (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime;\n\n     // A Windows tick is 100 nanoseconds. Windows epoch 1601-01-01T00:00:00Z\n     // is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z.\n     Timestamp timestamp;\n     timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL));\n     timestamp.set_nanos((INT32) ((ticks % 10000000) * 100));\n\n Example 4: Compute Timestamp from Java `System.currentTimeMillis()`.\n\n     long millis = System.currentTimeMillis();\n\n     Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000)\n         .setNanos((int) ((millis % 1000) * 1000000)).build();\n\n\n Example 5: Compute Timestamp from current time in Python.\n\n     timestamp = Timestamp()\n     timestamp.GetCurrentTime()\n\n # JSON Mapping\n\n In JSON format, the Timestamp type is encoded as a string in the\n [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) format. That is, the\n format is \"{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z\"\n where {year} is always expressed using four digits while {month}, {day},\n {hour}, {min}, and {sec} are zero-padded to two digits each. The fractional\n seconds, which can go up to 9 digits (i.e. up to 1 nanosecond resolution),\n are optional. The \"Z\" suffix indicates the timezone (\"UTC\"); the timezone\n is required. A proto3 JSON serializer should always use UTC (as indicated by\n \"Z\") when printing the Timestamp type and a proto3 JSON parser should be\n able to accept both UTC and other timezones (as indicated by an offset).\n\n For example, \"2017-01-15T01:30:15.01Z\" encodes 15.01 seconds past\n 01:30 UTC on January 15, 2017.\n\n In JavaScript, one can convert a Date object to this format using the\n standard [toISOString()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString]\n method. In Python, a standard `datetime.datetime` object can be converted\n to this format using [`strftime`](https://docs.python.org/2/library/time.html#time.strftime)\n with the time format spec '%Y-%m-%dT%H:%M:%S.%fZ'. Likewise, in Java, one\n can use the Joda Time's [`ISODateTimeFormat.dateTime()`](\n http://www.joda.org/joda-time/apidocs/org/joda/time/format/ISODateTimeFormat.html#dateTime--\n ) to obtain a formatter capable of generating timestamps in this format.\n\n\n"
          }
        }
      ],
      "options": {
        "javaPackage": "com.google.protobuf",
        "javaOuterClassname": "TimestampProto",
        "javaMultipleFiles": true,
        "goPackage": "github.com/golang/protobuf/ptypes/timestamp",
        "ccEnableArenas": true,
        "objcClassPrefix": "GPB",
        "csharpNamespace": "Google.Protobuf.WellKnownTypes",
        "location": {
          "span": [
            40,
            0,
            33
          ]
        }
      },
      "syntax": "proto3",
      "location": {
        "span": [
          30,
          0,
          134,
          1
        ]
      }
    },
    {
      "name": "protojson/example/hello.proto",
      "package": "sassafras.sassafras",
      "dependency": [
        "google/protobuf/timestamp.proto"
      ],
      "messageType": [
        {
          "name": "Hello",
          "field": [
            {
              "name": "greeting",
              "number": 1,
              "label": "LABEL_REPEATED",
              "type": "TYPE_ENUM",
              "typeName": ".sassafras.sassafras.Greeting",
              "jsonName": "greeting",
              "location": {
                "span": [
                  22,
                  4,
                  35
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
                  24,
                  4,
                  20
                ],
                "leadingComments": " above\n"
              }
            },
            {
              "name": "when",
              "number": 3,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_MESSAGE",
              "typeName": ".google.protobuf.Timestamp",
              "jsonName": "when",
              "location": {
                "span": [
                  27,
                  4,
                  39
                ],
                "leadingComments": " I don't know like whatever lol.\n"
              }
            },
            {
              "name": "snake_case",
              "number": 4,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_FIXED64",
              "jsonName": "snakeCase",
              "location": {
                "span": [
                  29,
                  4,
                  27
                ]
              }
            },
            {
              "name": "camelCase",
              "number": 5,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_FIXED64",
              "jsonName": "camelCase",
              "location": {
                "span": [
                  30,
                  4,
                  26
                ]
              }
            },
            {
              "name": "SHOUTING_CASE",
              "number": 6,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_FIXED64",
              "jsonName": "SHOUTINGCASE",
              "location": {
                "span": [
                  31,
                  4,
                  30
                ]
              }
            },
            {
              "name": "PascalCase",
              "number": 7,
              "label": "LABEL_OPTIONAL",
              "type": "TYPE_FIXED64",
              "jsonName": "PascalCase",
              "location": {
                "span": [
                  32,
                  4,
                  27
                ]
              }
            }
          ],
          "location": {
            "span": [
              21,
              0,
              33,
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
                  9,
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
                  10,
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
                  11,
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
                  12,
                  4,
                  13
                ],
                "trailingComments": " we're missing \"MS\"\n"
              }
            }
          ],
          "location": {
            "span": [
              8,
              0,
              13,
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
              "inputType": ".sassafras.sassafras.Hello",
              "outputType": ".sassafras.sassafras.Hello",
              "location": {
                "span": [
                  37,
                  4,
                  38
                ],
                "leadingComments": " Here I document the Greet method.\n"
              }
            }
          ],
          "location": {
            "span": [
              35,
              0,
              38,
              1
            ]
          }
        }
      ],
      "options": {
        "goPackage": "blah/blah/blah;blah",
        "location": {
          "span": [
            4,
            0,
            42
          ]
        }
      },
      "syntax": "proto3",
      "location": {
        "span": [
          0,
          0,
          38,
          1
        ]
      }
    }
  ]
}
```
