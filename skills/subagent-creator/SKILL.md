---
name: subagent-creator
description: SubAgent（エージェント定義ファイル）を対話形式で作成するためのガイド。SubAgentの設計・description設計・システムプロンプト作成・ファイル生成までの手順を提供する。Skillの方が適切な場合は判断して適切に誘導する。
---

# SubAgent Creator

Cursor環境でSubAgent（エージェント定義ファイル）を対話形式で作成するスキル。

## Step 0: Skill vs SubAgent の判断

SubAgentを作成する前に、SkillとSubAgentのどちらが適切かを判断する。

### Skillを選ぶケース

- 専門知識をコンテキストに残して参照しながら作業したい
- 処理過程も記録したい
- 決定論的な処理が必要（スクリプト実行）
- 繰り返し使うワークフローや手順を定義したい
- 例: 「〇〇の書き方で」「△△フレームワークで」

### SubAgentを選ぶケース

- タスクを委譲して結果だけ受け取りたい
- 探索結果の要約だけあれば十分
- 複数方向を同時に並列調査したい
- 処理過程を記録する必要がない
- 例: 「調べて」「探して」「比較して」「レビューして」

### 判断フロー

```
要件を分析
    ↓
処理過程を記録する必要がある？ or 専門知識をコンテキストに残したい？
    → Yes → Skill
    → No ↓
タスクを委譲して結果だけ受け取りたい？
    → Yes → SubAgent
    → No → Skill
```

もしSkillの方が適切な場合は、`skill-creator` スキルに処理を移譲する。`skills/skill-creator/SKILL.md` を読み込んでその指示に従う。

SubAgentが適切な場合は、以下の手順を続行する。

---

## SubAgentとSkillの分離（推奨パターン）

SubAgentとSkillは分離して作成することを推奨する。

```
.cursor/
├── skills/
│   └── my-task/
│       └── SKILL.md        ← ドメイン知識・手順・チェックリスト
│
└── agents/
    └── my-task.md          ← 実行方法・コンテキスト分離の設定
```

分離のメリット:
- Skillは親Agent・他のSubAgentからも利用可能（再利用性）
- 知識の更新はSkillだけ、実行方法の変更はSubAgentだけ（保守性）
- Skillを直接呼び出すことも可能（柔軟性）

SubAgentからSkillを呼び出す例:
```markdown
---
name: my-reviewer
description: コードレビューを行う専門エージェント
---

あなたはコードレビューの専門エージェントです。

## 実行手順
1. **Skillの読み込み**: `.cursor/skills/code-review/SKILL.md` を読み込む
2. Skillで定義された観点・チェックリストに従ってレビューを実行
3. 結果を出力
```

---

## SubAgent作成ワークフロー

### Step 1: 目的と役割のヒアリング

AskQuestionツールで以下を確認：

1. **SubAgentの目的**
   - どんな専門領域を担当するか
   - どんなタスクを委譲するか
   - 例: コードレビュー、ドキュメント作成、調査・探索、テスト作成

2. **自動呼び出しのトリガー**
   - ユーザーがどんな言葉を使ったときに呼び出されるべきか
   - 例:「レビューして」「調査して」「記事を書いて」

### Step 2: 設定の確認

AskQuestionツールで以下を確認：

1. **保存場所**
   - プロジェクトレベル: `.cursor/agents/` - このプロジェクトのみで使用
   - ユーザーレベル: `~/.cursor/agents/` - すべてのプロジェクトで使用

2. **使用ツールの制限**（オプション）
   - 読み取り専用: Read, Grep, Glob
   - 編集可能: Edit, Write
   - 実行可能: Bash
   - 全ツール: 制限なし（デフォルト）

### Step 3: description設計

descriptionはSubAgentの自動呼び出しの判断基準。以下のポイントで設計する。

1. 何をするかを明確に記述
2. いつ使うか（トリガー条件）を具体的に列挙
3. 積極的に呼び出したい場合は `PROACTIVELY` や `MUST BE USED` を含める
4. ユーザーが自然に使う言葉をトリガーワードとして含める

description例:
```
コードレビュー専門。PRのレビュー、コード品質チェック、セキュリティ監査時にPROACTIVELYに使用する
```

### Step 4: システムプロンプト設計

SubAgentの振る舞いを定義するMarkdown本文を作成：

1. **役割の明確化**: 「あなたは〇〇の専門家です」
2. **処理手順**: ステップバイステップのワークフロー
3. **出力形式**: 期待する出力のフォーマット
4. **注意事項**: 禁止事項、品質基準など

### Step 5: ファイル生成

以下の形式でファイルを生成：

```markdown
---
name: [subagent-name]
description: [設計したdescription]
tools: [使用可能ツール（省略時は全ツール継承）]
---

[システムプロンプト（Markdown本文）]
```

**ファイル名**: `[subagent-name].md`

**保存先**:
- プロジェクト: `.cursor/agents/[subagent-name].md`
- ユーザー: `~/.cursor/agents/[subagent-name].md`

## 実装時の注意

1. **ディレクトリ確認**: 保存先ディレクトリが存在しない場合は作成
2. **名前重複チェック**: 既存SubAgentと名前が重複しないか確認
3. **名前規則**: 小文字、ハイフン区切り、64文字以内

## ベストプラクティス

1. **1つのタスクに集中**: 各SubAgentは特定のタスクに特化させる
2. **詳細なdescription**: トリガーワードを含め、AIが委譲タイミングを判断できるように
3. **proactive言語を使用**: `PROACTIVELY` を含めると自動委譲されやすい
4. **SkillとSubAgentを分離**: ドメイン知識はSkill、実行ロジックはSubAgentに
5. **SubAgentからSkillを参照**: 再利用可能な知識はSkillとして切り出す
6. **コンテキスト消費を考慮**: 大量ファイル読み込みや長い出力を生成するタスクはSubAgentに

## トラブルシューティング

### SubAgentが見つからない
- ファイルが `.cursor/agents/` または `~/.cursor/agents/` にあるか確認
- ファイル拡張子が `.md` か確認
- YAMLフロントマターの構文が正しいか確認

### 自動委譲されない
- descriptionにトリガーワードが含まれているか確認
- `PROACTIVELY` `MUST BE USED` などの積極的な言葉を追加

## 詳細情報

- SubAgentの例とパターン: [references/examples.md](references/examples.md)
