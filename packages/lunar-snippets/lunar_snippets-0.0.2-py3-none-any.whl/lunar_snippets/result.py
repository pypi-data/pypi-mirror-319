from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional


class Severity(Enum):
    OK = "ok"
    WARN = "warn"
    CRITICAL = "critical"


class Op(Enum):
    CONTAINS = "contains"
    EQUALS = "equals"
    TRUE = "true"
    FALSE = "false"
    GREATER = "greater"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS = "less"
    LESS_OR_EQUAL = "less_or_equal"


@dataclass
class AssertionResult:
    op: Op
    args: list[Any]
    ok: bool
    severity: Severity
    details: str
    path: Optional[str] = None
