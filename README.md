# Connpass-RSS

connpass API を使用して、**47都道府県すべて**のイベント情報を RSS フィードとして生成するプログラムです。

## 概要

このプロジェクトは、[connpass](https://connpass.com/) の公開 API からイベント情報を取得し、都道府県ごとに個別の RSS フィード（`rss_<prefecture>.xml`）を生成します。今後開催されるイベントのみが含まれ、RSS リーダーで購読できます。

## 主な機能

- **47都道府県すべて**のイベント情報を自動取得
- 今後開催されるイベントのみをフィルタリング
- RSS 2.0 形式でフィード生成
- イベントの詳細情報を含む：
  - タイトル
  - URL
  - 開催日時
  - 開催地（会場名・住所）
  - 説明文（キャッチコピー + 本文）
  - イベント画像

## 必要要件

- Python 3.10 以上
- [uv](https://github.com/astral-sh/uv) (推奨)

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/sin471/Connpass-RSS.git
cd Connpass-RSS

# uv を使用して依存関係をインストール
uv sync
```

## 使い方

### RSS フィードの購読方法

生成された RSS フィードを RSS リーダーで購読できます。購読したいRSSフィードのxmlファイルを`rss`ディレクトリ内から選び、RawデータのURLをRSSリーダーに登録してください。

たとえば、東京のイベントのRSSフィードを購読する場合は、`rss/rss_tokyo.xml`のRawデータである https://raw.githubusercontent.com/sin471/Connpass-RSS/refs/heads/main/rss/rss_tokyo.xml のURLをRSSリーダーに登録します。

### RSS フィードの生成

```bash
uv run main.py
```

実行すると、`rss/` ディレクトリ内に47都道府県分の RSS フィードファイルが生成されます：

```
rss/rss_hokkaido.xml
rss/rss_aomori.xml
rss/rss_iwate.xml
...
rss/rss_okinawa.xml
```



## カスタマイズ

### 特定の都道府県のみ生成

`main.py` の `prefectures` リストを編集して、必要な都道府県のみに絞ることができます：

```python
prefectures = [
    ("tokyo", "東京"),
    ("osaka", "大阪"),
    ("aichi", "愛知"),
]
```

### キーワードフィルタを追加

`generate_rss_for_prefecture` 関数の呼び出し時にキーワードを指定できます：

```python
# Python 関連イベントのみ取得
generate_rss_for_prefecture("tokyo", "東京", keyword=["Python"])
```

## プロジェクト構成

```
Connpass-RSS/
├── main.py              # メインスクリプト
├── pyproject.toml       # プロジェクト設定ファイル
├── README.md            # このファイル
└── rss/                 # RSS フィード出力ディレクトリ
    ├── rss_hokkaido.xml # 北海道の RSS フィード
    ├── rss_tokyo.xml    # 東京の RSS フィード
    ├── rss_osaka.xml    # 大阪の RSS フィード
    └── ...              # その他47都道府県分
```

## 依存パッケージ

- `feedgen>=1.0.0` - RSS フィード生成
- `requests>=2.32.5` - HTTP リクエスト

## API について

このプロジェクトは [connpass API v2](https://connpass.com/about/api/) を使用しています。


## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します！バグ報告や機能要望は Issue でお知らせください。
