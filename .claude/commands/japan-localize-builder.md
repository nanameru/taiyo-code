# Japan Localize Builder (Claude Code版)

海外で成功しているプロダクトを発見→超詳細に分析→日本向け要件定義→Claude Codeで直接開発するワークフロー。

## 絶対ルール

1. **既存プロダクトのリソースに触らない** — 他のプロダクトのClerkアプリ、Convexプロジェクト、Vercelプロジェクト、GitHub リポジトリ等を一切変更・流用しない。**必ず新規作成する。**
2. **Clerkは毎回新規アプリ作成** — 既存のAPIキーを使い回さない。
3. **Convexも毎回新規プロジェクト** — `npx convex dev` で新規作成。既存プロジェクトに接続しない。
4. **コーディングはClaude Codeが直接行う** — Write/Edit/Bashツールを使って直接ファイルを作成・編集する。外部CLIツール（Codex CLI等）は使用しない。
5. **`any` 型の使用を絶対に禁止する** — `unknown`、具体的な型、ジェネリクスを使うこと。
6. **gitコミットメッセージは必ず日本語**で書くこと。

## Workflow Checklist

```
━━━ ステージ1: リサーチ & 分析（順次） ━━━
- [ ] Phase 0: 開発済みプロダクト確認
- [ ] Phase 1: ディープリサーチ（5件以上発見、Webアプリのみ）
- [ ] Phase 1.5: 候補アプリの実地調査（WebFetchで調査）
- [ ] Phase 2: 日本市場機会分析（スコアリング）

━━━ ステージ2: ドキュメント作成 ━━━
- [ ] Phase 3-A: ローカライズ戦略ドキュメント作成
- [ ] Phase 3-B: 超詳細要件定義書作成

━━━ ステージ3: 開発（Claude Codeが直接実装） ━━━
- [ ] Phase 4: プロジェクト作成→コード実装→完了

━━━ ステージ4: 品質保証 ━━━
- [ ] Phase 5: テスト（ビルド・起動・機能テスト）
- [ ] Phase 5.5: コード品質チェック（Biome & 型安全）
- [ ] Phase 5.7: SEO対策実装
- [ ] Phase 6: セキュリティ調査

━━━ ステージ5: デプロイ & 公開 ━━━
- [ ] Phase 7: GitHub リポジトリ作成 & プッシュ
- [ ] Phase 7.3: Convex セットアップ（自動・質問なし）
- [ ] Phase 7.5: Vercelデプロイ

━━━ ステージ5.5: 品質改善ループ ━━━
- [ ] Phase 7.8: 品質改善ループ（最低3周、実運用レベルまで）

━━━ ステージ6: Clerk認証（最終ステップ） ━━━
- [ ] Phase 8: OpenClawでClerk認証セットアップ

━━━ ステージ7: 完了 ━━━
- [ ] Phase 9: built-products.md 更新 & レポート出力
```

---

### Phase 0: 初期化 & 重複チェック

**まず現在の日時を取得:**
```bash
date '+%Y年%m月%d日 %H:%M %Z'
```

`.claude/skills/japan-localize-builder/references/built-products.md` を読み込み、同じプロダクトは作らない。機能・趣旨が異なるなら別物としてOK。

---

### Phase 1: ディープリサーチ

`.claude/skills/japan-localize-builder/references/research-sources.md` を読み込んでリサーチソースを確認。

1. **以下の指定サイトのみ**でリサーチ（WebSearch、WebFetchを活用）。一般Web検索は禁止:
   - **acquire.com** `/buyers/` — カテゴリ・収益でフィルタ
   - **Product Hunt** — 今週/今月のトレンド
   - **Indie Hackers** — 収益実証済みプロダクト
   - **Hacker News Show HN** — 新興ツール
   - **TechCrunch** — スタートアップニュース
   - **Crunchbase** — スタートアップDB
2. 各発見物を記録: 名前、URL、カテゴリ、概要、収益/トラクション、日本での面白さ
3. **最低5件**発見すること
4. **必ずWebアプリであること（Chrome拡張、モバイル専用アプリはNG）。ブラウザで完結するWebアプリのみ選定対象。**

### Phase 1.5: 候補アプリの実地調査（必須）

