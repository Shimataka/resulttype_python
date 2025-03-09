# ruff: noqa: T201

"""Example 2: Default Value

This example demonstrates the usage of the `unwrap_or` method.

Notes:
    - `unwrap_or` は `Result` 型が `Ok` 型の場合は `Ok` 型の値を返す
    - `unwrap_or` は `Result` 型が `Err` 型の場合は `default_value` を返す
"""

from pyresults import Err, Ok, Result


def get_config(key: str) -> Result[str, str]:
    """Get a configuration value.

    Args:
        key (str): The key to get the configuration value

    Returns:
        Result[str, str]: The configuration value

    Notes:
        - 正常系では `Ok` 型でかこまれた `str` 型を返す (ローカルホスト名)
        - 設定値が見つからないような異常系では `Err` 型でかこまれた `str` 型を返す
        - 設定値が見つからないエラーのメッセージは `"設定 {key} が見つかりません"` とした
    """
    if key == "host":
        return Ok("localhost")
    return Err(f"設定 {key} が見つかりません")


# エラー時にデフォルト値を使用
value = get_config("unknown_key").unwrap_or("default_value")
print(value)  # "default_value"
