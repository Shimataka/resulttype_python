from typing import TypeVar

import pytest

T = TypeVar("T")
E = TypeVar("E")

pytest.register_assert_rewrite("tests.test_base")
pytest.register_assert_rewrite("tests.test_deco")
pytest.register_assert_rewrite("tests.test_exception")
