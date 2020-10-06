import pytest
import sys
sys.path.insert(0, '.')
from pacbio_merge import merge_legacy_count_dict

# Testdata where we merge a dict into itself
# Source dict, times, merged dict
TEST = [
        ( {'value': {'count': 5}}, 1, {'value': {'count': 5}}),
        ( {'value': {'count': 5}}, 2, {'value': {'count': 10}}),
        ( {'value': {'extra_key': {'count': 5}}}, 1, {'value': {'extra_key': {'count': 5}}}),
        ( {'value': {'extra_key': {'count': 5}}}, 3, {'value': {'extra_key':
            {'count': 15}}}),
]

@pytest.mark.parametrize(['source', 'times', 'target'], TEST)
def test_merge_dict(source, times, target):
    merged = merge_legacy_count_dict([source]*times)
    assert merged == target
