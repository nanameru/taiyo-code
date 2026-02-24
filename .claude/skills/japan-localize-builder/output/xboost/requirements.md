# XBoost（エックスブースト）超詳細要件定義書

## 1. プロダクト概要

- **プロダクト名**: エックスブースト（XBoost）
- **一言コンセプト**: 日本のXクリエイターのための、AI搭載オールインワン成長プラットフォーム
- **URL構想**: xboost-jp.vercel.app

### ターゲットペルソナ

**ペルソナ1: インフルエンサー志望の会社員（田中さん・28歳）**
- 副業としてXで情報発信を始めた
- フォロワー500人→5,000人を目指している
- どんな投稿がバズるか分からず試行錯誤中
- 月額1,000円程度なら投資できる

**ペルソナ2: フリーランスマーケター（鈴木さん・35歳）**
- クライアントのSNS運用を代行
- 複数アカウントの分析レポートを効率化したい
- 競合分析やトレンド把握に時間がかかっている
- 業務効率化のためなら月額3,000円は出せる

**ペルソナ3: スタートアップCEO（高橋さん・32歳）**
- 自社プロダクトの認知拡大にXを活用
- 技術系ツイートでリードジェネレーション
- エンゲージメント分析で戦略を改善したい
- ROIが見えれば月額5,000円でもOK

### 独自の価値提案
「日本語AI × X分析 × 投稿自動化」を1つのプラットフォームで実現。SocialDogにはないAI機能、海外ツールにはない日本語ネイティブ対応。

## 2. 機能要件

### P0（必須・MVP）

| # | 機能名 | ユーザーストーリー | 受け入れ条件 | UI概要 |
|---|--------|-------------------|-------------|--------|
| F1 | ダッシュボード | ユーザーとして、Xアカウントの成長状況を一目で把握したい | フォロワー数推移、エンゲージメント率、今週の投稿数が表示される | カードグリッド + ミニチャート |
| F2 | フォロワー分析 | ユーザーとして、フォロワーの増減を日/週/月で確認したい | 折れ線グラフで推移表示、増減数とパーセンテージ表示 | 折れ線グラフ + 数値サマリー |
| F3 | 投稿分析 | ユーザーとして、各投稿のパフォーマンスを比較したい | いいね、RT、リプライ、インプレッション数を投稿別に表示 | テーブル + ソート機能 |
| F4 | エンゲージメント分析 | ユーザーとして、エンゲージメント率の推移を見たい | 日/週/月のエンゲージメント率グラフ | 折れ線グラフ |
| F5 | AIコンテンツ生成 | ユーザーとして、AIに投稿案を作ってもらいたい | トピック入力→3つの投稿案を生成→編集→投稿 | チャット型UI + プレビュー |
| F6 | バイラル投稿発見 | ユーザーとして、バズっている投稿を参考にしたい | カテゴリ別のバズ投稿一覧、エンゲージメント分析付き | カードフィード |
| F7 | 投稿スケジューラー | ユーザーとして、投稿を事前にスケジュールしたい | 日時指定で投稿予約、カレンダー表示 | カレンダー + 投稿キュー |
| F8 | ゴールデンタイム分析 | ユーザーとして、最適な投稿時間を知りたい | フォロワーのアクティブ時間帯をヒートマップ表示 | ヒートマップ |
| F9 | 認証（Clerk） | ユーザーとして、安全にログインしたい | メール/Google/Xでサインアップ・ログイン | Clerkコンポーネント |

### P1（重要）

| # | 機能名 | ユーザーストーリー | 受け入れ条件 | UI概要 |
|---|--------|-------------------|-------------|--------|
| F10 | AIリライト | ユーザーとして、自分の投稿をAIで改善したい | 投稿テキスト入力→トーン選択→リライト案3つ | エディター + トーンセレクター |
| F11 | ハッシュタグ分析 | ユーザーとして、効果的なハッシュタグを知りたい | トレンドハッシュタグ表示、推奨ハッシュタグ提案 | タグクラウド + リスト |
| F12 | スレッドコンポーザー | ユーザーとして、スレッドを効率的に作成したい | 複数投稿を連続入力→プレビュー→スケジュール/投稿 | ステップ型エディター |
| F13 | 設定ページ | ユーザーとして、アカウント設定を管理したい | プロフィール編集、通知設定、プラン管理 | フォーム型 |

