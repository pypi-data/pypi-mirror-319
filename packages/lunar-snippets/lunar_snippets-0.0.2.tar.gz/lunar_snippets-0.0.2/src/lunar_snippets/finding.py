import json
from typing import Any, Callable
from .data import JsonPathExpression, SnippetData
from .result import AssertionResult, Op, Severity


class Finding:
    def __init__(self, name: str, severity: Severity, data: SnippetData):
        self.name = name

        if not isinstance(severity, Severity):
            raise ValueError(
                f"Severity must be a Severity enum, got {severity}"
            )
        self.severity = severity

        if not isinstance(data, SnippetData):
            raise ValueError(
                f"Data must be a SnippetData instance, got {data}"
            )
        self.data = data

        self._accessed_paths = []
        self._used_vars = []
        self._results = []
        self._submitted = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.submit()

    def submit(self):
        if not self._submitted:
            print("submitting")
            json.dump(self._results, open("results.json", "w"))
            self._submitted = True

    def _make_assertion(
        self,
        op: Op,
        check_fn: Callable[[Any], bool],
        value: str,
        error_message: str,
        success_message: str
    ) -> AssertionResult:
        value = value
        path = None

        # Currently, if its not a JsonPathExpression, we assume it's a string
        # that should be used as raw value to compare against. Unsure how else
        # to handle this case?
        try:
            # Will raise ValueError if not a valid jsonpath
            jsonPath = JsonPathExpression(value)
            value = self.data.get(jsonPath)
            path = jsonPath.full_path
        except Exception as e:
            raise ValueError(f"Invalid JSON path: {value}") from e

        if isinstance(value, JsonPathExpression):
            value = self.data.get(value)
            path = value.full_path

        ok = check_fn(value)
        self._results.append(
            AssertionResult(
                op=op,
                args=[value],
                ok=ok,
                severity=Severity.OK if ok else self.severity,
                details=success_message if ok else error_message,
                path=path
            )
        )

    def is_true(
        self,
        value: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.TRUE,
            lambda v: v is True,
            value,
            error_message or f"{value} is not true",
            success_message or f"{value} is true"
        )

    def is_false(
        self,
        value: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.FALSE,
            lambda v: v is False,
            value,
            error_message or f"{value} is not false",
            success_message or f"{value} is false"
        )

    def equals(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.EQUALS,
            lambda v: v == expected,
            value,
            error_message or f"{value} is not equal to {expected}",
            success_message or f"{value} is equal to {expected}"
        )

    def contains(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.CONTAINS,
            lambda v: expected in v,
            value,
            error_message or f"{value} does not contain {expected}",
            success_message or f"{value} contains {expected}"
        )

    def greater(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.GREATER,
            lambda v: v > expected,
            value,
            error_message or f"{value} is not greater than {expected}",
            success_message or f"{value} is greater than {expected}"
        )

    def greater_or_equal(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.GREATER_OR_EQUAL,
            lambda v: v >= expected,
            value,
            error_message or
            f"{value} is not greater than or equal to {expected}",
            success_message or
            f"{value} is greater than or equal to {expected}"
        )

    def less(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.LESS,
            lambda v: v < expected,
            value,
            error_message or f"{value} is not less than {expected}",
            success_message or f"{value} is less than {expected}"
        )

    def less_or_equal(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.LESS_OR_EQUAL,
            lambda v: v <= expected,
            value,
            error_message or
            f"{value} is not less than or equal to {expected}",
            success_message or
            f"{value} is less than or equal to {expected}"
        )