**トップ候補3つ**に対して、WebFetchでアクセスして調査:

1. **サイトにアクセス** — LP/トップページの内容を取得
2. **主要機能の把握** — 機能一覧、UI構成、料金体系を調査
3. **UI/UXの詳細メモ** — 以下を記録:
   - レイアウト構成（サイドバー？タブ？）
   - カラーパレット（メインカラー、アクセントカラー）
   - 特徴的なUIパターン
4. **感想・評価** — 何が良い？何が微妙？日本向けに変えるべき点は？

この調査結果を `.claude/skills/japan-localize-builder/output/<project-name>/research-notes.md` に記録。

---

### Phase 2: 日本市場機会分析

`.claude/skills/japan-localize-builder/references/japan-localization.md` を読み込んでローカライズフレームワークを確認。

各候補を以下でスコアリング（各1-5点）:
- **JP競合の有無** — WebSearchで日本語検索
- **文化的フィット** — 日本ユーザーに刺さるか
- **市場規模** — 十分な市場があるか
- **ローカライズ難易度** — 低いほど高スコア
- **独自優位性** — JP版を作る意味があるか

合計スコアでランキング。**トップ1つ**を選定。

---

### Phase 3-A: ローカライズ戦略ドキュメント

`.claude/skills/japan-localize-builder/output/<project-name>/localization-strategy.md` に書き出す:

**1. 元プロダクト完全分析**
- 全機能リスト（UI構成の記述含む）
- ビジネスモデル詳細（料金体系、課金フロー、フリーミアム構成）
- ユーザージャーニー（登録→オンボーディング→コア体験→課金→リテンション）
- 成功要因（なぜバズったか、何が刺さったか）

**2. 日本市場ギャップ分析**
- 日本の類似サービス一覧と各サービスの弱点
- 日本ユーザーの未充足ニーズ
- 文化的に変更が必要な点
- 日本ユーザーが求める追加機能

**3. ローカライズ方針**
- UI/UX変更点（レイアウト、情報密度、色彩、フォント）
- コピーライティング方針（トーン、敬語レベル、キャッチコピー案3つ以上）
- 決済手段優先順位（クレカ、コンビニ払い、PayPay、LINE Pay）
- 日本独自機能（LINE連携、日本語検索最適化等）
- 法的対応（特商法表記、プライバシーポリシー、インボイス制度）

**4. Go-to-Market戦略**
- ローンチ前（ティザー、SNS、Note記事）
- ローンチ（PR TIMES、Twitter/X拡散）
- 成長（SEO、コンテンツマーケ、コミュニティ）
- KPI（DAU/MAU、CVR、チャーン率の具体的目標値）

---

### Phase 3-B: 超詳細要件定義書

`.claude/skills/japan-localize-builder/output/<project-name>/requirements.md` に書き出す。**これが開発の設計図。**

**1. プロダクト概要**
- プロダクト名（日本向け）、一言コンセプト
- ターゲットペルソナ3つ以上
- 独自の価値提案

**2. 機能要件（全機能）**
各機能に: 機能名、ユーザーストーリー、受け入れ条件、優先度（P0/P1/P2）、UI概要

**3. 画面一覧（元アプリを完全再現）**
各画面に: 画面名、目的、含まれる要素、ユーザーアクション、画面遷移先
**ログイン/サインアップ、ダッシュボード、設定、プロフィール等すべての画面を網羅**

**4. データモデル（Convexスキーマ）**
- エンティティ一覧、各フィールド（Convex型）、リレーション
- **`convex/schema.ts` のコード例を含める**

**5. Convex関数設計**
- Queries、Mutations、Actions一覧
- 認証方式（Convex Auth / Clerk連携）

**6. 技術スタック**
- フロントエンド: Next.js 15 + TypeScript + Tailwind CSS
- **UIコンポーネント: shadcn/ui（必須）**
- **チャート: shadcn/ui Charts**
- バックエンド/DB: **Convex**（必須）
- 認証: Clerk

**7. 非機能要件**
- パフォーマンス、SEO、アクセシビリティ、レスポンシブ

**8. 日本語ローカライズ仕様**
- フォント: Noto Sans JP / BIZ UDPGothic
- 日付: YYYY年MM月DD日、通貨: ¥（小数点なし）
- 主要UI文言の日本語訳一覧