### P2（あると嬉しい）

| # | 機能名 | ユーザーストーリー | 受け入れ条件 | UI概要 |
|---|--------|-------------------|-------------|--------|
| F14 | アルゴリズムシミュレーター | ユーザーとして、投稿前にパフォーマンスを予測したい | 投稿テキスト入力→予測スコア表示 | スコアゲージ + アドバイス |
| F15 | 競合分析 | ユーザーとして、競合アカウントと比較したい | 相手のハンドル入力→フォロワー/エンゲージメント比較 | 比較チャート |
| F16 | レポート出力 | ユーザーとして、月次レポートをダウンロードしたい | PDF/CSV形式でダウンロード | ボタン + プレビュー |

## 3. 画面一覧

### 公開ページ（未認証）

| 画面名 | パス | 目的 | 含まれる要素 | 主なアクション |
|--------|------|------|-------------|---------------|
| ランディングページ | `/` | サービス紹介、CTA | ヒーロー、機能紹介、料金、CTA、テスティモニアル | サインアップ |
| 料金ページ | `/pricing` | 料金プラン詳細 | プラン比較テーブル、FAQ | プラン選択 |
| サインイン | `/sign-in` | ログイン | Clerkサインインフォーム | ログイン |
| サインアップ | `/sign-up` | 新規登録 | Clerkサインアップフォーム | 登録 |
| サービスについて | `/about` | ミッション・運営情報 | ミッション、特徴、運営者情報 | - |
| ヘルプ | `/help` | FAQ・お問い合わせ | よくある質問、お問い合わせフォーム | 質問検索、メール送信 |
| 利用規約 | `/terms` | 利用規約 | 規約テキスト | - |
| プライバシーポリシー | `/privacy` | 個人情報保護方針 | ポリシーテキスト | - |
| 特商法表記 | `/legal` | 特定商取引法表記 | 法定表記 | - |
| ステータス | `/status` | サービス稼働状況 | システム別ステータス | - |

### 認証済みページ（アプリ内）

| 画面名 | パス | 目的 | 含まれる要素 | 主なアクション |
|--------|------|------|-------------|---------------|
| ダッシュボード | `/dashboard` | アカウント概要 | KPIカード、ミニチャート、直近の投稿 | 各セクションへ遷移 |
| フォロワー分析 | `/dashboard/followers` | フォロワー推移 | 折れ線グラフ、数値サマリー、期間選択 | 期間切替 |
| 投稿分析 | `/dashboard/posts` | 投稿パフォーマンス | テーブル、ソート、フィルター | ソート、詳細表示 |
| エンゲージメント | `/dashboard/engagement` | エンゲージメント分析 | 折れ線グラフ、エンゲージメント率 | 期間切替 |
| ゴールデンタイム | `/dashboard/best-times` | 最適投稿時間 | ヒートマップ、推奨時間帯 | - |
| AIコンテンツ生成 | `/dashboard/ai-generate` | AI投稿作成 | トピック入力、トーン選択、生成結果 | 生成、編集、コピー |
| AIリライト | `/dashboard/ai-rewrite` | 投稿改善 | テキスト入力、トーン選択、リライト結果 | リライト、採用 |
| バイラル発見 | `/dashboard/viral` | バズ投稿発見 | カテゴリフィルター、バズ投稿カード | カテゴリ切替、詳細表示 |
| ハッシュタグ | `/dashboard/hashtags` | ハッシュタグ分析 | タグクラウド、トレンドリスト | コピー |
| スケジューラー | `/dashboard/scheduler` | 投稿予約 | カレンダー、投稿キュー、新規作成 | 予約、編集、削除 |
| 設定 | `/dashboard/settings` | アカウント設定 | プロフィール、通知、プラン | 保存 |

