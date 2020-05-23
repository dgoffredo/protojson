#!/usr/bin/env python3
"Convert compiled protobuf schemas into JSON"

import json
import sys

import google.protobuf.compiler  # for the _message types
from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.json_format import MessageToDict


def jsonify_path(path, proto_file_message):
    """Convert the specified source location `path` to an analogous path
    containing field names instead of field numbers, so that the resulting path
    could be used to address a subtree within the JSON version of
    `proto_file_message`.
    """
    result = []
    message = proto_file_message
    for part in path:
        jsonified_part, message = jsonify_path_part(part, message)
        result.append(jsonified_part)

    return result


def jsonify_path_part(part, message):
    Listy = google.protobuf.pyext._message.RepeatedCompositeContainer
    if isinstance(message, Listy):
        return part, message[part]

    for descriptor, value in message.ListFields():
        if descriptor.number == part:
            return descriptor.camelcase_name, value

    raise Exception('Invalid field ID {} for message {}'.format(part, message))


def resolve(json_path, obj):
    """Extract the subtree within `obj` addressed by `json_path`."""
    for part in json_path:
        obj = obj[part]

    return obj


def to_dict_with_locations(proto_request):
    proto_py = MessageToDict(proto_request)

    for proto, py in zip(proto_request.proto_file, proto_py['protoFile']):
        for location, py_loc in zip(proto.source_code_info.location,
                                    py['sourceCodeInfo']['location']):
            json_path = jsonify_path(location.path, proto)
            json_target = resolve(json_path, py)
            if isinstance(json_target, dict):
                # Leave out .path, since it refers to field IDs, which don't
                # have any meaning anymore once we've used MessageToDict.
                json_target['location'] = {
                    key: value \
                    for key, value in py_loc.items() if key != 'path'
                }
        del py['sourceCodeInfo']

    return proto_py


def run_plugin(input_raw_file, output_raw_file):
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(input_raw_file.read())

    proto_py = to_dict_with_locations(request)

    response = plugin.CodeGeneratorResponse()
    file = response.file.add()
    file.name = 'request.json'
    file.content = json.dumps(proto_py)

    output_raw_file.write(response.SerializeToString())


if __name__ == '__main__':
    run_plugin(sys.stdin.buffer, sys.stdout.buffer)