**9. 必須ページ（全プロダクト共通）**

| パス | ページ名 | 内容 |
|------|----------|------|
| `/about` | サービスについて | ミッション、主な特徴、運営者情報（木村太陽、神奈川県藤沢市藤沢本町） |
| `/help` | ヘルプセンター | よくある質問、お問い合わせ先 |
| `/terms` | 利用規約 | サービス内容、アカウント、料金と返金、禁止事項等 |
| `/privacy` | プライバシーポリシー | 収集する情報、利用目的、第三者サービス等 |
| `/legal` | 特定商取引法に基づく表記 | 販売業者、運営責任者、所在地等 |
| `/status` | サービスステータス | 各システムの稼働状況 |

**共通情報:**
- 運営者: 木村太陽
- 所在地: 神奈川県藤沢市藤沢本町
- メール: taiyo.kimura.3w@stu.hosei.ac.jp
- フッターに全ページへのリンクを配置

---

### Phase 4: Claude Codeによる直接開発

requirements.mdに基づいて、Claude Codeが直接コードを書く。

**1. プロジェクト初期化**
```bash
PROJECT_DIR=~/<project-name>
mkdir -p $PROJECT_DIR && cd $PROJECT_DIR
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm
```

**2. 依存パッケージインストール**
```bash
npx shadcn@latest init
npx shadcn@latest add button card dialog input label select table tabs sonner badge separator sheet avatar dropdown-menu popover calendar command tooltip progress textarea switch chart
npm install convex @clerk/nextjs
```

**3. Convex Provider の実装（Clerkキー未設定でもビルド可能にする）**

`src/components/providers/convex-client-provider.tsx` は以下のように実装すること:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` が未設定またはプレースホルダの場合、ClerkProviderをスキップして子要素をそのまま返す
- クライアントサイドでのみClerkProviderをマウントする（`useState` + `useEffect` でマウント制御）
- これにより、Clerkのセットアップが完了していなくてもビルド＆静的ページが正常に動作する

```tsx
// パターン:
const [mounted, setMounted] = useState(false);
useEffect(() => { setMounted(true); }, []);

if (!mounted || !isValidClerkKey(clerkPubKey)) {
  return <>{children}</>;
}

