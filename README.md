# TOMONOWA Event Portal

GitHub Pages用の静的LPです。OpenAI、DB、サーバー、APIキーは不要です。

## GitHub Pagesで公開する手順

1. GitHubで新規リポジトリ `tomonowa-event-portal` を作成する。
2. このフォルダ内のファイルをすべてアップロードする。
3. GitHubの `Settings` → `Pages` を開く。
4. `Build and deployment` の `Source` を `Deploy from a branch` にする。
5. Branch は `main`、Folder は `/ (root)` を選び、`Save` を押す。
6. 数分後に `https://GitHubユーザー名.github.io/tomonowa-event-portal/` が公開URLになる。

独自ドメインは、GitHub Pagesの `Custom domain` にドメインを入力して、取得先のDNS設定を行えば接続できます。

## 編集場所

- 文章・日付・料金：`index.html`
- 色・余白・スマホ表示：`styles.css`
- 写真・ロゴ：`assets/`
