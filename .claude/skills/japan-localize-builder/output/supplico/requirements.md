# サプリコ (SuppliCo) 超詳細要件定義書

## 1. プロダクト概要

- **プロダクト名**: サプリコ (SuppliCo)
- **一言コンセプト**: AIが研究論文をもとに、あなたに最適なサプリメントを見つけるプラットフォーム
- **参考元**: [Pillser](https://pillser.com/)

### ターゲットペルソナ

1. **健康意識の高い30代女性（美容サプリ派）**
   - コラーゲン、ビタミンC、鉄分などに興味
   - 「本当に効くのか」を知りたい
   - Instagram/Xで健康情報を収集

2. **40-50代男性（生活習慣病予防派）**
   - 高血圧、コレステロール対策
   - 医師に相談しにくいが気になっている
   - エビデンスを重視する

3. **60代以上（シニア健康維持派）**
   - 関節、骨、認知機能のサプリに興味
   - 複数サプリの飲み合わせが心配
   - 使いやすいUIが必須

### 独自の価値提案
- 日本初の「AIサプリメント分析」プラットフォーム
- 中立・客観的な情報源（特定ブランドを推さない）
- 研究論文ベースのエビデンス提供
- 日本独自の制度（トクホ・機能性表示食品）に対応

---

## 2. 機能要件

### P0（必須）

| 機能名 | ユーザーストーリー | 受け入れ条件 | UI概要 |
|--------|-------------------|-------------|--------|
| サプリ検索 | ユーザーとして、サプリ名や成分名で検索して情報を見たい | 検索結果が0.5秒以内に表示 | 検索バー + オートコンプリート |
| サプリ詳細ページ | ユーザーとして、サプリの成分・効果・エビデンスを確認したい | 各サプリに詳細ページがある | タブ形式（概要/成分/研究/価格） |
| 成分データベース | ユーザーとして、特定成分の効果と研究を確認したい | 主要50成分以上のデータ | 成分詳細ページ |
| AI相談 | ユーザーとして、サプリに関する質問をAIにしたい | AIが研究ベースで回答する | チャットUI |
| カテゴリブラウジング | ユーザーとして、目的別にサプリを探したい | 10カテゴリ以上 | カテゴリカード + リスト |
| ランディングページ | 訪問者として、サービスの価値を理解したい | 3秒で価値提案が伝わる | ヒーロー + 特徴 + 統計 |
| 必須ページ6つ | ユーザーとして、運営情報を確認したい | 全6ページ存在 | 静的ページ |

### P1（重要）

| 機能名 | ユーザーストーリー | 受け入れ条件 | UI概要 |
|--------|-------------------|-------------|--------|
| パーソナライズ診断 | ユーザーとして、自分に必要なサプリを知りたい | 5問の質問で推薦 | ステップフォーム → 結果 |
| 飲み合わせチェッカー | ユーザーとして、複数サプリの相互作用を確認したい | 2つ以上のサプリを選択可 | マルチセレクト + 結果表示 |
| ブランド一覧 | ユーザーとして、ブランド別にサプリを探したい | 日本の主要10ブランド以上 | ブランドカード + 詳細 |
| 研究フィード | ユーザーとして、最新の研究論文情報を見たい | 最新順で表示 | カードフィード |
| ダッシュボード | 登録ユーザーとして、マイサプリ管理をしたい | お気に入り・履歴管理 | タブ付きダッシュボード |

### P2（あると嬉しい）

| 機能名 | ユーザーストーリー | 受け入れ条件 | UI概要 |
|--------|-------------------|-------------|--------|
| 季節別おすすめ | ユーザーとして、時期に合ったサプリを知りたい | 季節ごとに推薦変更 | バナー + カード |
| ユーザーレビュー | ユーザーとして、他ユーザーの体験談を見たい | 星評価 + テキスト | レビューリスト |
| 価格アラート | ユーザーとして、お気に入りサプリの値下げを知りたい | メール通知 | 設定画面 |

---

## 3. 画面一覧

| パス | 画面名 | 目的 | 含まれる要素 | ユーザーアクション | 遷移先 |
|------|--------|------|-------------|-------------------|--------|
| `/` | トップページ | サービス紹介・検索入口 | ヒーロー、検索バー、統計、特徴、カテゴリ、CTA | 検索、カテゴリ選択 | 検索結果、カテゴリ |
| `/search` | 検索結果 | サプリ・成分の検索結果 | フィルタ、結果リスト、ページネーション | フィルタ、詳細へ | サプリ詳細 |
| `/supplements/[id]` | サプリ詳細 | 個別サプリの情報 | 概要、成分一覧、研究エビデンス、価格比較 | 成分クリック、お気に入り | 成分詳細 |
| `/ingredients` | 成分一覧 | 全成分ブラウジング | カテゴリフィルタ、成分カード | カテゴリ選択、詳細へ | 成分詳細 |
| `/ingredients/[id]` | 成分詳細 | 個別成分の情報 | 効果、研究、推奨量、含有サプリ | サプリ選択 | サプリ詳細 |
| `/categories` | カテゴリ一覧 | 目的別ブラウジング | カテゴリカード（美容、免疫、関節等） | カテゴリ選択 | カテゴリ詳細 |
| `/categories/[slug]` | カテゴリ詳細 | カテゴリ別サプリ一覧 | サプリリスト、フィルタ | 詳細へ | サプリ詳細 |
| `/brands` | ブランド一覧 | ブランド別ブラウジング | ブランドカード（DHC, ファンケル等） | ブランド選択 | ブランド詳細 |
| `/brands/[slug]` | ブランド詳細 | ブランドのサプリ一覧 | ブランド情報、サプリリスト | 詳細へ | サプリ詳細 |
| `/ai-consultation` | AI相談 | AIにサプリ相談 | チャットUI、おすすめ質問 | 質問入力 | — |
| `/diagnosis` | パーソナライズ診断 | 自分に必要なサプリ診断 | ステップフォーム | 回答入力 | 診断結果 |
| `/diagnosis/result` | 診断結果 | 推薦サプリ表示 | 推薦リスト、根拠 | 詳細へ | サプリ詳細 |
| `/interaction-checker` | 飲み合わせチェッカー | 相互作用チェック | マルチセレクト、結果 | サプリ選択 | — |
| `/research` | 研究フィード | 最新研究論文 | カードフィード | 詳細へ | 研究詳細 |
| `/dashboard` | ダッシュボード | マイサプリ管理 | お気に入り、履歴、設定 | 管理操作 | 各詳細 |
| `/dashboard/favorites` | お気に入り | お気に入りサプリ一覧 | サプリリスト | 詳細へ | サプリ詳細 |
| `/dashboard/history` | 閲覧履歴 | 閲覧済みサプリ | 時系列リスト | 詳細へ | サプリ詳細 |
| `/dashboard/settings` | 設定 | プロフィール・通知設定 | フォーム | 保存 | — |
| `/pricing` | 料金プラン | プラン説明 | 3プラン比較 | プラン選択 | — |
| `/sign-in` | ログイン | 認証 | Clerkログインフォーム | ログイン | ダッシュボード |
| `/sign-up` | 新規登録 | 認証 | Clerk登録フォーム | 登録 | 診断 |
| `/about` | サービスについて | 運営情報 | ミッション、特徴、運営者 | — | — |
| `/help` | ヘルプ | FAQ・お問い合わせ | FAQ、連絡先 | — | — |
| `/terms` | 利用規約 | 法的文書 | 規約テキスト | — | — |
| `/privacy` | プライバシーポリシー | 法的文書 | ポリシーテキスト | — | — |
| `/legal` | 特商法表記 | 法的文書 | 表記テーブル | — | — |
| `/status` | サービスステータス | 稼働状況 | ステータス表示 | — | — |

---

## 4. データモデル（Convexスキーマ）

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // ユーザー
  users: defineTable({
    clerkId: v.string(),
    name: v.string(),
    email: v.string(),
    age: v.optional(v.number()),
    gender: v.optional(v.union(v.literal("male"), v.literal("female"), v.literal("other"))),
    healthGoals: v.optional(v.array(v.string())),
    createdAt: v.number(),
  }).index("by_clerk_id", ["clerkId"]),

  // サプリメント
  supplements: defineTable({
    name: v.string(),
    nameEn: v.optional(v.string()),
    brand: v.string(),
    brandSlug: v.string(),
    category: v.string(),
    categorySlug: v.string(),
    description: v.string(),
    imageUrl: v.optional(v.string()),
    ingredients: v.array(v.object({
      ingredientId: v.optional(v.id("ingredients")),
      name: v.string(),
      amount: v.string(),
      unit: v.string(),
    })),
    certification: v.optional(v.union(
      v.literal("tokuho"),
      v.literal("kinousei"),
      v.literal("eiyou"),
      v.literal("none")
    )),
    price: v.optional(v.number()),
    servingSize: v.optional(v.string()),
    rating: v.optional(v.number()),
    reviewCount: v.optional(v.number()),
    createdAt: v.number(),
  })
    .index("by_brand", ["brandSlug"])
    .index("by_category", ["categorySlug"])
    .searchIndex("search_name", { searchField: "name" }),

  // 成分
  ingredients: defineTable({
    name: v.string(),
    nameEn: v.optional(v.string()),
    category: v.string(),
    description: v.string(),
    benefits: v.array(v.string()),
    recommendedDosage: v.optional(v.string()),
    sideEffects: v.optional(v.array(v.string())),
    interactions: v.optional(v.array(v.string())),
    researchSummary: v.optional(v.string()),
    evidenceLevel: v.optional(v.union(
      v.literal("strong"),
      v.literal("moderate"),
      v.literal("limited"),
      v.literal("insufficient")
    )),
    createdAt: v.number(),
  })
    .searchIndex("search_name", { searchField: "name" }),

  // ブランド
  brands: defineTable({
    name: v.string(),
    slug: v.string(),
    description: v.string(),
    logoUrl: v.optional(v.string()),
    website: v.optional(v.string()),
    country: v.string(),
    supplementCount: v.number(),
    createdAt: v.number(),
  }).index("by_slug", ["slug"]),

  // カテゴリ
  categories: defineTable({
    name: v.string(),
    slug: v.string(),
    description: v.string(),
    icon: v.string(),
    supplementCount: v.number(),
    createdAt: v.number(),
  }).index("by_slug", ["slug"]),

  // 研究論文
  researchPapers: defineTable({
    title: v.string(),
    titleJa: v.optional(v.string()),
    authors: v.array(v.string()),
    journal: v.string(),
    publishedDate: v.string(),
    abstract: v.string(),
    abstractJa: v.optional(v.string()),
    url: v.optional(v.string()),
    relatedIngredients: v.array(v.string()),
    evidenceLevel: v.union(
      v.literal("strong"),
      v.literal("moderate"),
      v.literal("limited"),
      v.literal("insufficient")
    ),
    createdAt: v.number(),
  }).index("by_date", ["createdAt"]),

  // AI相談履歴
  aiConsultations: defineTable({
    userId: v.optional(v.id("users")),
    sessionId: v.string(),
    question: v.string(),
    answer: v.string(),
    relatedSupplements: v.optional(v.array(v.id("supplements"))),
    createdAt: v.number(),
  }).index("by_session", ["sessionId"]),

  // パーソナライズ診断
  diagnoses: defineTable({
    userId: v.optional(v.id("users")),
    sessionId: v.string(),
    age: v.number(),
    gender: v.string(),
    concerns: v.array(v.string()),
    lifestyle: v.array(v.string()),
    currentSupplements: v.optional(v.array(v.string())),
    recommendations: v.array(v.object({
      supplementName: v.string(),
      ingredientName: v.string(),
      reason: v.string(),
      priority: v.union(v.literal("high"), v.literal("medium"), v.literal("low")),
    })),
    createdAt: v.number(),
  }).index("by_session", ["sessionId"]),

  // お気に入り
  favorites: defineTable({
    userId: v.id("users"),
    supplementId: v.id("supplements"),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_user_supplement", ["userId", "supplementId"]),

  // 閲覧履歴
  viewHistory: defineTable({
    userId: v.optional(v.id("users")),
    sessionId: v.string(),
    supplementId: v.id("supplements"),
    viewedAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_session", ["sessionId"]),

  // 飲み合わせチェック
  interactionChecks: defineTable({
    userId: v.optional(v.id("users")),
    sessionId: v.string(),
    ingredients: v.array(v.string()),
    results: v.array(v.object({
      ingredient1: v.string(),
      ingredient2: v.string(),
      interactionType: v.union(
        v.literal("safe"),
        v.literal("caution"),
        v.literal("warning"),
        v.literal("danger")
      ),
      description: v.string(),
    })),
    createdAt: v.number(),
  }).index("by_session", ["sessionId"]),

  // ユーザー設定
  userSettings: defineTable({
    userId: v.id("users"),
    notificationsEnabled: v.boolean(),
    emailUpdates: v.boolean(),
    theme: v.union(v.literal("light"), v.literal("dark"), v.literal("system")),
    updatedAt: v.number(),
  }).index("by_user", ["userId"]),
});
```

---

## 5. Convex関数設計

### Queries
| 関数名 | ファイル | 説明 |
|--------|---------|------|
| `supplements.list` | `convex/supplements.ts` | サプリ一覧（フィルタ・ページネーション） |
| `supplements.getById` | `convex/supplements.ts` | サプリ詳細取得 |
| `supplements.search` | `convex/supplements.ts` | サプリ全文検索 |
| `supplements.getByBrand` | `convex/supplements.ts` | ブランド別サプリ一覧 |
| `supplements.getByCategory` | `convex/supplements.ts` | カテゴリ別サプリ一覧 |
| `ingredients.list` | `convex/ingredients.ts` | 成分一覧 |
| `ingredients.getById` | `convex/ingredients.ts` | 成分詳細取得 |
| `ingredients.search` | `convex/ingredients.ts` | 成分検索 |
| `brands.list` | `convex/brands.ts` | ブランド一覧 |
| `brands.getBySlug` | `convex/brands.ts` | ブランド詳細取得 |
| `categories.list` | `convex/categories.ts` | カテゴリ一覧 |
| `categories.getBySlug` | `convex/categories.ts` | カテゴリ詳細取得 |
| `researchPapers.list` | `convex/researchPapers.ts` | 研究論文一覧 |
| `favorites.list` | `convex/favorites.ts` | お気に入り一覧（認証必須） |
| `viewHistory.list` | `convex/viewHistory.ts` | 閲覧履歴一覧 |
| `users.getCurrent` | `convex/users.ts` | 現在のユーザー取得 |
| `diagnoses.getBySession` | `convex/diagnoses.ts` | セッション別診断結果 |

### Mutations
| 関数名 | ファイル | 説明 |
|--------|---------|------|
| `users.create` | `convex/users.ts` | ユーザー作成 |
| `favorites.add` | `convex/favorites.ts` | お気に入り追加 |
| `favorites.remove` | `convex/favorites.ts` | お気に入り削除 |
| `viewHistory.add` | `convex/viewHistory.ts` | 閲覧履歴追加 |
| `diagnoses.save` | `convex/diagnoses.ts` | 診断結果保存 |
| `interactionChecks.save` | `convex/interactionChecks.ts` | 飲み合わせ結果保存 |
| `userSettings.update` | `convex/userSettings.ts` | 設定更新 |

### Actions
| 関数名 | ファイル | 説明 |
|--------|---------|------|
| `ai.consult` | `convex/ai.ts` | AI相談（外部API呼び出し） |
| `supplements.seed` | `convex/seed.ts` | シードデータ投入 |

---

## 6. 技術スタック

- **フロントエンド**: Next.js 15 + TypeScript + Tailwind CSS
- **UIコンポーネント**: shadcn/ui（必須）
- **バックエンド/DB**: Convex（必須）
- **認証**: Clerk
- **フォント**: Noto Sans JP
- **アイコン**: Lucide React

---

## 7. 非機能要件

- **パフォーマンス**: LCP < 2.5秒、FID < 100ms
- **SEO**: 全ページメタデータ、サイトマップ、robots.txt
- **アクセシビリティ**: WCAG 2.1 AA準拠
- **レスポンシブ**: モバイル・タブレット・デスクトップ対応

---

## 8. 日本語ローカライズ仕様

- **フォント**: Noto Sans JP
- **日付**: YYYY年MM月DD日
- **通貨**: ¥（小数点なし）
- **lang属性**: `<html lang="ja">`

### 主要UI文言

| 英語 | 日本語 |
|------|--------|
| Search | 検索 |
| Supplements | サプリメント |
| Ingredients | 成分 |
| Brands | ブランド |
| Categories | カテゴリ |
| AI Consultation | AI相談 |
| Diagnosis | パーソナライズ診断 |
| Interaction Checker | 飲み合わせチェッカー |
| Research | 研究 |
| Dashboard | ダッシュボード |
| Favorites | お気に入り |
| History | 閲覧履歴 |
| Settings | 設定 |
| Sign In | ログイン |
| Sign Up | 新規登録 |
| Evidence Level | エビデンスレベル |
| Strong | 強い |
| Moderate | 中程度 |
| Limited | 限定的 |
| Insufficient | 不十分 |

---

## 9. 必須ページ（全プロダクト共通）

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
