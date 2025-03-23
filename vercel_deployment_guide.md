# Vercelを使用した暗号通貨売買シグナル生成システムのデプロイ手順

このガイドでは、暗号通貨売買シグナル生成システムをVercelにデプロイする手順を説明します。

## 前提条件

1. GitHubアカウント
2. Vercelアカウント（GitHubアカウントでサインアップ可能）

## デプロイ手順

### 1. GitHubリポジトリの作成

1. GitHubにログインします。
2. 新しいリポジトリを作成します（例：`crypto-trading-system`）。
3. リポジトリを作成したら、以下のコマンドでローカルプロジェクトをGitHubにプッシュします：

```bash
# プロジェクトディレクトリに移動
cd /home/ubuntu/crypto_web_app

# Gitリポジトリを初期化
git init

# すべてのファイルをステージング
git add .

# コミット
git commit -m "Initial commit"

# リモートリポジトリを追加（URLは実際のリポジトリURLに置き換えてください）
git remote add origin https://github.com/yourusername/crypto-trading-system.git

# プッシュ
git push -u origin main
```

### 2. Vercelへのデプロイ

1. [Vercel](https://vercel.com/)にアクセスし、GitHubアカウントでログインします。
2. ダッシュボードから「New Project」をクリックします。
3. 「Import Git Repository」セクションで、先ほど作成したGitHubリポジトリを選択します。
4. プロジェクト設定画面で、以下の設定を確認します：
   - Framework Preset: Next.js
   - Root Directory: ./
   - Build Command: next build
   - Output Directory: .next
5. 「Environment Variables」セクションで、必要な環境変数を設定します（必要に応じて）。
6. 「Deploy」ボタンをクリックしてデプロイを開始します。

デプロイが完了すると、Vercelは自動的にプロジェクトのURLを生成します（例：`https://crypto-trading-system.vercel.app`）。

### 3. デプロイ後の確認

1. 生成されたURLにアクセスして、アプリケーションが正常に動作していることを確認します。
2. 問題がある場合は、Vercelダッシュボードの「Deployments」タブでログを確認できます。

### 4. 継続的デプロイ

Vercelは継続的デプロイをサポートしています。GitHubリポジトリに変更をプッシュすると、Vercelは自動的に新しいバージョンをデプロイします。

## 注意事項

1. **データベース**: Vercelのサーバーレス環境では、D1データベースの代わりにVercel KV（Key-Value Store）やVercel Postgres、Supabaseなどの外部データベースサービスを使用することを検討してください。

2. **環境変数**: 機密情報や設定値は環境変数として設定し、コードにハードコーディングしないでください。

3. **ビルド時間**: 大きなプロジェクトの場合、ビルド時間が長くなることがあります。Vercelの無料プランではビルド時間に制限があるため、必要に応じて有料プランへのアップグレードを検討してください。

## トラブルシューティング

1. **ビルドエラー**: ビルド時にエラーが発生した場合は、Vercelダッシュボードの「Deployments」タブでログを確認してください。

2. **依存関係の問題**: 依存関係の問題が発生した場合は、`package.json`ファイルを確認し、必要なパッケージがすべて含まれていることを確認してください。

3. **APIルートの問題**: APIルートが機能しない場合は、ファイルパスとルート構造を確認してください。

## まとめ

Vercelを使用することで、Next.jsアプリケーションを簡単にデプロイし、継続的デプロイの恩恵を受けることができます。GitHubとの統合により、コードの変更が自動的にデプロイされるため、開発ワークフローが効率化されます。
