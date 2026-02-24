# チシキ (Chishiki) — 超詳細要件定義書

## 1. プロダクト概要

- **プロダクト名**: チシキ (Chishiki)
- **一言コンセプト**: AIが知識を整理する、日本人のためのセカンドブレインアプリ
- **URL**: chishiki
- **参考元**: [Rabrain](https://www.rabrain.com/)

### ターゲットペルソナ
1. **情報収集家・田中さん（28歳・エンジニア）** — Qiita/Zennの記事を毎日大量に読むが、保存した記事を見返すことがない。検索したい時に見つからない。
2. **勉強家・佐藤さん（35歳・マーケター）** — 業界ニュースやノウハウ記事を大量にブックマークするが、情報が埋もれて活用できていない。
3. **リサーチャー・鈴木さん（24歳・大学院生）** — 論文PDFやWeb記事をリサーチ用に大量に保存。横断検索と要約で効率化したい。

### 独自の価値提案
- 保存した情報をAIが自動整理・要約・検索可能にする
- 「保存して終わり」から「保存した知識を活用する」への転換
- 日本語に最適化されたセマンティック検索とAI要約

## 2. 機能要件（全機能）

### P0: 必須機能

#### F1: ブックマーク保存
- **ユーザーストーリー**: ユーザーとしてWebページのURLを貼り付けて、タイトル・サムネイル・概要を自動取得して保存したい
- **受け入れ条件**: URL入力→メタ情報自動取得→保存→一覧表示
- **UI概要**: ダッシュボード上部に「+ 追加」ボタン、URL入力モーダル

#### F2: コレクション（フォルダ）管理
- **ユーザーストーリー**: 保存したブックマークをコレクション（フォルダ）に分類して整理したい
- **受け入れ条件**: コレクション作成・編集・削除、ブックマークの移動・複数コレクション登録
- **UI概要**: サイドバーにコレクション一覧、ドラッグ＆ドロップ対応

#### F3: AIタグ自動付与
- **ユーザーストーリー**: 保存時にAIが自動でタグを付けてくれるので、手動でタグ付けする手間が省ける
- **受け入れ条件**: 保存時にAIがコンテンツを分析→3-5個のタグを自動提案→ユーザーが承認/編集
- **UI概要**: ブックマーク詳細画面にタグバッジ、クリックで編集

#### F4: AI要約生成
- **ユーザーストーリー**: 保存した記事の要約をAIが自動生成してくれるので、全文を読まなくても内容を把握できる
- **受け入れ条件**: 保存された記事に対してAI要約を生成、3-5行の簡潔な日本語要約
- **UI概要**: ブックマーク一覧のカードに要約プレビュー、詳細画面に全要約

#### F5: 検索（キーワード＋セマンティック）
- **ユーザーストーリー**: 保存した全ブックマークを横断検索して、キーワードだけでなく意味的に関連するものも見つけたい
- **受け入れ条件**: テキスト入力→タイトル/URL/タグ/要約を検索→結果一覧表示
- **UI概要**: グローバルヘッダーに検索バー、リアルタイムサジェスト

#### F6: ダッシュボード
- **ユーザーストーリー**: 保存した知識の全体像を一覧で把握し、最近の保存や未読をすぐ確認したい
- **受け入れ条件**: 最近の保存一覧、コレクション別統計、タグクラウド、AI提案（関連記事等）
- **UI概要**: カードグリッドレイアウト、統計ウィジェット

### P1: 重要機能

#### F7: AIチャット（RAG対話）
- **ユーザーストーリー**: 保存したコンテンツについてAIに質問して、自分の知識ベースから回答を得たい
- **受け入れ条件**: チャットUI、保存コンテンツをコンテキストにしたAI回答、ソース引用
- **UI概要**: サイドパネルまたは専用ページにチャットUI

#### F8: お気に入り＆ピン留め
- **ユーザーストーリー**: よく参照するブックマークをお気に入りに登録して素早くアクセスしたい
- **受け入れ条件**: スター/ハートでお気に入り登録、お気に入り一覧フィルタ
- **UI概要**: ブックマークカードにスターアイコン

#### F9: タグフィルタリング
- **ユーザーストーリー**: 特定のタグで絞り込んで関連するブックマークだけを表示したい
- **受け入れ条件**: タグクリックでフィルタ、複数タグAND/OR切り替え
- **UI概要**: サイドバーまたはフィルタバーにタグ一覧

#### F10: インポート
- **ユーザーストーリー**: 他のブックマーク管理サービスからデータを移行したい
- **受け入れ条件**: ブラウザブックマーク(HTML)インポート対応
- **UI概要**: 設定画面にインポートセクション

### P2: 追加機能

#### F11: アーカイブ
- **ユーザーストーリー**: 不要になったブックマークを削除せずアーカイブしたい
- **受け入れ条件**: アーカイブ/復元、アーカイブ一覧
- **UI概要**: 右クリックメニューまたはスワイプでアーカイブ

#### F12: 閲覧履歴
- **ユーザーストーリー**: 最近閲覧したブックマークの履歴を確認したい
- **受け入れ条件**: 閲覧日時の記録、履歴一覧表示
- **UI概要**: サイドバーに「最近閲覧」セクション

## 3. 画面一覧

### 3.1 ランディングページ (/)
- **目的**: 未ログインユーザーへのサービス紹介
- **含まれる要素**: ヒーローセクション（キャッチコピー+CTA）、機能紹介（3カラム）、使い方ステップ、料金プラン、FAQ、フッター
- **ユーザーアクション**: サインアップ/ログイン
- **遷移先**: /sign-up, /sign-in

### 3.2 サインアップ (/sign-up)
- **目的**: 新規アカウント作成
- **含まれる要素**: Clerk SignUpコンポーネント
- **ユーザーアクション**: メール/Google/GitHub認証
- **遷移先**: /dashboard

### 3.3 サインイン (/sign-in)
- **目的**: 既存アカウントログイン
- **含まれる要素**: Clerk SignInコンポーネント
- **ユーザーアクション**: メール/Google/GitHub認証
- **遷移先**: /dashboard

### 3.4 ダッシュボード (/dashboard)
- **目的**: メインハブ。保存したブックマークの全体像
- **含まれる要素**:
  - サイドバー（コレクション一覧、タグクラウド、ナビゲーション）
  - メインエリア（統計カード: 総保存数/今週の保存数/未読数、最近のブックマーク一覧）
  - 「+ 追加」ボタン（FAB）
- **ユーザーアクション**: ブックマーク追加、コレクション切替、検索、ブックマーク閲覧
- **遷移先**: /dashboard/bookmarks/:id, /dashboard/collections/:id

### 3.5 ブックマーク一覧 (/dashboard/bookmarks)
- **目的**: 全ブックマークの一覧表示
- **含まれる要素**: 検索バー、フィルタ（タグ/コレクション/日付）、ソート、カードグリッド/リスト表示切替
- **ユーザーアクション**: フィルタリング、ソート、ブックマーク選択
- **遷移先**: /dashboard/bookmarks/:id

### 3.6 ブックマーク詳細 (/dashboard/bookmarks/:id)
- **目的**: 個別ブックマークの詳細表示
- **含まれる要素**: タイトル、URL、サムネイル、AI要約、タグ、コレクション、メモ、作成日、最終閲覧日
- **ユーザーアクション**: 要約の再生成、タグ編集、コレクション変更、メモ追加、外部リンクで開く、削除
- **遷移先**: 外部URL、/dashboard/bookmarks

### 3.7 コレクション一覧 (/dashboard/collections)
- **目的**: コレクション（フォルダ）の管理
- **含まれる要素**: コレクションカード一覧（名前、アイコン、ブックマーク数）
- **ユーザーアクション**: コレクション作成、編集、削除
- **遷移先**: /dashboard/collections/:id

### 3.8 コレクション詳細 (/dashboard/collections/:id)
- **目的**: 特定コレクション内のブックマーク一覧
- **含まれる要素**: コレクション名、説明、ブックマーク一覧
- **ユーザーアクション**: ブックマーク追加/削除、並び替え
- **遷移先**: /dashboard/bookmarks/:id

### 3.9 AI チャット (/dashboard/chat)
- **目的**: 保存した知識ベースとのAI対話
- **含まれる要素**: チャットメッセージ一覧、入力フィールド、ソース引用表示
- **ユーザーアクション**: 質問入力、回答閲覧、ソースブックマークへ遷移
- **遷移先**: /dashboard/bookmarks/:id

### 3.10 検索結果 (/dashboard/search)
- **目的**: 検索結果の表示
- **含まれる要素**: 検索バー、結果カード一覧、ハイライト
- **ユーザーアクション**: キーワード変更、結果選択
- **遷移先**: /dashboard/bookmarks/:id

### 3.11 設定 (/dashboard/settings)
- **目的**: アカウント設定
- **含まれる要素**: プロフィール編集、テーマ切替（ライト/ダーク）、インポート、エクスポート、アカウント削除
- **ユーザーアクション**: 設定変更、データインポート
- **遷移先**: -

### 3.12-3.17 必須ページ
- `/about` — サービスについて
- `/help` — ヘルプセンター
- `/terms` — 利用規約
- `/privacy` — プライバシーポリシー
- `/legal` — 特定商取引法に基づく表記
- `/status` — サービスステータス

## 4. データモデル（Convexスキーマ）

### エンティティ一覧

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // ユーザー拡張情報
  users: defineTable({
    clerkId: v.string(),
    name: v.string(),
    email: v.string(),
    imageUrl: v.optional(v.string()),
    plan: v.union(v.literal("free"), v.literal("pro")),
    bookmarkCount: v.number(),
    createdAt: v.number(),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),

  // ブックマーク
  bookmarks: defineTable({
    userId: v.id("users"),
    url: v.string(),
    title: v.string(),
    description: v.optional(v.string()),
    thumbnailUrl: v.optional(v.string()),
    siteName: v.optional(v.string()),
    favicon: v.optional(v.string()),
    aiSummary: v.optional(v.string()),
    tags: v.array(v.string()),
    isFavorite: v.boolean(),
    isArchived: v.boolean(),
    readCount: v.number(),
    lastReadAt: v.optional(v.number()),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_user_favorite", ["userId", "isFavorite"])
    .index("by_user_archived", ["userId", "isArchived"])
    .index("by_user_created", ["userId", "createdAt"]),

  // コレクション
  collections: defineTable({
    userId: v.id("users"),
    name: v.string(),
    description: v.optional(v.string()),
    icon: v.optional(v.string()),
    color: v.optional(v.string()),
    bookmarkCount: v.number(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"]),

  // ブックマーク-コレクション 中間テーブル
  bookmarkCollections: defineTable({
    bookmarkId: v.id("bookmarks"),
    collectionId: v.id("collections"),
    userId: v.id("users"),
    addedAt: v.number(),
  })
    .index("by_bookmark", ["bookmarkId"])
    .index("by_collection", ["collectionId"])
    .index("by_user", ["userId"]),

  // AIチャット履歴
  chatMessages: defineTable({
    userId: v.id("users"),
    role: v.union(v.literal("user"), v.literal("assistant")),
    content: v.string(),
    sources: v.optional(v.array(v.id("bookmarks"))),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_user_created", ["userId", "createdAt"]),

  // メモ
  notes: defineTable({
    userId: v.id("users"),
    bookmarkId: v.id("bookmarks"),
    content: v.string(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_bookmark", ["bookmarkId"])
    .index("by_user", ["userId"]),
});
```

## 5. Convex関数設計

### Queries
| 関数名 | 説明 | 認証 |
|--------|------|------|
| `bookmarks.list` | ユーザーのブックマーク一覧（ページネーション、フィルタ、ソート） | 必須 |
| `bookmarks.get` | 単一ブックマーク取得 | 必須 |
| `bookmarks.search` | キーワード検索 | 必須 |
| `bookmarks.getFavorites` | お気に入り一覧 | 必須 |
| `bookmarks.getRecent` | 最近の保存 | 必須 |
| `bookmarks.getStats` | 統計情報（総数、今週の保存数等） | 必須 |
| `collections.list` | コレクション一覧 | 必須 |
| `collections.get` | 単一コレクション取得 | 必須 |
| `collections.getBookmarks` | コレクション内ブックマーク一覧 | 必須 |
| `chatMessages.list` | チャット履歴 | 必須 |
| `notes.getByBookmark` | ブックマークのメモ取得 | 必須 |
| `users.getCurrent` | 現在のユーザー情報 | 必須 |

### Mutations
| 関数名 | 説明 | 認証 |
|--------|------|------|
| `bookmarks.create` | ブックマーク作成 | 必須 |
| `bookmarks.update` | ブックマーク更新（タグ、メモ等） | 必須 |
| `bookmarks.delete` | ブックマーク削除 | 必須 |
| `bookmarks.toggleFavorite` | お気に入りトグル | 必須 |
| `bookmarks.toggleArchive` | アーカイブトグル | 必須 |
| `bookmarks.incrementReadCount` | 閲覧回数インクリメント | 必須 |
| `collections.create` | コレクション作成 | 必須 |
| `collections.update` | コレクション更新 | 必須 |
| `collections.delete` | コレクション削除 | 必須 |
| `bookmarkCollections.add` | コレクションにブックマーク追加 | 必須 |
| `bookmarkCollections.remove` | コレクションからブックマーク削除 | 必須 |
| `chatMessages.create` | チャットメッセージ追加 | 必須 |
| `notes.create` | メモ作成 | 必須 |
| `notes.update` | メモ更新 | 必須 |
| `notes.delete` | メモ削除 | 必須 |
| `users.createOrUpdate` | ユーザー作成/更新 | 必須 |

### Actions
| 関数名 | 説明 | 認証 |
|--------|------|------|
| `bookmarks.fetchMetadata` | URL先のメタ情報取得（OGP等） | 必須 |
| `bookmarks.generateSummary` | AI要約生成 | 必須 |
| `bookmarks.generateTags` | AIタグ生成 | 必須 |
| `chat.sendMessage` | AIチャット送信＋応答生成 | 必須 |

## 6. 技術スタック

- **フロントエンド**: Next.js 15 + TypeScript + Tailwind CSS
- **UIコンポーネント**: shadcn/ui（必須）
- **チャート**: shadcn/ui Charts（ダッシュボード統計）
- **バックエンド/DB**: Convex（必須）
- **認証**: Clerk
- **フォント**: Noto Sans JP
- **アイコン**: Lucide React

## 7. 非機能要件

- **パフォーマンス**: LCP < 2.5秒、FID < 100ms
- **SEO**: 全ページにmetadata設定、構造化データ、サイトマップ
- **アクセシビリティ**: WAI-ARIA準拠、キーボードナビゲーション
- **レスポンシブ**: モバイル/タブレット/デスクトップ対応

## 8. 日本語ローカライズ仕様

- **フォント**: Noto Sans JP (400, 500, 700)
- **日付**: YYYY年MM月DD日
- **通貨**: ¥（小数点なし）
- **主要UI文言**:
  | 英語 | 日本語 |
  |------|--------|
  | Dashboard | ダッシュボード |
  | Bookmarks | ブックマーク |
  | Collections | コレクション |
  | Search | 検索 |
  | Add Bookmark | ブックマークを追加 |
  | AI Summary | AI要約 |
  | Tags | タグ |
  | Favorites | お気に入り |
  | Archive | アーカイブ |
  | Settings | 設定 |
  | AI Chat | AIチャット |
  | Sign In | ログイン |
  | Sign Up | 新規登録 |
  | Recent | 最近の保存 |
  | All | すべて |
  | Import | インポート |
  | Export | エクスポート |
  | Delete | 削除 |
  | Edit | 編集 |
  | Save | 保存 |
  | Cancel | キャンセル |

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

## 10. デザインガイドライン（実運用レベル品質）

### カラーパレット
- **メイン**: Indigo (#4F46E5) — 知性・信頼感
- **アクセント**: Amber (#F59E0B) — 温かみ・アクション
- **背景**: Slate-50 (#F8FAFC) — クリーンな白背景
- **ダーク背景**: Slate-950 (#020617) — ダークモード
- **テキスト**: Slate-900 (#0F172A) — メインテキスト
- **サブテキスト**: Slate-500 (#64748B)
- **ボーダー**: Slate-200 (#E2E8F0)
- **成功**: Emerald (#10B981)
- **エラー**: Rose (#F43F5E)

### コンポーネントスタイル
- **カード**: bg-white rounded-xl border shadow-sm hover:shadow-md transition
- **ボタン(Primary)**: bg-indigo-600 text-white rounded-lg hover:bg-indigo-700
- **入力**: border rounded-lg focus:ring-2 focus:ring-indigo-500
- **サイドバー**: 固定幅240px、bg-white/dark:bg-slate-900
- **グリッド**: 3カラム(デスクトップ)→2カラム(タブレット)→1カラム(モバイル)

### アニメーション
- ページ遷移: fade-in (150ms)
- カードホバー: scale(1.02) + shadow
- モーダル: slide-up + overlay
- ローディング: skeleton UI
