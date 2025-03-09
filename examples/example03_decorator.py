# ruff: noqa: T201

"""Example 3: Decorator

This example demonstrates the usage of the `@result` decorator.

Notes:
    - `@result` デコレータは `Result` 型の値を返す関数をラップして、エラーを伝播する。
        ラップされた関数内で `UnwrapError` 型の例外が発生した場合、付随する `Err` 型の値をそのまま返して伝播する。
    - `question` 関数は、引数に `Result` 型の値を受け取り、その値が `Ok` 型の場合は `unwrap` して値を返すが、
        エラーが発生した場合は `UnwrapError` 型の例外を発生させる。
"""

from pyresults import Err, Ok, Result, question, result


def inner_function() -> Result[int, str]:
    return Err("error@inner_function")


@result
def outer_function() -> Result[int, str]:
    result = question(inner_function())
    return Ok(result)


result = outer_function()  # Err("error@inner_function")

if result.is_err():
    print(result.unwrap_err())
