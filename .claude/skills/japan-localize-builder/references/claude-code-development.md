# Claude Code Development Workflow

## 開発方針

Claude Codeが直接コードを書く。外部CLIツール（Codex CLI等）は使用しない。

### プロジェクト初期化
```bash
PROJECT_DIR=~/<project-name>
mkdir -p $PROJECT_DIR && cd $PROJECT_DIR
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm
```

### shadcn/ui セットアップ
```bash
npx shadcn@latest init
# 必要なコンポーネントを追加
npx shadcn@latest add button card dialog input label select table tabs toast chart
```

### Convex セットアップ
```bash
npx convex init
# スキーマ定義後
npx convex dev
```

### 推奨ディレクトリ構造
```
<project-name>/
├── convex/
│   ├── schema.ts          # データモデル定義
│   ├── auth.config.ts     # Clerk連携設定
│   ├── users.ts           # ユーザー関連関数
│   └── [entity].ts        # エンティティごとの関数
├── src/
│   ├── app/
│   │   ├── layout.tsx     # ルートレイアウト（Provider、フォント）
│   │   ├── page.tsx       # LP/トップページ
│   │   ├── about/page.tsx
│   │   ├── help/page.tsx
│   │   ├── terms/page.tsx
│   │   ├── privacy/page.tsx
│   │   ├── legal/page.tsx
│   │   ├── status/page.tsx
│   │   ├── dashboard/     # メイン機能
│   │   ├── sign-in/       # Clerk認証
│   │   └── sign-up/       # Clerk認証
│   ├── components/
│   │   ├── ui/            # shadcn/ui コンポーネント
│   │   ├── layout/        # Header, Footer, Sidebar等
│   │   └── features/      # 機能別コンポーネント
│   └── lib/
│       └── utils.ts       # ユーティリティ
├── public/
├── .env.local
├── next.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

### 実装順序
1. **基盤**: layout.tsx（Provider、フォント、メタデータ）
2. **認証**: Clerk Provider、sign-in/sign-up ページ
3. **データ**: Convex スキーマ、関数
4. **LP**: トップページ（ヒーロー、機能紹介、CTA）
5. **コア機能**: ダッシュボード、メイン機能画面
6. **補助ページ**: about, help, terms, privacy, legal, status
7. **SEO**: metadata, sitemap, robots, JSON-LD
8. **仕上げ**: レスポンシブ、アニメーション、エラー処理

### コーディング規約
- **`any` 型は絶対禁止** — `unknown`、具体的な型、ジェネリクスを使用
- **Server Components優先** — `"use client"` は最小限
- **shadcn/ui必須** — カスタムUIもshadcnのデザイントーンに合わせる
- **日本語UI** — 全テキスト日本語、Noto Sans JP
- **型安全** — strict mode、全関数に型注釈

### 技術スタック
- **SaaS/Web App**: Next.js 15 + TypeScript + Tailwind + shadcn/ui + Convex + Clerk
- **フォント**: Noto Sans JP (next/font)
- **デプロイ**: Vercel
- **CI**: GitHub + Vercel自動デプロイ
