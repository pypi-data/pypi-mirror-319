import itertools, collections, more_itertools
from collections.abc import Iterable, Callable, Mapping
from typing import Literal


def f[T, KT](data: Iterable[T], key: Callable[[T], KT]) -> Mapping[KT, Iterable[T]]:
    result = collections.defaultdict(list[T])
    for element in data:
        result[key(element)].append(element)
    return result


test = 'Hello Every One'


def key(ch: str) -> Literal['l' ,'u', 'n']:
    return 'l' if ch.islower() else 'u' if ch.isupper() else 'n'


a = f(test, key)
print(a)
assert set(a.keys()) == {'l', 'u', 'n'}
assert tuple(a['l']) == tuple('elloveryne')
assert tuple(a['u']) == tuple('HEO')
assert tuple(a['n']) == tuple('  ')



