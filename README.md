# Sequential image downloader
画像まとめサイトの画像を上から順にダウンロードして保存する

# インストール
```
$ git clone git@github.com:KerorinNorthFox/sequential-image-downloader.git
$ cd sequential-image-downloader
$ python -m pip install -r requirements.txt
```

## 実行環境
```
Windows 11
python >= 3.11.3
```

# ディレクトリ構造
```
sequential-image-downloader
|-requirements.txt        # 依存ライブラリが書かれたテキスト。最初にインストールする
|-save                    # ダウンロードしたコンテンツの保存先
`-src
  |-rules                 # cssセレクタなどのサイト別のルールを追加するディレクトリ
  | |-basic_rule.py       # 基本的なhtml解析や画像ダウンロードの処理が実装されたルール
  | |-id_required_rule.py # cssセレクタにuriのidが必要なルール
  | |-rule.py             # ルールの抽象クラス
  | `-rules.py            # 全てのルールのリスト
  |-image_downloader.py   # 画像ダウンロードクラス
  |-logger.py
  |-main.py
  |-uri.py                # URLの構造を表したクラス
  `-urls.txt              # ここにダウンロードしたいページを入れていく
```

# 使い方
## 0. ルールの追加
`rule`ディレクトリにダウンロード先ウェブサイト個別のルールを作る

ルールに記載する内容は
* ドメイン名
* 先頭画像のcssセレクタ
* 先頭画像のnth-childの値
* メソッドをオーバーライドして追加の個別処理

### 実装方法
`basic_rule.py`の`BasicRule`クラスまたは、id_required_rule.pyの`IdRequiredRule`クラスを継承したルールを作成する (基本的に`BasicRule`を使用。`IdRequiredRule`については後述)

クラスの命名ルールは、`"{ウェブサイトのドメイン名}+Rule"`とキャメルケースで記載する

ファイル名は、クラス名をスネークケースで記載する

#### ソースファイルとクラスの命名の例
```python
# ドメイン名 :https://example.com 
# ファイル名 :example_com_rule.py
class ExampleComRule(BasicRule):
...
```

#### 書き方
ルールの書き方は以下のテンプレートを使用
```python
from rules.basic_rule import BasicRule

class ExampleComRule(BasicRule):
    def __init__(self) -> None:
        super().__init__(
            "example.com", # ウェブサイトのドメイン
            [
                "#pictures > ul > li:nth_child(xxxx) > a > img", # 先頭画像のcssセレクタ
                "#pictures > ul > li:nth_child(xxxx) > img", # cssセレクタの種類が複数ある場合は追加
            ],
            start_nth_child_index = 1 # cssセレクタのnth-childの値 ("xxxx"の部分)
        )

    # 親クラスのメソッドをオーバーライドして処理を追加できる　
    # 使えるメソッドはbasic_rule.pyを参照
```
cssセレクタはダウンロードしたい画像のうちの一番先頭の画像から取る。

#### ルールの追加
次に、実装したルールクラスを`rules.py`の`RULES`リストに追加する。

```python
from rules.example_com_rule import ExampleComRule

RULES: list[Rule] = [
  ...,
  ExampleComRule(),
  # 下にどんどん追加していく
]
```
最初は`rules.py`を作成する必要がある。
```bash
$ touch src/rule/rules.py
```

## 1. URLをファイルに入力
ダウンロードしたいページのURLをurls.txtに入力する。

改行して指定することで複数のページの画像を一度にダウンロードできる。
### urls.txtのフォーマット
```
example.com/post/index.html
example2.com/post/0001
```

## 2.実行
`main.py`を実行する
```
$ python main.py
```
実行すると、saveフォルダに画像がダウンロードされている

また、ダウンロード完了したurlは、`urlx.txt`から自動的に削除される

ダウンロード中にエラーが発生したurlは、`urls.txt`に残る

ダウンロード中に`urls.txt`を編集する操作は行わない方がよい。

## `IdRequiredRule`について
たまに以下のような、URL末尾の数字とCSSセレクタのクラス名が対応しているウェブサイトがある。
```
URL :https://example2.com/post/114514
CSSセレクタ :#post-114514 > ul > li:nth-child(1) > img
```

この場合、URLによってCSSセレクタが毎回変わってしまうため、`IdRequiredRule`クラスでは`BasicRule`にURLからCSSセレクタを生成するコードを追加している。

以上から、このようなページの構造をしているウェブサイトのルールを作成する場合は、`IdRequiredRule`クラスを継承する必要がある。