// ClerkProvider + ConvexProviderWithClerk でラップ
```

**4. ダッシュボードのSSR対応**
- `src/app/dashboard/layout.tsx` はServer Componentにして `export const dynamic = "force-dynamic"` を設定
- サイドバー等のClient Componentは別ファイル `src/components/dashboard-shell.tsx` に分離
- `UserButton` (Clerk) は `dynamic(() => import("@clerk/nextjs").then(...), { ssr: false })` で読み込む

**5. コード実装（Claude Codeが直接書く）**
Write/Editツールで以下を順に実装:
1. Convexスキーマ (`convex/schema.ts`)
2. Convex関数 (`convex/` 内のqueries/mutations/actions)
3. `convex/convex.config.ts` — `import { defineApp } from "convex/server"; const app = defineApp(); export default app;`
4. レイアウト (`src/app/layout.tsx`) — Noto Sans JP、Provider
5. 全ページ実装 (`src/app/` 配下)
6. コンポーネント (`src/components/` 配下)
7. 必須ページ6つ (about/help/terms/privacy/legal/status)
8. SEO設定 (metadata, sitemap, robots)

**6. 実装ルール**
- shadcn/uiコンポーネントを最大活用
- `any` 型は絶対使わない
- Server Componentsを最大活用（`"use client"` は最小限）
- 元アプリのUI/UXを可能な限り完全再現
- 全テキスト日本語

---

### Phase 5: テスト

**1. ビルドテスト**
```bash
cd ~/<project-name>
npm run build
```

**2. 起動テスト**
```bash
npm run dev
```

**3. 機能テスト**
- WebFetchで各ページにアクセスして表示確認
- TypeScriptエラーがゼロであること
- コンソールエラーがないこと

**4. 修正ループ**
- 問題発見 → 直接修正 → 再テスト → 全パスまで繰り返し

---

### Phase 5.5: コード品質チェック

**1. Biomeセットアップ & 実行**
```bash
npx @biomejs/biome init
npx @biomejs/biome check --write .
```

**2. any型の完全排除**
```bash
grep -rn ': any' --include='*.ts' --include='*.tsx' src/
grep -rn 'as any' --include='*.ts' --include='*.tsx' src/
```
**`any` が1つでもあれば直接修正。全ファイルで `any` ゼロになるまで繰り返す。**

**3. TypeScript strict チェック**
- `tsconfig.json` の `strict: true` を確認
- `npm run build` でエラーゼロ

---

### Phase 5.7: SEO対策実装

**1. メタデータ（Next.js Metadata API）**
- `app/layout.tsx` にグローバルメタデータ設定
- 各ページに個別metadata
- OGP設定 (locale: `ja_JP`)

**2. 構造化データ（JSON-LD）**
- トップページに `Organization` または `WebApplication` スキーマ

**3. 技術的SEO**
- `app/sitemap.ts` — 動的サイトマップ
- `app/robots.ts` — robots.txt
- `next.config.ts` でセキュリティヘッダー
- `next/image` でWebP自動変換
- セマンティックHTML

**4. 日本語SEO**
- `<html lang="ja">`
- ページタイトルに主要キーワード
- description は自然な日本語

---

### Phase 6: セキュリティ調査

**1. 依存パッケージ脆弱性**
```bash
npm audit
```

**2. 環境変数漏洩チェック**
- `.env` が `.gitignore` に含まれているか
- ハードコードされたシークレットがないか

**3. 認証・認可の確認**
- 未認証ユーザーのアクセス制限
- API/Convex関数の認証チェック

**4. 入力バリデーション**
- XSS対策
- `dangerouslySetInnerHTML` の不正使用チェック

---

### Phase 7: GitHub リポジトリ作成 & プッシュ

```bash
cd ~/<project-name>
gh repo create <project-name> --public --source=. --remote=origin
git add -A
git commit -m "初回リリース: <プロダクト名日本語>"
git push -u origin main
```

---

### Phase 7.3: Convex セットアップ（自動・質問なし）

**⚡ ユーザーに一切質問せず、自動で完了させること。**

**1. チームslugの自動取得**
既存のConvexプロジェクトの `.env.local` から `CONVEX_DEPLOYMENT` の `team:` コメントを読み取ってチームslugを取得する:

```bash
# 既存プロジェクトからチームslugを検索
find ~/ -maxdepth 3 -name ".env.local" -exec grep -l "CONVEX_DEPLOYMENT" {} \; 2>/dev/null | head -1 | xargs grep "team:" | head -1
```

コメント部分から `team: <slug>` を抽出する（例: `team: 4869nanataitai` → slug は `4869nanataitai`）。

**2. Convexプロジェクト作成 & デプロイ**
```bash
cd ~/<project-name>
npx convex dev --once --configure=new --team <team-slug> --project <project-name>
```

このコマンドで:
- 新規Convexプロジェクトが作成される
- `.env.local` に `NEXT_PUBLIC_CONVEX_URL` と `CONVEX_DEPLOYMENT` が自動書き込みされる
- スキーマと全Convex関数がデプロイされる

**3. デプロイ確認**
```bash
npx convex dev --once
```
エラーが出ないことを確認。

**重要: このフェーズでユーザーに質問は一切しない。自動取得・自動実行する。**

---

### Phase 7.5: Vercelデプロイ

```bash
npx vercel --yes
npx vercel --prod
```

- 環境変数設定（Convex URL）
- デプロイ完了後、本番URLで表示確認
- **注意: この時点ではClerkの認証はまだ設定されていない。認証が必要なページ以外が正常に表示されることを確認する。**

---

### Phase 7.8: 品質改善ループ（最大20周）

```
┌─────────────────────────────────────────┐
│  改善ループ（1周 = 以下の全ステップ）     │
│                                         │
│  1. 本番URLをWebFetchで全画面確認       │
│  2. 問題リスト作成                       │
│  3. Claude Codeで直接修正               │
│  4. git commit & push                   │
│  5. 問題が残っていれば → 1に戻る         │
│                                         │
│  問題ゼロになったら → Phase 8へ          │
└─────────────────────────────────────────┘
```

**各周で確認する観点:**

周回1: 基本動作 & UI品質
- 全ページアクセス可、リンク正常、レイアウト崩れなし
- Noto Sans JP統一、必須ページ6つ存在、フッターリンク

周回2: 機能 & UX品質
- ランディングページ→料金→必須ページ全フロー
- ローディング状態、エラー表示、レスポンシブ

周回3+: 本番品質 & セルフ改善
- OGP、サイトマップ、robots.txt、読み込み速度
- UX改善、デザイン改善、コピーライティング改善

**終了条件:** 自分が実際にユーザーとして使いたいと思えるレベル（認証フロー以外）

---

### Phase 8: Claude CodeからOpenClawへClerk認証セットアップを委譲（自動実行）

**⚡ Claude CodeのターミナルからOpenClaw CLIを直接呼び出してClerk認証を自動セットアップする。ユーザーに手動操作を求めない。**

Clerk認証のセットアップには、Clerkダッシュボードでのブラウザ操作（アプリ作成、APIキー取得）が必要。OpenClawはブラウザツールを持っているため、`openclaw agent`コマンドで委譲する。

**1. OpenClawのGateway稼働確認**
```bash
openclaw status
```
Gatewayが `reachable` であることを確認。もし起動していなければ:
```bash
openclaw gateway &
```

**2. OpenClawのclerk-auth-componentスキル確認**
```bash
openclaw skills list | grep clerk
```
`clerk-auth-component` が `ready` であることを確認。

**3. OpenClawにClerk認証タスクを送信**
```bash
openclaw agent --agent main --session-id "agent:main:main" \
  --message "clerk-auth-componentスキルを使って、~/<project-name> プロジェクトにClerk認証をセットアップしてください。

