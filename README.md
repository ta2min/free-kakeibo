# 家計簿アプリ

#### デプロイ

conohaのVPSにNginxでデプロイしています。

<https://kakeibo.ta2milab.com/accounts/login>

ユーザー名：demo

パスワード:  &FZbMuTfx2G1

#### 主な使用ライブラリ

- Django
- Django REST Framework
- Siｍple JWT

#### 機能

- ユーザー認証
- 一覧表示（ソート・検索機能付き）
- 支出・収入のカテゴリ別登録
- 支出・収入のCRUD
- 月次支出/収入カテゴリ別割合
- カテゴリ別金額推移
- ユニットテスト
  - 少ししか書けてない
- API機能
  - [ドキュメント](https://github.com/ta2min/free-kakeibo/wiki)
- JWT認証

#### 課題点・反省点

- 使ったことのないライブラリや実装したことのない機能が多く1つの機能を付けるのに時間がかかった。
- テストコードを書いたことがなくやりたいテストを書くことができなかかった
- モデルにuuidを使ってないのでAPIで他人のデータを書き換えることが簡単にできる
- APIのカテゴリ登録で、ユーザー名が必要な点
  - JWT認証しているので、そこからユーザ名を持ってくることができる。しかし、ユーザ名とカテゴリ名のユニーク制約のバリデーションよりも遅いのでエラーが出てしまう。
