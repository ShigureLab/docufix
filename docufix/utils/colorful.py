from __future__ import annotations

from .._compat import Final

Color = Final[str]

CSI: Color = "\x1b["

RED: Color = f"{CSI}31m"
GREEN: Color = f"{CSI}32m"
YELLOW: Color = f"{CSI}33m"
BLUE: Color = f"{CSI}34m"
MAGENTA: Color = f"{CSI}35m"
CYAN: Color = f"{CSI}36m"
WHITE: Color = f"{CSI}37m"

BACK_RED: Color = f"{CSI}41m"
BACK_GREEN: Color = f"{CSI}42m"
BACK_YELLOW: Color = f"{CSI}43m"
BACK_BLUE: Color = f"{CSI}44m"
BACK_MAGENTA: Color = f"{CSI}45m"
BACK_CYAN: Color = f"{CSI}46m"
BACK_WHITE: Color = f"{CSI}47m"

RST: Color = f"{CSI}0m"
