import pytest

from pyilpp import UInt, line, measurement, parse, tag, tags


def test_measurement():
    # measurement = pp.Combine(
    #     pp.Word(pp.alphas) + pp.ZeroOrMore(pp.common.identifier)
    # ).set_results_name("measurement")

    lp1 = "foo,tag1=tag_value f=1 1.0"
    assert measurement.parse_string(lp1).as_dict() == {
        "measurement": "foo",
    }

    lp2 = "foo_bar f=1 1.0"
    assert measurement.parse_string(lp2).as_dict() == {
        "measurement": "foo_bar",
    }

    special_characters = 'my\\ Measurement fieldKey="string value"'
    assert measurement.parse_string(special_characters).as_dict() == {
        "measurement": "my Measurement",
    }


def test_line():
    comments = """# This is a comment
myMeasurement fieldKey=t,f1=FALSE 1556813561098000000
"""
    assert line.parse_string(comments).as_list()[0] == {
        "measurement": "myMeasurement",
        "tags": {},
        "fields": {"fieldKey": True, "f1": False},
        "time": 1556813561098000000,
    }

    no_time = """myMeasurement fieldKey=t,f1=FALSE"""
    assert line.parse_string(no_time).as_list()[0] == {
        "measurement": "myMeasurement",
        "tags": {},
        "fields": {"fieldKey": True, "f1": False},
    }

    floats = "myMeasurement f1=1.0,f2=1e10,f3=NaN,f4=inf,f5=-inf 1556813561098000000"
    assert line.parse_string(floats).as_list()[0] == {
        "measurement": "myMeasurement",
        "tags": {},
        "fields": {
            "f1": 1.0,
            "f2": 1e10,
            "f3": pytest.approx(float("nan"), nan_ok=True),
            "f4": float("inf"),
            "f5": float("-inf"),
        },
        "time": 1556813561098000000,
    }

    ints = "myMeasurement i1=1i,i2=0i,i3=-32768i 1556813561098000000"
    assert line.parse_string(ints).as_list()[0] == {
        "measurement": "myMeasurement",
        "tags": {},
        "fields": {
            "i1": 1,
            "i2": 0,
            "i3": -32768,
        },
        "time": 1556813561098000000,
    }

    uints = "myMeasurement u1=1u,u2=0u,u3=32768u 1556813561098000000"
    parsed = line.parse_string(uints).as_list()[0]
    assert isinstance(parsed["fields"]["u1"], UInt)
    assert parsed == {
        "measurement": "myMeasurement",
        "tags": {},
        "fields": {
            "u1": 1,
            "u2": 0,
            "u3": 32768,
        },
        "time": 1556813561098000000,
    }

    strs = 'm,t=v s1="string value",s2="\\"string\\" within a string",s3="Launch 🚀" 1556813561098000000'
    parsed = line.parse_string(strs).as_list()[0]
    assert parsed == {
        "measurement": "m",
        "tags": {"t": "v"},
        "fields": {
            "s1": "string value",
            "s2": '"string" within a string',
            "s3": "Launch 🚀",
        },
        "time": 1556813561098000000,
    }


def test_tag():
    t1 = "foo=bar"
    assert tag.parse_string(t1).as_dict() == {"tag": {"foo": "bar"}}

    t2 = 'field="string\\ value"'
    assert tag.parse_string(t2).as_dict() == {"tag": {"field": '"string value"'}}

    st = "tag\\ Key1=tag\\ Value1"
    assert tag.parse_string(st).as_dict() == {"tag": {"tag Key1": "tag Value1"}}

    st = "tag\\ Key2=tag\\ Value2"
    assert tag.parse_string(st).as_dict() == {"tag": {"tag Key2": "tag Value2"}}

    st = "tagKey=🍭"
    assert tag.parse_string(st).as_dict() == {"tag": {"tagKey": "🍭"}}


def test_tags():
    ts = ""
    assert tags.parse_string(ts).as_dict() == {"tags": {}}

    ts = ",tag\\ Key1=tag\\ Value1,tag\\ Key2=tag\\ Value2"
    assert tags.parse_string(ts).as_dict() == {
        "tags": {
            "tag Key1": "tag Value1",
            "tag Key2": "tag Value2",
        },
    }


def test_lines():
    example = """
# Syntax
# <measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]

# Example
myMeasurement,tag1=value1,tag2=value2 fieldKey="fieldValue" 1556813561098000000
"""
    res = parse(example)
    assert len(res) == 1
    assert res[0] == {
        "measurement": "myMeasurement",
        "tags": {"tag1": "value1", "tag2": "value2"},
        "fields": {"fieldKey": "fieldValue"},
        "time": 1556813561098000000,
    }

    data = """
measurement,tag1=tag_value1,tag2=tag_value2 int=1i,uint=1u,float=0.0,str="foo bar",boolean=t 1556813561098000000
measurement2,tag1=tag_value1,tag2=tag_value2 int=1i,uint=1u,float=0.0,str="foo bar",boolean=t 1556813561098000000
"""
    res = parse(data)
    assert len(res) == 2
    assert res[0] == {
        "measurement": "measurement",
        "tags": {"tag1": "tag_value1", "tag2": "tag_value2"},
        "fields": {
            "int": 1,
            "uint": 1,
            "float": 0.0,
            "str": "foo bar",
            "boolean": True,
        },
        "time": 1556813561098000000,
    }
    assert res[1] == {
        "measurement": "measurement2",
        "tags": {"tag1": "tag_value1", "tag2": "tag_value2"},
        "fields": {
            "int": 1,
            "uint": 1,
            "float": 0.0,
            "str": "foo bar",
            "boolean": True,
        },
        "time": 1556813561098000000,
    }
