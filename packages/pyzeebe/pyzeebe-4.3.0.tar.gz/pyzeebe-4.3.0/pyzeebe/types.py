from collections.abc import Mapping, Sequence
from typing import Any

from typing_extensions import TypeAlias

Headers: TypeAlias = Mapping[str, Any]
Variables: TypeAlias = Mapping[str, Any]
Unset = "UNSET"

ChannelArgumentType: TypeAlias = Sequence[tuple[str, Any]]
