# pyresults

RustのResult型をPythonに移植した型安全なエラーハンドリングライブラリ

## 概要

`PyResults`は、Rustの`Result<T, E>`型をPythonで忠実に再現したライブラリです。従来の例外処理に代わる宣言的で型安全なエラーハンドリングを提供し、関数型プログラミングのパターンを活用してより堅牢なコードの作成を支援します。

## 特徴

- **型安全性**: TypeHintによる完全な型推論サポート
- **Rust互換**: RustのResult型のメソッドを完全実装
- **関数型プログラミング**: `map`, `and_then`, `or_else`などのコンビネータサポート
- **Zero-cost abstraction**: 最小限のオーバーヘッドで高い表現力
- **question mark operator**: Rustの`?`演算子をPythonで再現

## インストール

```bash
pip install git+https://github.com/Shimataka/resulttype_python.git
```

## 基本的な使い方

### Result型の作成

```python
from pyresults import Ok, Err, Result

# 成功を表すOk
success: Result[int, str] = Ok(42)

# 失敗を表すErr
failure: Result[int, str] = Err("エラーが発生しました")
```

### 結果の判定

```python
result = Ok(10)

if result.is_ok():
    print(f"成功: {result.unwrap()}")  # 成功: 10

if result.is_err():
    print(f"失敗: {result.unwrap_err()}")
```

### 安全な値の取得

```python
# デフォルト値を指定
value = result.unwrap_or(0)  # 成功時は値、失敗時は0

# 関数でデフォルト値を計算
value = result.unwrap_or_else(lambda err: len(err))

# カスタムメッセージ付きで取得
value = result.expect("値が必要です")
```

## 高度な使い方

### 値の変換 - map操作

```python
from pyresults import Ok, Err

# 成功値に関数を適用
result = Ok(5).map(lambda x: x * 2)  # Ok(10)

# エラー値に関数を適用
result = Err("error").map_err(lambda e: f"Failed: {e}")  # Err("Failed: error")

# 成功時は関数適用、失敗時はデフォルト値
result = Ok(5).map_or(lambda x: x * 2, 0)  # 10
result = Err("error").map_or(lambda x: x * 2, 0)  # 0
```

### チェーン操作 - and_then/or_else

```python
def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Err("ゼロ除算エラー")
    return Ok(a / b)

def sqrt(x: float) -> Result[float, str]:
    if x < 0:
        return Err("負の数の平方根")
    return Ok(x ** 0.5)

# チェーン操作
result = (Ok(16.0)
          .and_then(lambda x: divide(x, 4))  # Ok(4.0)
          .and_then(sqrt))                   # Ok(2.0)

# エラー時のリカバリ
result = (Err("初期エラー")
          .or_else(lambda _: Ok(10))         # Ok(10)
          .and_then(sqrt))                   # Ok(3.16...)
```

### question mark operator - Rustライクなエラー伝播

```python
from pyresults import result, question

@result
def complex_calculation(a: float, b: float, c: float) -> Result[float, str]:
    # ?演算子のように動作 - エラー時は即座に関数から抜ける
    x = question(divide(a, b))
    y = question(sqrt(x))
    z = question(divide(y, c))
    return Ok(z)

result = complex_calculation(16.0, 4.0, 2.0)  # Ok(1.0)
result = complex_calculation(16.0, 0.0, 2.0)  # Err("ゼロ除算エラー")
```

### イテレータサポート

```python
# 成功値のイテレータ
for value in Ok(42).iter():
    print(value)  # 42

# エラー値のイテレータ
for error in Err("failed").iter_err():
    print(error)  # "failed"

# 複数のResultから成功値のみを抽出
results = [Ok(1), Err("error"), Ok(3), Ok(5)]
values = [val for result in results for val in result.iter()]
print(values)  # [1, 3, 5]
```

## 実践的な例

### ファイル操作

```python
import json
from pathlib import Path
from pyresults import Result, Ok, Err, result, question

def read_file(path: str) -> Result[str, str]:
    try:
        return Ok(Path(path).read_text())
    except FileNotFoundError:
        return Err(f"ファイルが見つかりません: {path}")
    except PermissionError:
        return Err(f"ファイルの読み取り権限がありません: {path}")

def parse_json(content: str) -> Result[dict, str]:
    try:
        return Ok(json.loads(content))
    except json.JSONDecodeError as e:
        return Err(f"JSONパースエラー: {e}")

@result
def load_config(path: str) -> Result[dict, str]:
    content = question(read_file(path))
    config = question(parse_json(content))
    return Ok(config)

# 使用例
config_result = load_config("config.json")
config = config_result.unwrap_or({})
```

### API呼び出し

