from typing import Optional, Union, get_origin, get_args

MaybeInt1 = Optional[int]
print(type(MaybeInt1), MaybeInt1, get_origin(MaybeInt1), get_args(MaybeInt1), MaybeInt1.__args__)

MaybeInt2 = int | None
print(type(MaybeInt2), MaybeInt2, get_origin(MaybeInt2), get_args(MaybeInt2), MaybeInt2.__args__)

print(Optional[int] | str | bool | float)