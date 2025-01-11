import enum
from typing import get_args, get_origin, Literal, Sequence, Annotated, _SpecialForm

from typing_extensions import Doc

from typeformtools import undisguised


type LiteralValueType = Annotated[str | bytes | int | bool | enum.Enum | None,
                                  Doc("Type of values that can make up a `Literal`.")]


def literal_values(tf: _SpecialForm) -> Sequence[LiteralValueType]:
    """Return literal values making up `Literal` `tf` (or fail for other kind of `tf`).

    >>> literal_values(Literal[1, 'test'])
    (1, 'test')
    """
    tf = undisguised(tf)
    if get_origin(tf) is not Literal:
        raise TypeError(f"{tf} is not a parametrised Literal[...]")

    logger.debug(f"Literal[{', '.join(map(repr, get_args(tf)))}]")
    return get_args(tf)
