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

### リクエスト

以下のURLにGETリクエストを送信します:

http://localhost:8000/slogan/?slogan_kana=すこしずつ、かくじつに、ぜんしんしよう。

### レスポンス

```json
[
    {
        "slogan_kana": "少しずつ、確実に、全身しよう。",
        "distance": 1.0
    },
    {
        "slogan_kana": "一歩ずつ、一緒に進もう。",
        "distance": 0.73
    },
    {
        "slogan_kana": "決して諦めるな、ただ全身しよう。",
        "distance": 0.68
    },
    {
        "slogan_kana": "賢故さと熱意で成功を目指そう。",
        "distance": 0.57
    },
    {
        "slogan_kana": "変化を恐れずに、受け入れよう。",
        "distance": 0.5
    },
    {
        "slogan_kana": "夢を追いかける勇気を持ち続けよう。",
        "distance": 0.48
    },
    {
        "slogan_kana": "希望を持ち、行動しよう。",
        "distance": 0.41
    },
    {
        "slogan_kana": "未来は今日の選択にかかっている。",
        "distance": 0.36
    },
    {
        "slogan_kana": "努力は無駄にならない。",
        "distance": 0.36
    },
    {
        "slogan_kana": "チャレンジは成長の機会である。",
        "distance": 0.29
    }
]
```

リクエストには、特定の標語（"slogan_kana"）をカナで指定し、類似度（"distance"）が高い順にレスポンスが返されます
