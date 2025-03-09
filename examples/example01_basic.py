# ruff: noqa: T201

"""Example 1: Basic Usage

## 基本的な使い方

- `Ok` 型は `Result` 型の正常系を表す
- `Err` 型は `Result` 型の異常系を表す
- `Result` 型は `Ok` 型と `Err` 型のUnion型となっていて、どちらかを返す
- `Result` 型のメソッド `is_ok` と `is_err`
    - `is_ok` は `Result` 型が `Ok` 型かどうかをbool型で返す
    - `is_err` は `Result` 型が `Err` 型かどうかをbool型で返す
- `Result` 型のメソッド `unwrap` と `unwrap_err`
    - `unwrap` は `Result` 型が `Ok` 型の場合は `Ok` 型の値を返す
    - `unwrap_err` は `Result` 型が `Err` 型の場合は `Err` 型の値を返す
    - この2つに当てはまらない条件の場合、`UnwrapError` 型の例外を発生させる
"""

from pyresults import Err, Ok, Result


def divide(a: float, b: float) -> Result[float, str]:
    """Divide two floating numbers.

    Args:
        a (float): The dividend
        b (float): The divisor

    Returns:
        Result[float, str]: The result of the division

    Notes:
        - 正常系では `Ok` 型でかこまれた `float` 型を返す (商を返す)
        - ゼロ除算となるような異常系では `Err` 型でかこまれた `str` 型を返す
        - ゼロ除算エラーのメッセージは `"ゼロ除算エラー"` とした
    """
    if b == 0:
        return Err("ゼロ除算エラー")
    return Ok(a / b)


# 成功ケース
result1 = divide(10, 2)
if result1.is_ok():  # True
    print(result1.unwrap())  # 5.0

# エラーケース
result2 = divide(10, 0)
if result2.is_err():  # True
    print(result2.unwrap_err())  # "ゼロ除算エラー"

# エラーケースで例外が発生する
result3 = divide(10, 0)
print(result3.unwrap())  # 例外が発生する
