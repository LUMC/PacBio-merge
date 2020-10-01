#!/usr/bin/env python

import logging
import re
import sys
import json

from collections import OrderedDict


def merge_count_dict(dictionaries):
    """ Merge the specified dictionaries together on the 'count' keys """
    merged = dict()

    for d in dictionaries:
        for key, value in d.items():
            # Is this the first time we see key
            if key not in merged:
                merged[key] = value
            # If the value is another dictionary
            elif isinstance(value, dict):
                    merged[key] = merge_count_dict([value, merged[key]])
            else:
                merged[key] += value

    return merged

def parse_PacBio_log(file_content):
    """ Parse ccs log file """
    data = dict()
    # This is a local dictionary to store which annotations belong to which
    # result dictionary. This will be used to structure the output, but will
    # not be part of the output itself
    annotations = dict()
    current_annotation = None

    for line in file_content:
        # Get rid of trailing newlines
        line = line.strip('\n')
        # Did we enter a new section with annotations for an earlier result?  # If so, we will only add an empty dictionary with the correct name # These field are of the format "something something for (A):"
        section_header_pattern = ' for [(][A-Z][)][:]$'
        if re.search(section_header_pattern, line):
            linedata = parse_line(line)
            ann = linedata['annotation']
            # Cut off the ' for (B):' part
            name = line[:-9]
            # We make a new heading with the current name under the data that
            # matches the current annotation
            current_annotation = dict()
            # We keep the dictonary accessible under 'current_annotation',
            # so we can keep adding new data to it without having to keep track
            # of where it belongs
            annotations[ann][name] = current_annotation
            continue

        linedata = parse_line(line)

        # If we got no data, we reached the end of the annotated section
        if not linedata:
            current_annotation = None
            continue

        # Lets get the name of the data
        name = linedata.pop('name')
        # If we are in an annotated section, we add the data to the current
        # annotation
        if current_annotation is not None:
            current_annotation[name] = linedata
        # Otherwise, we add the newfound annotation to the dictionary in case
        # we find a corresponding section later on.
        # The data from the current line we add directly to the output data
        else:
            annotation = linedata.pop('annotation')
            annotations[annotation] = linedata
            data[name] = linedata

    return data

def parse_line(line):
    """ Parse a line from the ccs log file """
    data = dict()

    # If we got an empty line to parse
    if not line.strip():
        return data

    # Split the line on the colon character
    try:
        key, values = line.strip().split(':')
    except ValueError as e:
        print(line)
        raise e

    # The key can have multiple parts
    keys = key.strip().split()

    # Does the key have an annotation (A), (B) etc
    if re.fullmatch('[(][A-Z][)]', keys[-1]):
        # We store the annotation without the bracets
        data['annotation'] = keys[-1][1:-1]
        # And we add the rest of the key as name
        data['name'] = ' '.join(keys[:-1])
    # Otherwise, we just store the name
    else:
        data['name'] = ' '.join(keys)

    # Parsing the values
    values = values.strip().split()
    # Are there are no values we are done
    if not values:
        return data

    # If there is a single value
    if len(values) == 1:
        value = values.pop()
        # Is the value a percentage, we don't add it
        if value.endswith('%'):
            pass
        # Otherwise, it is an integer
        else:
            data['count'] = int(value)
    elif len(values) == 2:
        # If there are multiple values, they are in the format
        # count (percentage%)
        count = values[0]
        percentage = values[1]

        # The percentage should be in the format:
        # (12.34%) or (100%) or (0%) or (-nan%)
        # So we can remove the bracets first
        percentage = percentage[1:-1]
        # Then we make sure it is one of the supported patterns
        assert re.fullmatch(r'(\d+\.\d+%|\d+%|-nan%)', percentage)

        # We don't add the percentage, we just want to make sure the formatting
        # is correct
        # Add the count as an integer
        data['count'] = int(count)

    return data

if __name__ == '__main__':
    dataset = list()
    for filename in sys.argv[1:]:
        with open(filename) as fin:
            data = parse_PacBio_log(fin)
            dataset.append(data)
            with open(filename+'.json', 'wt') as fout:
                print(json.dumps(data, indent=True), file=fout)

    # Merge the dictionaries
    merged = merge_count_dict(dataset)
    with open('merged.json', 'wt') as fout:
        print(json.dumps(merged, indent=True), file=fout)