## 4. データモデル（Convexスキーマ）

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // ユーザープロフィール
  users: defineTable({
    clerkId: v.string(),
    name: v.string(),
    email: v.string(),
    imageUrl: v.optional(v.string()),
    xHandle: v.optional(v.string()),
    plan: v.union(v.literal("free"), v.literal("pro"), v.literal("business")),
    onboardingCompleted: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),

  // フォロワー推移データ
  followerSnapshots: defineTable({
    userId: v.id("users"),
    count: v.number(),
    change: v.number(), // 前日比
    date: v.string(), // YYYY-MM-DD
    createdAt: v.number(),
  })
    .index("by_user_date", ["userId", "date"])
    .index("by_user", ["userId"]),

  // 投稿データ
  posts: defineTable({
    userId: v.id("users"),
    xPostId: v.optional(v.string()),
    content: v.string(),
    mediaType: v.optional(v.union(v.literal("image"), v.literal("video"), v.literal("none"))),
    likes: v.number(),
    retweets: v.number(),
    replies: v.number(),
    impressions: v.number(),
    engagementRate: v.number(),
    postedAt: v.number(),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_user_engagement", ["userId", "engagementRate"]),

  // スケジュール済み投稿
  scheduledPosts: defineTable({
    userId: v.id("users"),
    content: v.string(),
    scheduledAt: v.number(),
    status: v.union(v.literal("pending"), v.literal("posted"), v.literal("failed"), v.literal("cancelled")),
    isThread: v.boolean(),
    threadParts: v.optional(v.array(v.string())),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_user_status", ["userId", "status"])
    .index("by_scheduled_at", ["scheduledAt"]),

  // AI生成コンテンツ履歴
  aiGenerations: defineTable({
    userId: v.id("users"),
    type: v.union(v.literal("generate"), v.literal("rewrite")),
    input: v.string(),
    tone: v.string(),
    results: v.array(v.string()),
    selectedIndex: v.optional(v.number()),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"]),

  // バイラル投稿キャッシュ
  viralPosts: defineTable({
    category: v.string(),
    authorHandle: v.string(),
    authorName: v.string(),
    content: v.string(),
    likes: v.number(),
    retweets: v.number(),
    replies: v.number(),
    impressions: v.number(),
    postedAt: v.number(),
    fetchedAt: v.number(),
  })
    .index("by_category", ["category"])
    .index("by_likes", ["likes"]),

  // ハッシュタグ分析
  hashtags: defineTable({
    tag: v.string(),
    category: v.string(),
    tweetCount: v.number(),
    trendScore: v.number(),
    fetchedAt: v.number(),
  })
    .index("by_category", ["category"])
    .index("by_trend_score", ["trendScore"]),

  // ゴールデンタイムデータ
  bestTimes: defineTable({
    userId: v.id("users"),
    dayOfWeek: v.number(), // 0=日, 1=月, ... 6=土
    hour: v.number(), // 0-23
    engagementScore: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"]),

  // ユーザー設定
  userSettings: defineTable({
    userId: v.id("users"),
    notifyDailyReport: v.boolean(),
    notifyWeeklyReport: v.boolean(),
    notifyViralTrend: v.boolean(),
    defaultTone: v.string(),
    timezone: v.string(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"]),
});
```

## 5. Convex関数設計

### Queries
| 関数名 | 引数 | 戻り値 | 認証 | 説明 |
|--------|------|--------|------|------|
| `users.getMe` | - | User | ✅ | 現在のユーザー取得 |
| `followerSnapshots.getByUser` | userId, period | Snapshot[] | ✅ | フォロワー推移取得 |
| `posts.getByUser` | userId, limit, sort | Post[] | ✅ | 投稿一覧取得 |
| `posts.getTopPosts` | userId, limit | Post[] | ✅ | トップ投稿取得 |
| `scheduledPosts.getByUser` | userId | ScheduledPost[] | ✅ | スケジュール投稿取得 |
| `aiGenerations.getByUser` | userId, limit | Generation[] | ✅ | AI生成履歴取得 |
| `viralPosts.getByCategory` | category, limit | ViralPost[] | ✅ | バイラル投稿取得 |
| `hashtags.getTrending` | category, limit | Hashtag[] | ✅ | トレンドハッシュタグ取得 |
| `bestTimes.getByUser` | userId | BestTime[] | ✅ | ゴールデンタイム取得 |
| `userSettings.get` | userId | Settings | ✅ | ユーザー設定取得 |
| `dashboard.getSummary` | userId | DashboardData | ✅ | ダッシュボードサマリー |

### Mutations
| 関数名 | 引数 | 戻り値 | 認証 | 説明 |
|--------|------|--------|------|------|
| `users.create` | clerkId, name, email | Id | ✅ | ユーザー作成 |
| `users.update` | userId, fields | void | ✅ | ユーザー更新 |
| `scheduledPosts.create` | content, scheduledAt, isThread | Id | ✅ | 予約投稿作成 |
| `scheduledPosts.update` | id, fields | void | ✅ | 予約投稿更新 |
| `scheduledPosts.cancel` | id | void | ✅ | 予約投稿キャンセル |
| `aiGenerations.save` | type, input, tone, results | Id | ✅ | AI生成結果保存 |
| `userSettings.update` | userId, fields | void | ✅ | 設定更新 |
| `posts.seed` | userId, posts | void | ✅ | デモデータ投入 |
| `followerSnapshots.seed` | userId, snapshots | void | ✅ | デモスナップショット投入 |

### Actions
| 関数名 | 引数 | 戻り値 | 認証 | 説明 |
|--------|------|--------|------|------|
| `ai.generateContent` | topic, tone, count | string[] | ✅ | AIコンテンツ生成 |
| `ai.rewriteContent` | text, tone | string[] | ✅ | AIリライト |
| `ai.predictEngagement` | text | PredictionResult | ✅ | エンゲージメント予測 |

## 6. 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | Next.js 15 + TypeScript + Tailwind CSS |
| UIコンポーネント | **shadcn/ui**（必須） |
| チャート | **shadcn/ui Charts**（Recharts ベース） |
| バックエンド/DB | **Convex** |
| 認証 | **Clerk** |
| AIプロバイダー | OpenAI API (GPT-4) |
| デプロイ | Vercel |
| フォント | Noto Sans JP |

## 7. 非機能要件

- **パフォーマンス**: LCP < 2.5秒、FID < 100ms
- **SEO**: Core Web Vitals グリーン
- **アクセシビリティ**: WCAG 2.1 AA準拠
- **レスポンシブ**: モバイル(375px)〜デスクトップ(1440px)

## 8. 日本語ローカライズ仕様

- **フォント**: Noto Sans JP（ウェイト: 400, 500, 600, 700）
- **日付**: YYYY年MM月DD日
- **通貨**: ¥（小数点なし）
- **数値**: 3桁カンマ区切り（1,234,567）

### 主要UI文言

| 英語 | 日本語 |
|------|--------|
| Dashboard | ダッシュボード |
| Followers | フォロワー |
| Posts | 投稿 |
| Engagement | エンゲージメント |
| Best Times | ゴールデンタイム |
| AI Generate | AI生成 |
| AI Rewrite | AIリライト |
| Viral | バイラル |
| Hashtags | ハッシュタグ |
| Scheduler | スケジューラー |
| Settings | 設定 |
| Sign In | ログイン |
| Sign Up | 新規登録 |
| Upgrade | アップグレード |
| Free Plan | 無料プラン |
| Pro Plan | プロプラン |
| Business Plan | ビジネスプラン |

## 9. 必須ページ

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
