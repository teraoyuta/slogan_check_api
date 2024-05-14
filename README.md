# 標語類似度api営業用

## インストールと実行方法

1. リポジトリをクローンします:

    ```bash
    git clone https://mads.backlog.com/git/MONOLITHSDEV/slogan_checker.git
    ```

2. docker-compose.ymlが存在するディレクトリに移動します:

    ```bash
    cd docker
    ```

3. Dockerを使用してプロジェクトをビルドします:

    ```bash
    docker-compose build --no-cache --force-rm
    ```

4. Dockerコンテナをバックグラウンドで起動します:

    ```bash
    docker-compose up -d
    ```

5. Pythonのコンテナに入り、マイグレーションを行います:

    ```bash
    docker-compose exec python bash
    python manage.py migrate
    ```

## サンプルリクエストとレスポンス

### 類似度チェックapi

#### リクエスト

以下のURLにGETリクエストを送信します:

<http://localhost:8000/api/check_slogan/?slogan_sentence=少しずつ、確実に、全身しよう。&response_limit=1>

#### レスポンス

```json
{
    "message": "success check slogan",
    "distances": [
        {
            "slogan": "少しずつ、確実に、全身しよう。",
            "distance": 1.0
        },
    ]
}
```

リクエストには、特定の標語（"slogan_sentence"）を指定し、類似度（"distance"）が高い順に上限レスポンス数(response_limit)分のレスポンスが返されます

### 標語登録api

#### リクエスト

以下のURLにPOSTリクエストを送信します:

<http://localhost:8000/api/save_slogan/>

##### リクエストbody

```json
{
    "slogan_sentences": 
    [
        "未来を創る、今日の決断。",
        "失敗は成功への階段。",
        "挑戦を受け入れ、成長を追求せよ。",
        "忍耐と情熱で、目標を達成せよ。",
        "想像力を燃やし、可能性を拓こう。",
        "変革の時代、自ら進んで変われ。",
        "信念を持ち、不可能を可能にしよう。",
        "心の強さが道を切り拓く。",
        "誠実な努力が未来を形作る。",
        "共に挑戦し、共に成長しよう。"
    ]
}
```

#### レスポンス

```json
{
    "message": "success insert slogan"
}
```

リクエストのボディーに登録したい標語のリスト(slogan_sentences)をjson形式で指定し登録します

### 標語リスト取得api

#### リクエスト

以下のURLにGETリクエストを送信します:

<http://localhost:8000/api/get_slogan_list?search_head_date=2015-08-25&search_tail_date=2016-08-30>

#### レスポンス

```json
{
    "message": "success get slogan list",
    "slogans": [
        {
            "id": 1,
            "slogan": "未来は今日の選択にかかっている。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 2,
            "slogan": "少しずつ、確実に、全身しよう。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 3,
            "slogan": "努力は無駄にならない。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 4,
            "slogan": "夢を追いかける勇気を持ち続けよう。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 5,
            "slogan": "チャレンジは成長の機会である。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 6,
            "slogan": "希望を持ち、行動しよう。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 7,
            "slogan": "変化を恐れずに、受け入れよう。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 8,
            "slogan": "賢故さと熱意で成功を目指そう。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 9,
            "slogan": "決して諦めるな、ただ全身しよう。",
            "created_at": "2016-08-25 13:30:00"
        },
        {
            "id": 10,
            "slogan": "一歩ずつ、一緒に進もう。",
            "created_at": "2016-08-25 13:30:00"
        }
    ]
}
```

検索対象開始日(search_head_date)、検索対象終了日(search_tail_date)YYYY-MM-DD形式で設定します
search_head_date、search_tail_dateは共に任意です

### 標語削除api

#### リクエスト

以下のURLにPOSTリクエストを送信します:

<http://localhost:8000/api/delete_slogan/?id=1>

#### レスポンス

```json
{
    "message": "success delete slogan id:1"
}
```

リクエストには、削除したい標語の登録ID(id)を指定します (削除は論理削除となります)

## 付録

### ひらがな文字列取得api

#### リクエスト

以下のURLにPOSTリクエストを送信します:

<http://localhost:8000/api/get_kana_from_slogan/?slogan_sentence=少しずつ、確実に、前進しよう。>

#### レスポンス

```json
{
    "message": "success get kana",
    "kana": "すこしずつ、かくじつに、ぜんしんしよう。"
}
```

リクエストには、日本語にしたい文字列(slogan_sentence)を指定します。
