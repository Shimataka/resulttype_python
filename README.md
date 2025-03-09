# pyresults

`PyResults` は、Rustの `Result` 型に似たPythonの型です。

## 特徴

- エラーハンドリングのための型を提供
- エラーを伝播するためのデコレータを提供
- エラーをデフォルト値で処理するための関数を提供
- エラーをマッピングするための関数を提供

## インストール

- pip非対応
- GitHubリポジトリからインストールする場合は、以下のコマンドを実行してください。

```bash
pip install git+https://github.com/Shimataka/pyresults.git
```

## 使用例

### 基本的な使用例

[example01_basic.py](examples/example01_basic.py) を参考。

```python
from pyresults import Ok, Err, Result, result, question

def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Err("ゼロ除算エラー")
    return Ok(a / b)

result1 = divide(10, 2)
if result1.is_ok():
    print(result1.unwrap())  # 5.0

result2 = divide(10, 0)
if result2.is_err():
    print(result2.unwrap_err())  # "ゼロ除算エラー"
```
