# type: ignore[reportUnknownMemberType]

"""test_result.py

## 3つのテストクラスに分けて実装

- TestResult: 基本的なResult型の機能テスト
    - Ok/Errの状態チェック
    - 値の取り出し
    - マッピング処理
    - エラーハンドリング
- TestResultDecorator: @resultデコレータのテスト
    - デコレータの成功/失敗ケース
    - デコレータのチェーン・伝搬処理
- TestQuestion: question関数のテスト
    - 正常系: 値の取り出し
    - エラー系: エラーハンドリング

## カバレッジを最大化するため、以下のケースをテスト

- Ok/Errの両方のケース
- すべてのメソッド (is_ok, is_err, unwrap, unwrap_or, unwrap_err, map)
- エラーケース (UnwrapErrorの発生)
- デコレータの成功/失敗ケース
- デコレータのチェーン処理
- 例外を含むケース

## 型ヒントを完全に記述

- すべての関数に戻り値の型を記述
- すべての変数に型を記述
- ジェネリック型パラメータを適切に使用

## pytestとunittestの両方を使用

- unittest.TestCaseを基本として使用
- pytestのraisesを使用してエラーケースをテスト
"""

import unittest

import pytest

from pyresults.result import Err, Ok, Result, UnwrapError, question, result


class TestResult(unittest.TestCase):
    def test_ok_is_ok(self) -> None:
        ok: Result[int, str] = Ok(1)
        assert ok.is_ok() is True
        assert ok.is_err() is False

    def test_err_is_err(self) -> None:
        err: Result[int, str] = Err("error")
        assert err.is_ok() is False
        assert err.is_err() is True

    def test_ok_unwrap(self) -> None:
        ok: Result[int, str] = Ok(1)
        assert ok.unwrap() == 1

    def test_err_unwrap(self) -> None:
        err: Result[int, str] = Err("error")
        with pytest.raises(UnwrapError):
            err.unwrap()

    def test_ok_unwrap_or(self) -> None:
        ok: Result[int, str] = Ok(1)
        assert ok.unwrap_or(2) == 1

    def test_err_unwrap_or(self) -> None:
        err: Result[int, str] = Err("error")
        assert err.unwrap_or(2) == 2

    def test_ok_unwrap_err(self) -> None:
        ok: Result[int, str] = Ok(1)
        with pytest.raises(UnwrapError):
            ok.unwrap_err()

    def test_err_unwrap_err(self) -> None:
        err: Result[int, str] = Err("error")
        assert err.unwrap_err() == "error"

    def test_ok_map(self) -> None:
        ok: Result[int, str] = Ok(1)
        mapped: Result[str, str] = ok.map(str)
        assert isinstance(mapped, Ok)
        assert mapped.unwrap() == "1"

    def test_err_map(self) -> None:
        err: Result[int, str] = Err("error")
        mapped: Result[str, str] = err.map(str)
        assert isinstance(mapped, Err)
        assert mapped.unwrap_err() == "error"

    def test_unwrap_error_with_exception(self) -> None:
        ok: Result[int, Exception] = Ok(1)
        with pytest.raises(UnwrapError):
            ok.unwrap_err()

        err: Result[int, Exception] = Err(ValueError("test"))
        with pytest.raises(UnwrapError):
            err.unwrap()


@result
def example_success() -> Result[int, str]:
    return Ok(1)


@result
def example_error() -> Result[int, str]:
    return Err("error")


@result
def example_chained() -> Result[int, str]:
    val: int = question(example_success())
    return Ok(val + 1)


@result
def example_chained_error() -> Result[int, str]:
    _: int = question(example_error())
    return Ok(1)


class TestResultDecorator(unittest.TestCase):
    def test_result_decorator_success(self) -> None:
        result: Result[int, str] = example_success()
        assert isinstance(result, Ok)
        assert result.unwrap() == 1

    def test_result_decorator_error(self) -> None:
        result: Result[int, str] = example_error()
        assert isinstance(result, Err)
        assert result.unwrap_err() == "error"

    def test_result_decorator_chained(self) -> None:
        result: Result[int, str] = example_chained()
        assert isinstance(result, Ok)
        assert result.unwrap() == 2

    def test_result_decorator_chained_error(self) -> None:
        result: Result[int, str] = example_chained_error()
        assert isinstance(result, Err)
        assert result.unwrap_err() == "error"


class TestQuestion(unittest.TestCase):
    def test_question_ok(self) -> None:
        ok: Result[int, str] = Ok(1)
        assert question(ok) == 1

    def test_question_err(self) -> None:
        err: Result[int, str] = Err("error")
        with pytest.raises(UnwrapError):
            question(err)


if __name__ == "__main__":
    unittest.main()
