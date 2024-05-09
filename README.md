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

5. Pythonのコンテナに入り、マイグレーションと初期データの読み込みを行います:

    ```bash
    docker-compose exec python bash
    python manage.py migrate
    python manage.py loaddata slogan_initial.json
    ```

## サンプルリクエストとレスポンス

### 類似度チェックapi

#### リクエスト

以下のURLにGETリクエストを送信します:

<http://localhost:8000/api/check_slogan/?slogan_sentence=少しずつ、確実に、全身しよう。>

#### レスポンス

```json
{
    "message": "success check slogan",
    "distances": [
        {
            "slogan": "少しずつ、確実に、全身しよう。",
            "distance": 0.96
        },
        {
            "slogan": "一歩ずつ、一緒に進もう。",
            "distance": 0.72
        },
        {
            "slogan": "決して諦めるな、ただ全身しよう。",
            "distance": 0.68
        },
        {
            "slogan": "賢故さと熱意で成功を目指そう。",
            "distance": 0.56
        },
        {
            "slogan": "夢を追いかける勇気を持ち続けよう。",
            "distance": 0.5
        },
        {
            "slogan": "変化を恐れずに、受け入れよう。",
            "distance": 0.5
        },
        {
            "slogan": "希望を持ち、行動しよう。",
            "distance": 0.4
        },
        {
            "slogan": "努力は無駄にならない。",
            "distance": 0.38
        },
        {
            "slogan": "未来は今日の選択にかかっている。",
            "distance": 0.34
        },
        {
            "slogan": "チャレンジは成長の機会である。",
            "distance": 0.26
        }
    ]
}
```

リクエストには、特定の標語（"slogan_sentence"）を指定し、類似度（"distance"）が高い順にレスポンスが返されます

### 標語登録api

#### リクエスト

以下のURLにPOSTリクエストを送信します:

<http://localhost:8000/api/save_slogan>

body

```json
{
    "sentences": 
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

リクエストのボディーに登録したい標語のリストを指定し登録します。

### 標語リスト取得api

#### リクエスト

以下のURLにGETリクエストを送信します:

<http://localhost:8000/api/get_slogan_list?select_head_date=2015-08-25&select_tail_date=2016-08-30>

#### レスポンス

```json
{
    "message": "success get slogan list",
    "slogans": [
        {
            "id": 1,
            "slogan": "未来は今日の選択にかかっている。"
        },
        {
            "id": 2,
            "slogan": "少しずつ、確実に、全身しよう。"
        },
        {
            "id": 3,
            "slogan": "努力は無駄にならない。"
        },
        {
            "id": 4,
            "slogan": "夢を追いかける勇気を持ち続けよう。"
        },
        {
            "id": 5,
            "slogan": "チャレンジは成長の機会である。"
        },
        {
            "id": 6,
            "slogan": "希望を持ち、行動しよう。"
        },
        {
            "id": 7,
            "slogan": "変化を恐れずに、受け入れよう。"
        },
        {
            "id": 8,
            "slogan": "賢故さと熱意で成功を目指そう。"
        },
        {
            "id": 9,
            "slogan": "決して諦めるな、ただ全身しよう。"
        },
        {
            "id": 10,
            "slogan": "一歩ずつ、一緒に進もう。"
        }
    ]
}
```

select_head_dateは登録日による検索開始日、select_tail_dateには終了日をYYYY-MM-DD形式で設定します。
select_head_date、select_tail_dateは共に任意です。

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

リクエストには、削除したい標語の登録idを指定します。(削除は論理削除となります。)
