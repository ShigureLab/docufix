from __future__ import annotations

from typing import Final, TypeAlias

Color: TypeAlias = Final[str]

CSI: Color = "\x1b["

RED: Color = f"{CSI}31m"
GREEN: Color = f"{CSI}32m"
YELLOW: Color = f"{CSI}33m"
BLUE: Color = f"{CSI}34m"
MAGENTA: Color = f"{CSI}35m"
CYAN: Color = f"{CSI}36m"
WHITE: Color = f"{CSI}37m"

RST: Color = f"{CSI}0m"
