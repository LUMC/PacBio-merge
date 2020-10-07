import pytest
import sys
import os
sys.path.insert(0, '.')
import json
from pacbio_merge import merge_legacy_count_dict, merge_json_reports

# Testdata where we merge a dict into itself
# Source dict, times, merged dict
TEST_LEGACY = [
        ( {'value': {'count': 5}}, 1, {'value': {'count': 5}}),
        ( {'value': {'count': 5}}, 2, {'value': {'count': 10}}),
        ( {'value': {'extra_key': {'count': 5}}}, 1, {'value': {'extra_key': {'count': 5}}}),
        ( {'value': {'extra_key': {'count': 5}}}, 3, {'value': {'extra_key':
            {'count': 15}}}),
]

def jl(filename):
    """ Load json files from test/v5.0.0/target """
    folder = 'test/v5.0.0/target'
    return json.load(open(os.path.join(folder,filename)))

# Testdata for PacBio json reports
# input dictionary, number of times, output dictionary
TEST_JSON = [
        ([{'id': 'ccs_processing'}], {'id': 'ccs_processing'}),
        #([jl('chunk1.json'), jl('chunk2.json')], jl('target.json'))
]

# Testdata for dictionaries that should not be merged
TEST_INVALID_COMBINATION = [
        ([{'id': 'ccs_processing'}, {'id': 'not_ccs_processing'}]),
]

@pytest.mark.parametrize(['source', 'times', 'target'], TEST_LEGACY)
def test_merge_legacy_dict(source, times, target):
    merged = merge_legacy_count_dict([source]*times)
    assert merged == target

@pytest.mark.parametrize(['source', 'target'], TEST_JSON)
def test_merge_json(source, target):
    merged = merge_json_reports(source)
    assert merged == target

@pytest.mark.parametrize('dataset', TEST_INVALID_COMBINATION)
def test_merge_invalid_json(dataset):
    with pytest.raises(AssertionError):
        merged = merge_json_reports(dataset)
