# 家計簿アプリ

### デプロイ

conohaのVPSにNginxでデプロイしています。

<https://kakeibo.ta2milab.com/accounts/login>

ユーザー名：demo

パスワード:  &FZbMuTfx2G1

### 主な使用ライブラリ

- Django
- Django REST Framework
- Docker

### 機能

- ユーザー認証
- 一覧表示（ソート・検索機能付き）
- 支出・収入のカテゴリ別登録
- 支出・収入のCRUD
- 月次支出/収入カテゴリ別割合
- カテゴリ別金額推移
- 家族グループ機能
- ユニットテスト
  - 少ししか書けてない
- API([ドキュメント](https://kakeibo.ta2milab.com/api/documents/))
  - JWT認証
  - swaggerでAPIドキュメントを生成した


### 開発環境構築

``` shell
# 初回起動時
$ docker-compose up --build
$ docker-compose exec web python manage.py

# 2回目以降
$ docker-compose up
```