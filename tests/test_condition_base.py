import pytest

from vakt.conditions.base import Condition
from vakt.conditions.string import StringEqualCondition
from vakt.exceptions import ConditionCreationError
import vakt.conditions.net


class ABCondition(Condition):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def satisfied(self, what=None, request=None):
        return self.a == self.b


def test_satisfied():
    assert ABCondition(2, 2).satisfied()
    assert not ABCondition(1, 2).satisfied()


def test_to_json():
    conditions = [
        ABCondition(1, 2),
        ABCondition('x', 'y'),
    ]
    assert '{"contents": {"a": 1, "b": 2}, "type": "test_condition_base.ABCondition"}' == conditions[0].to_json()
    assert '{"contents": {"a": "x", "b": "y"}, "type": "test_condition_base.ABCondition"}' == conditions[1].to_json()


def test_from_json():
    conditions = [
        '{"contents": {"a": 1, "b": 1}, "type": "test_condition_base.ABCondition"}',
        '{"contents": {"a": "x", "b": "y"}, "type": "test_condition_base.ABCondition"}',
    ]
    c1 = Condition.from_json(conditions[0])
    c2 = Condition.from_json(conditions[1])
    assert isinstance(c1, ABCondition)
    assert isinstance(c2, ABCondition)
    assert c1.satisfied()
    assert not c2.satisfied()


@pytest.mark.parametrize('condition, satisfied', [
    (ABCondition(1, 1), True),
    (ABCondition(1, 1.2), False),
    (StringEqualCondition('foo'), False),
    (vakt.conditions.net.CIDRCondition('192.168.0.1/24'), False),
])
def test_json_roundtrip(condition, satisfied):
    c1 = Condition.from_json(condition.to_json())
    assert isinstance(c1, condition.__class__)
    assert c1.__dict__ == condition.__dict__
    assert satisfied == c1.satisfied(None, None)


@pytest.mark.parametrize('data, msg', [
    ('{crap}', 'Invalid JSON data'),
    ("{}", "No 'contents' key in JSON"),
    ('{"type": "vakt.conditions.net.CIDRCondition"}', "No 'contents' key in JSON"),
    ('{"contents": {"cidr": "192.168.2.0/24"}}', "No 'type' key in JSON"),
    ('{"contents": {"cidr": "192.168.2.0/24", "foo":"bar"}, "type": "vakt.conditions.net.CIDRCondition"}',
     'Number of arguments does not match. Given 2. Expected 1'),
])
def test_from_json_fails(data, msg):
    with pytest.raises(ConditionCreationError) as excinfo:
        Condition.from_json(data)
    assert msg in str(excinfo.value)