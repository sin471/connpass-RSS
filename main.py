import datetime
import os

import feedgen.feed as ffeed
import requests


def add_entry(fg: ffeed.FeedGenerator, event: dict):
    """
    connpass API から取得したイベント情報を RSS エントリーとして追加する
    """
    fe = fg.add_entry()
    fe.id(event["url"])
    fe.title(event["title"])
    fe.link(href=event["url"])
    description = ""
    # 開催地情報を追加
    if event.get("place"):
        description += f"📍 会場: {event['place']}"
        if event.get("address"):
            description += f"\n住所: {event['address']}"

    # 説明文を作成（catch と description の組み合わせ）
    description += f"\n\n{event.get('catch', '')}"
    description += f"\n\n{event.get('description', '')}"
    fe.description(description)

    # 開始日時を published として設定
    if "started_at" in event:
        fe.published(event["started_at"])

    # 画像を設定（enclosure として追加）
    if event.get("image_url"):
        # feedgen では enclosure を使って画像を追加
        # RSS では enclosure は通常メディアファイル用
        # 代わりに content として設定することも可能
        fe.enclosure(event["image_url"], 0, "image/png")

    return fg


def fetch_content(keyword: list, prefecture: str) -> dict:
    """
    connpass API からイベント情報を取得する
    """
    URL = "https://connpass.com/api/v2/events/"
    API_KEY = os.getenv("CONNPASS_API_KEY", "")
    headers = {"X-API-Key": API_KEY, "User-Agent": "connpass-rss/1.0"}
    params = {"keyword": keyword, "prefecture": prefecture}

    try:
        print(f"Fetching content from {URL} with params {params}")
        response = requests.get(URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": "Failed to fetch content", "events": []}


def generate_rss_for_prefecture(prefecture_en: str, prefecture_ja: str, keyword: list = []):
    """
    指定された都道府県の RSS フィードを生成する
    """
    content = fetch_content(prefecture=prefecture_en, keyword=keyword)
    event_count = len(content.get('events', []))
    print(f"[{prefecture_ja}] 取得したイベント数: {event_count}")

    fg = ffeed.FeedGenerator()
    fg.id("https://connpass.com/explore/")
    fg.title(prefecture_ja + "のイベント")
    fg.author({"name": "connpass-rss", "email": "example@example.com"})
    fg.link(href="https://connpass.com/explore/", rel="alternate")
    fg.subtitle(prefecture_ja + "のイベント情報")
    fg.link(href="https://connpass.com/explore/", rel="self")
    fg.language("ja")
    fg.logo("https://raw.githubusercontent.com/sin471/connpass-RSS/refs/heads/main/image/connpass_logo_4.png")

    # 取得したイベントのうちこれから開催されるものをRSSエントリーとして追加
    added_count = 0
    for event in content.get("events", []):
        if event.get("started_at") > datetime.datetime.now().isoformat():
            fg = add_entry(fg, event)
            added_count += 1

    # ファイル名を都道府県名で保存
    filename = f"rss/rss_{prefecture_en}.xml"
    fg.rss_file(filename)
    print(f"[{prefecture_ja}] RSS feed generated: {filename} ({added_count} events)")
    return added_count


def main():
    # 47都道府県のリスト（英語名と日本語名）
    prefectures = [
        ("online", "オンライン"),
        ("hokkaido", "北海道"),
        ("aomori", "青森"),
        ("iwate", "岩手"),
        ("miyagi", "宮城"),
        ("akita", "秋田"),
        ("yamagata", "山形"),
        ("fukushima", "福島"),
        ("ibaraki", "茨城"),
        ("tochigi", "栃木"),
        ("gunma", "群馬"),
        ("saitama", "埼玉"),
        ("chiba", "千葉"),
        ("tokyo", "東京"),
        ("kanagawa", "神奈川"),
        ("niigata", "新潟"),
        ("toyama", "富山"),
        ("ishikawa", "石川"),
        ("fukui", "福井"),
        ("yamanashi", "山梨"),
        ("nagano", "長野"),
        ("gifu", "岐阜"),
        ("shizuoka", "静岡"),
        ("aichi", "愛知"),
        ("mie", "三重"),
        ("shiga", "滋賀"),
        ("kyoto", "京都"),
        ("osaka", "大阪"),
        ("hyogo", "兵庫"),
        ("nara", "奈良"),
        ("wakayama", "和歌山"),
        ("tottori", "鳥取"),
        ("shimane", "島根"),
        ("okayama", "岡山"),
        ("hiroshima", "広島"),
        ("yamaguchi", "山口"),
        ("tokushima", "徳島"),
        ("kagawa", "香川"),
        ("ehime", "愛媛"),
        ("kochi", "高知"),
        ("fukuoka", "福岡"),
        ("saga", "佐賀"),
        ("nagasaki", "長崎"),
        ("kumamoto", "熊本"),
        ("oita", "大分"),
        ("miyazaki", "宮崎"),
        ("kagoshima", "鹿児島"),
        ("okinawa", "沖縄"),
    ]

    print("=" * 60)
    print("47都道府県の RSS フィード生成を開始します")
    print("=" * 60)

    total_events = 0
    for prefecture_en, prefecture_ja in prefectures:
        added_count = generate_rss_for_prefecture(prefecture_en, prefecture_ja)
        total_events += added_count

    print("=" * 60)
    print("全都道府県の RSS フィード生成が完了しました")
    print(f"総イベント数: {total_events}")
    print("=" * 60)


if __name__ == "__main__":
    main()
