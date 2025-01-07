## InfluxDB line protocol parser

A simple [InfluxDB line protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/) parser built using pyparsing.

The entry point is the `parse` function which receives a string and returns a list of the parsed line-protocol.

### Example

```python
>>> import pyilpp
>>> data = """
... measurement,tag1=tag_value1,tag2=tag_value2 int=1i,uint=1u,float=0.0,str="foo bar",boolean=t 1556813561098000000
... measurement2,tag1=tag_value1,tag2=tag_value2 int=1i,uint=1u,float=0.0,str="foo bar",boolean=t 1556813561098000000
... """
>>> res = pyilpp.parse(data)
>>> print(res)
[{'measurement': 'measurement',
  'tags': {'tag1': 'tag_value1', 'tag2': 'tag_value2'},
  'fields': {'int': 1,
             'uint': 1,
             'float': 0.0,
             'str': 'foo bar',
             'boolean': True},
  'time': 1556813561098000000},
 {'measurement': 'measurement2',
  'tags': {'tag1': 'tag_value1', 'tag2': 'tag_value2'},
  'fields': {'int': 1,
             'uint': 1,
             'float': 0.0,
             'str': 'foo bar',
             'boolean': True},
  'time': 1556813561098000000}]
```

### Installation

From PyPI:

```bash
$ python3 -m pip install pyilpp
```

or from source (needs [pdm](https://pdm-project.org)):

```bash
$ git clone https://github.com/maxyz/pyilpp.git
$ cd pyilpp
$ pdm build
$ python3 -m pip install ./dist/pyilpp-*.whl
```
