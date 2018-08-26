import re as _re
from functools import reduce as _reduce
from operator import add as _add
from random import choice as _choice

DIE_ROLL_EXPRESSION = (
    '([0-9]+)?d([0-9]+|[f%])([+-][0-9]+)?(/[+-][0-9]+)?(k[0-9]+)?'
)


def Roll(roll_description):
    roll = _parse_roll_description(roll_description)
    output = list()
    total = 0
    for _ in range(roll.count):
        result = _choice(_simple_side_generation(roll.sides))
        output.append(result)
    if roll.keep_best:
        output.sort()
        output.reverse()
        output = output[:roll.keep_best]
    output = map(lambda x: (x, roll.per_die), output)
    total = _reduce(_add, _reduce(_add, output))
    total += roll.post_roll
    total = total if total >= 0 else 0
    return (total, output)


def _parse_roll_description(roll_description):
    match = _re.search(DIE_ROLL_EXPRESSION, roll_description)
    roll = None
    if match:
        res = match.groups()
        roll = DieRoll()
        if not res[0]:
            roll.count = 1
        else:
            roll.count = int(res[0])
        if res[1] == '%':
            roll.sides = 100
        else:
            roll.sides = int(res[1])
        roll.post_roll = _decode_modifier(res[2])
        roll.per_die = _decode_modifier(res[3])
        roll.keep_best = int(res[4][1:]) if res[4] else None
    return roll


def _decode_modifier(modifier):
    if modifier:
        value = int(modifier[1:])
        if modifier[0] == '-':
            value *= -1
    else:
        value = 0
    return value


def _simple_side_generation(count):
    return tuple(map(lambda x: x + 1, range(count)))


class DieRoll:
    count = 1
    sides = range(6)
    post_roll = None
    per_die = None
    keep_best = None