```python
import requests
from dataclasses import dataclass
from pyresults import Result, Ok, Err

@dataclass
class User:
    id: int
    name: str
    email: str

def fetch_user(user_id: int) -> Result[User, str]:
    try:
        response = requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 404:
            return Err("ユーザーが見つかりません")
        elif response.status_code != 200:
            return Err(f"APIエラー: {response.status_code}")

        data = response.json()
        user = User(
            id=data["id"],
            name=data["name"],
            email=data["email"]
        )
        return Ok(user)
    except requests.RequestException as e:
        return Err(f"ネットワークエラー: {e}")

# エラーハンドリング
user_result = fetch_user(123)
user_result.map_or_else(
    lambda user: print(f"ユーザー取得成功: {user.name}"),
    lambda error: print(f"エラー: {error}")
)
```

### バリデーション

```python
from typing import List
from pyresults import Result, Ok, Err, result, question

def validate_email(email: str) -> Result[str, str]:
    if "@" not in email:
        return Err("無効なメールアドレス")
    return Ok(email)

def validate_age(age: int) -> Result[int, str]:
    if age < 0 or age > 150:
        return Err("年齢は0-150の範囲で入力してください")
    return Ok(age)

@result
def create_user(name: str, email: str, age: int) -> Result[dict, str]:
    validated_email = question(validate_email(email))
    validated_age = question(validate_age(age))

    user = {
        "name": name,
        "email": validated_email,
        "age": validated_age
    }
    return Ok(user)

# バリデーション実行
user_result = create_user("田中太郎", "invalid-email", 25)
# Err("無効なメールアドレス")
```

## APIリファレンス

### Result[T, E]

基底クラス。すべてのメソッドは`Ok`と`Err`で実装されています。

#### 判定メソッド

- `is_ok() -> bool`: 成功かどうかを判定
- `is_ok_and(func: Callable[[T], bool]) -> bool`: 成功かつ条件を満たすかを判定
- `is_err() -> bool`: 失敗かどうかを判定
- `is_err_and(func: Callable[[E], bool]) -> bool`: 失敗かつ条件を満たすかを判定

#### 値取得メソッド

- `unwrap() -> T`: 成功値を取得（失敗時は例外）
- `unwrap_or(default: T) -> T`: 成功値を取得（失敗時はデフォルト値）
- `unwrap_or_else(func: Callable[[E], T]) -> T`: 成功値を取得（失敗時は関数でデフォルト値を計算）
- `unwrap_err() -> E`: エラー値を取得（成功時は例外）
- `expect(message: str) -> T`: カスタムメッセージ付きで成功値を取得
- `expect_err(message: str) -> E`: カスタムメッセージ付きでエラー値を取得

#### 変換メソッド

- `map(func: Callable[[T], R]) -> Result[R, E]`: 成功値に関数を適用
- `map_err(func: Callable[[E], R]) -> Result[T, R]`: エラー値に関数を適用
- `map_or(func: Callable[[T], R], default: R) -> R`: 成功時は関数適用、失敗時はデフォルト値
- `map_or_else(func: Callable[[T], R], default: Callable[[E], R]) -> R`: 成功時・失敗時それぞれに関数適用

#### チェーンメソッド

- `and_then(func: Callable[[T], Result[R, E]]) -> Result[R, E]`: 成功時に別のResult返却関数を適用
- `or_else(func: Callable[[E], Result[T, R]]) -> Result[T, R]`: 失敗時に別のResult返却関数を適用

#### イテレータメソッド

- `iter() -> Iterator[T]`: 成功値のイテレータ
- `iter_err() -> Iterator[E]`: エラー値のイテレータ

### デコレータとヘルパー

- `@result`: question mark operatorをサポートするデコレータ
- `question(result: Result[T, E]) -> T`: Rustの`?`演算子相当の関数

## よくある質問

### Q: なぜ例外処理ではなくResult型を使うのですか？

A: Result型には以下の利点があります：

1. **型安全性**: エラーの可能性が型レベルで表現される
2. **明示性**: 関数のシグネチャを見るだけでエラーの可能性が分かる
3. **組み合わせ易さ**: `map`, `and_then`などでエラーハンドリングロジックを組み合わせられる
4. **パフォーマンス**: 例外の投げ上げよりも軽量

### Q: 既存のコードとどう統合すればよいですか？

A: 段階的な導入を推奨します：

```python
# 既存の例外ベースの関数をResult型でラップ
def safe_divide(a: float, b: float) -> Result[float, str]:
    try:
        return Ok(old_divide_function(a, b))
    except ZeroDivisionError:
        return Err("ゼロ除算エラー")
    except Exception as e:
        return Err(str(e))
```

### Q: 非同期処理では使えますか？

A: はい。非同期関数でも同様に使用できます：

```python
async def async_fetch(url: str) -> Result[str, str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return Ok(await response.text())
    except Exception as e:
        return Err(str(e))
```

## ライセンス

MIT License

## 使用例

- [Example01](./examples/example01_basic.py)
- [Example02](./examples/example02_default.py)
- [Example03](./examples/example03_decorator.py)
