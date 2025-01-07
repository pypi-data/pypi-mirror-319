import typing as t

import pyparsing as pp


class UInt(int):
    pass


class LineProtocol(t.TypedDict):
    measurement: str
    tags: dict[str, str]
    fields: dict[str, bool | int | UInt | float | str]
    time: t.NotRequired[int]


def to_bool(toks: pp.ParseResults) -> bool:
    t = toks[0]
    return t in {"t", "T", "true", "True", "TRUE"}


def to_uint(toks: pp.ParseResults) -> UInt:
    tok = toks[0]
    return UInt(t.cast(int, tok))


def merge_dicts(toks: pp.ParseResults) -> dict:
    res = {}
    for d in toks:
        res |= d
    return res


def to_line_protocol(toks: pp.ParseResults) -> LineProtocol:
    return t.cast(LineProtocol, toks.as_dict())


mfc = pp.Regex(r"[^_ ,\\]")
mc = pp.Regex(r"[^ ,\\]")
qc = pp.Suppress("\\") + pp.Regex(".")
measurement = pp.Combine(mfc + pp.ZeroOrMore(mc ^ qc)).set_results_name("measurement")

tfc = pp.Regex(r"[^_ ,=\\]")
tc = pp.Regex(r"[^ ,=\\]")
tag_key = pp.Combine(tfc + pp.ZeroOrMore(tc ^ qc)).set_results_name("key")
tag_value = pp.Combine(tfc + pp.ZeroOrMore(tc ^ qc)).set_results_name("value")

tag = pp.Dict(pp.Group(tag_key + pp.Suppress("=") + tag_value)).set_results_name("tag")
tags = (
    pp.Opt(
        pp.Suppress(",")
        + pp.DelimitedList(tag, delim=",").set_parse_action(merge_dicts)
    )
    .set_parse_action(merge_dicts)
    .set_results_name("tags")
)

field_key = pp.Combine(tfc + pp.ZeroOrMore(tc ^ qc)).set_results_name("key")

boolean_value = (
    pp.Literal("t")
    ^ "T"
    ^ "true"
    ^ "True"
    ^ "TRUE"
    ^ "f"
    ^ "F"
    ^ "false"
    ^ "False"
    ^ "FALSE"
).set_parse_action(to_bool)

float_value = pp.common.ieee_float
int_value = pp.common.signed_integer + pp.Suppress("i")
uint_value = (pp.common.integer + pp.Suppress("u")).set_parse_action(to_uint)

sc = pp.Regex(r"[^\"\\]")
str_value = pp.Suppress('"') + pp.Combine(pp.ZeroOrMore(sc ^ qc)) + pp.Suppress('"')

field_value = (
    boolean_value ^ float_value ^ int_value ^ uint_value ^ str_value
).set_results_name("value")

field = pp.Dict(pp.Group(field_key + pp.Suppress("=") + field_value)).set_results_name(
    "field"
)

fields = (
    (pp.DelimitedList(field, delim=","))
    .set_parse_action(merge_dicts)
    .set_results_name("fields")
)

time = pp.Opt(pp.common.signed_integer).set_results_name("time")

comment = pp.Suppress("#" + pp.restOfLine())

line = (
    pp.Suppress(pp.LineStart())
    + pp.ZeroOrMore(comment)
    + measurement
    + tags
    + fields
    + time
    + pp.Suppress(pp.LineEnd())
).set_parse_action(to_line_protocol)

lines = pp.ZeroOrMore(line)


def parse(input: str) -> t.Sequence[LineProtocol]:
    return lines.parse_string(input).as_list()