やるべきこと:
1. Clerkダッシュボード(https://dashboard.clerk.com)でブラウザを使って新しいアプリ「<project-name>」を作成
2. APIキー(NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY と CLERK_SECRET_KEY)を取得
3. ~/<project-name>/.env.local を更新(既存のplaceholderを実際のキーに置換)
4. Convex環境変数にもClerk Issuer URLを設定
5. サインイン・サインアップの動作確認

Convex情報:
- プロジェクト: <project-name>
- Team: <team-slug>
- Deployment: <deployment-name>

重要: ブラウザツールを使ってClerkダッシュボードにアクセスし、新しいアプリを作成してください。" \
  --timeout 600
```

**4. .env.localの更新確認**
OpenClawの応答後、実際にキーが更新されたか確認:
```bash
cat ~/<project-name>/.env.local
```
`pk_test_placeholder` が実際のキー（`pk_test_...` または `pk_live_...`）に変わっていることを確認。

**5. Vercel環境変数の更新**
Clerk APIキーをVercel環境変数にも反映:
```bash
# 既存のプレースホルダーを削除して新しいキーを設定
npx vercel env rm NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY production -y
npx vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY production <<< "<actual-key>"
npx vercel env rm CLERK_SECRET_KEY production -y
npx vercel env add CLERK_SECRET_KEY production <<< "<actual-key>"
```

**6. 再デプロイ**
```bash
npx vercel --prod --force
```

**7. サインインページの動作確認**
WebFetchで `/sign-in` ページにアクセスし、Clerkのサインインフォームが表示されることを確認。

**重要: このフェーズでユーザーに手動操作を求めない。Claude CodeがOpenClaw CLIを直接呼び出して全自動で実行する。**

---

### Phase 9: 完了処理

1. `.claude/skills/japan-localize-builder/references/built-products.md` にプロダクト情報を追記
2. レポート出力:

```markdown
# 海外トレンド → 日本ローカライズ レポート

## リサーチ結果
| # | Name | Category | Revenue | JP Competition | Score |
|---|------|----------|---------|----------------|-------|

## 選定プロダクト詳細分析
### [Product Name]
- **参考元アプリ**: [元アプリ名](URL)
- **概要**: ...
- **なぜ日本で成功できるか**: ...

## 開発成果物
- **プロジェクトパス**: ~/<name>
- **GitHub**: https://github.com/<user>/<repo>
- **Vercel本番URL**: https://<name>.vercel.app
- **Clerk認証**: OpenClawの `clerk-auth-component` スキルで設定（Phase 8参照）
```
