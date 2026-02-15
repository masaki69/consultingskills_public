# Consulting Toolkit

コンサルティングプロジェクトの立ち上げから最終報告書の作成まで、ワークフロー全体をAIがサポートするスキル・コマンド・エージェント群。

調査プロジェクトでは、提案書の論点を軸にインタビューガイド・報告書骨子まで一貫して設計する。各スキルに品質基準が組み込まれており、AIタスクと人間タスクを明確に分離した協調型ワークフローで運用する。

---

## Skills

### プロジェクト管理

| スキル | 説明 | トリガー |
|--------|------|----------|
| [project-manager](skills/project-manager/SKILL.md) | ワークフローのオーケストレーター。状態管理・進捗追跡を行い、各ステップで適切なスキルを呼び出す | 「プロジェクトを開始」「進捗確認」「次のタスク」 |

### 調査プロジェクト

デスクリサーチとインタビューを組み合わせた調査に対応する。技術動向調査、市場調査、インタビュー中心、デューデリジェンスなど幅広いプロジェクト種類をカバーする。

| スキル | 説明 | トリガー |
|--------|------|----------|
| [interview-research-proposal](skills/interview-research-proposal/SKILL.md) | 与件情報と打ち合わせメモから調査提案書を作成 | 「提案書を作成して」「プロポーザルを作って」 |
| [interview-guide-creator](skills/interview-guide-creator/SKILL.md) | 提案書の論点に対応したインタビューガイドを作成 | 「インタビューガイドを作成して」「質問リストを作って」 |
| [interview-candidate-selector](skills/interview-candidate-selector/SKILL.md) | 候補者リストから最適なインタビュー対象者を選定・評価 | 「インタビュー対象者を選定して」「候補者を評価して」 |
| [interview-minutes-creator](skills/interview-minutes-creator/SKILL.md) | 文字起こしと質問リストから詳細なインタビュー議事録を作成 | 「インタビュー議事録を作成して」「ヒアリング内容を整理して」 |
| [report-outline-creator](skills/report-outline-creator/SKILL.md) | 提案書・調査結果から最終報告書の骨子を設計 | 「報告書骨子を作成して」「章立てを設計して」 |
| [slide-structure-designer](skills/slide-structure-designer/SKILL.md) | ソースドキュメントからスライドのページ構成をMDで設計 | 「スライド構成を設計して」「ページ構成を考えて」 |
| [research-project-workflow](skills/research-project-workflow/SKILL.md) | 3フェーズ・13ステップのワークフロー定義 | project-managerから自動呼び出し |

### ユーティリティ

| スキル | 説明 | トリガー |
|--------|------|----------|
| [desk-research](skills/desk-research/SKILL.md) | 論点・仮説に基づくデスクトップリサーチを実行し、調査レポートを出力 | 「デスクリサーチを実行して」「初期調査をして」 |
| [agent-team-playbook](skills/agent-team-playbook/SKILL.md) | Agent Teamの適否を判断し、適切なら要件書MDを生成する | 「Agent Teamで〜」「並行処理で〜」 |
| [meeting-minutes-creator](skills/meeting-minutes-creator/SKILL.md) | 会議メモから議事録を作成 | 「会議メモから議事録を作って」「打ち合わせの議事録を作成して」 |
| [docx-to-markdown-with-references](skills/docx-to-markdown-with-references/SKILL.md) | Word文書をMarkdownに変換し、参考文献を整理 | 「Wordをマークダウンに変換して」 |
| [skill-creator](skills/skill-creator/SKILL.md) | スキル作成の手順・スクリプト・リファレンスを提供する知識パッケージ。Skillが適切かSubAgentが適切かを判断し、適切な方を作成する | 「スキルを作成して」「これをスキル化して」 |
| [subagent-creator](skills/subagent-creator/SKILL.md) | SubAgent（エージェント定義）を作成するガイド。Skillが適切かSubAgentが適切かを判断し、適切な方を作成する | 「エージェントを作成して」「SubAgentを作って」 |

---

## Agents

特定の役割に特化したサブエージェント。project-managerやワークフローの各ステップから自動的に呼び出される。

| エージェント | 説明 | 呼び出しタイミング |
|-------------|------|-------------------|
| [quality-reviewer](agents/quality-reviewer.md) | 成果物の品質レビュー専門。指定された品質チェック項目＋デフォルト5軸評価（論理構造・具体性・読み手視点・整合性・網羅性）の2層で評価し、合格/条件付き合格/要修正を判定する | AIタスク完了後のレビューゲート（review_level=fullのみ） |
| [desk-researcher](agents/desk-researcher.md) | デスクトップリサーチ実行専門。WebSearch/WebFetch/Browser Useで情報を収集し、調査レポートと仮説検証シートを出力する | Step 3（初期調査）、Step 10（詳細調査） |

---

## ワークフロー

project-manager は汎用オーケストレーターとして動作し、プロジェクト種類に応じたワークフロースキルにステップ実行を委譲する。状態管理・レビューゲート・進捗追跡は project-manager が担い、各ステップの具体的な手順はワークフロースキル側に定義する。

プロジェクトの状態は3ファイルで管理する:
- **CLAUDE.md**: 静的な基本情報（クライアント名・納期・ファイル配置）。全セッションで自動ロード
- **workflow.md**: プロセス進捗（チェックリスト・成果物リンク・履歴・重要な意思決定）
- **Output/プロジェクトサマリ.md**: 知識状態（論点・仮説検証状況・リスク・主要発見事項）。プロジェクト初期化時にスケルトンを作成し、以降随時更新

与件の内容に応じて3つのパスでワークフローを決定する:

- **パスA**: 定義済みワークフローをそのまま使う
- **パスB**: 定義済みをベースにステップを追加・省略・順序変更
- **パスC**: AIが与件から新規設計する（定義済みを参照パターンとして使う）

### 定義済みワークフロー

| プロジェクト種類 | ワークフロースキル | 状態 |
|------------------|-------------------|------|
| 調査プロジェクト | [research-project-workflow](skills/research-project-workflow/SKILL.md) | 実装済み |
| コンテンツ作成 | - | 将来追加 |
| 事業計画・戦略策定 | - | 将来追加 |
| ソフトウェア開発 | - | 将来追加 |

定義済みに合わないプロジェクトでは、AIが与件を分析してカスタムワークフローを設計する。カスタムで繰り返し使ったパターンは定義済みワークフローに昇格させる。追加手順は [project-manager/SKILL.md](skills/project-manager/SKILL.md) の「新しいワークフロースキルの追加」を参照。

### 調査プロジェクトのワークフロー

3フェーズ・13ステップで構成される。技術動向調査、市場調査、インタビュー中心、デューデリジェンスに対応する。

```
Phase 0: 提案
┌────────────────────────────────────────────────────────────────┐
│  Step 1.  提案書作成 [AI]              → interview-research-proposal │
│  Step 2.  提案用スライド構成設計 [AI]   → slide-structure-designer    │
│  Step 3.  初期デスクトップ調査 [AI]     → desk-researcher             │
│  Step 4.  提案書更新 [AI]              → interview-research-proposal │
│  Step 5.  インタビューガイド作成 [AI]   → interview-guide-creator     │
│  Step 6.  報告書骨子案作成 [AI]         → report-outline-creator      │
└────────────────────────────────────────────────────────────────┘
                              ↓
Phase 1: 調査
┌────────────────────────────────────────────────────────────────┐
│  Step 7.  インタビュー対象者選定 [AI]   → interview-candidate-selector│
│  (インタビュー実施) [人間]                                           │
│  Step 8.  議事メモ作成 [AI]             → interview-minutes-creator   │
│  Step 9.  インタビューまとめ [AI]                                     │
│  Step 10. デスクリサーチ [AI]           → desk-researcher             │
└────────────────────────────────────────────────────────────────┘
                              ↓
Phase 2: 分析・とりまとめ
┌────────────────────────────────────────────────────────────────┐
│  Step 11. 統合・分析 [AI]                                            │
│  Step 12. 報告書作成 [AI]                                            │
│  Step 13. 報告用スライド構成設計 [AI]   → slide-structure-designer    │
└────────────────────────────────────────────────────────────────┘
```

各AIステップ完了後、レビューゲートを経て次へ進む。ステップごとに `review_level` が設定されており、`full` は quality-reviewer SubAgent + ユーザー確認、`light` はユーザー確認のみで進む。

---

## 使い方

### プロジェクト全体をワークフローで進める場合

1. 与件があれば `Input/` に配置しておく
2. 「プロジェクトを開始」と入力
3. プロジェクト名・クライアント名・納期・スコープを入力
4. AIが与件を分析し、ワークフローを提案:
   - 定義済みワークフローが合えばそのまま使用
   - 合わない場合はカスタム設計（既存の修正、またはゼロから設計）
5. 提案されたワークフローを確認し、承認する
6. 「次のタスク」で各ステップを順に実行（状態に応じて自動で次のアクションを提示）
7. AIステップ完了後、成果物を確認して承認または修正指示
8. 「進捗確認」で進捗をいつでも確認

### 個別スキルだけを使う場合

トリガーワードをチャットに入力する。

```
「提案書を作成して」         → interview-research-proposal が起動
「会議メモから議事録を作って」 → meeting-minutes-creator が起動
「インタビュー議事録を作成して」→ interview-minutes-creator が起動
「デスクリサーチを実行して」   → desk-research が起動
```

---

## Agent Team による並列実行

Claude Code の Agent Team は、リードエージェントが複数のチームメイトを動的に生成し、独立したタスクを並列実行する機能。各チームメイトは独立したコンテキストで動作し、共有タスクリストとメッセージでリードと連携する。

通常のワークフローはステップを順に実行するが、複数の独立した成果物を同時に作れる場面では Agent Team で処理時間を短縮できる。

### いつ使うか

以下の条件をすべて満たす場面で有効に機能する。

- 同時並列で回せる独立タスクが3つ以上ある
- 各タスクが異なるファイルを出力する（競合しない）
- 1セッション内で完結できる規模
- 逐次実行と比べて時間短縮の実益がある

いずれかを満たさない場面では、project-manager + 個別スキルによる逐次ワークフローのほうがシンプルで品質管理しやすい。

### 逐次ワークフローとの使い分け

| 場面 | 推奨 | 理由 |
|------|------|------|
| 与件受領 → 提案一式 | Agent Team | 提案書と調査を並列で作成でき、成果物が独立している |
| 文字起こしが複数溜まった場合 | Agent Team | 複数議事録 + 調査を並列で処理する。ファイル数が多いほど効果が出る |
| 報告書ドラフト + レビュー | Agent Team | 多角レビューの並列実行 |
| クライアントフィードバック反映 | 逐次 | 単一ファイル修正。並列の必要がない |
| インタビュー1件の議事録 | 逐次 | 単一タスク。チーム生成がオーバーヘッドになる |
| 分析の方向性検討 | 逐次 | 人間との対話的探索が必要 |
| スライド作成 | 逐次 | スライド制作スキルで逐次処理（別途用意） |

### 実行方法

Claude Code でプロジェクトフォルダを開き、自然言語で指示する。

```
「Agent Teamで提案を作成して」
「インタビュー結果をAgent Teamで並行処理して」
「報告書をAgent Teamで作成して」
```

AIが [agent-team-playbook](skills/agent-team-playbook/SKILL.md) を参照し、適否を判断した上で要件書MDを生成する。ユーザーが確認後、Claude Code にその内容を渡して実行する。

> Agent Team は Claude Code 固有の機能であり、Cursor では利用できない。Cursor で逐次ワークフローを進める場合は project-manager スキルを自然言語で呼び出す。

---

## 成果物の格納先

| 成果物 | パス |
|--------|------|
| プロジェクトサマリ | `Output/プロジェクトサマリ.md` |
| 提案書 | `Output/提案書.md` |
| スライド構成（提案） | `Output/スライド構成_提案.md` |
| インタビューガイド | `Output/インタビューガイド.md` |
| インタビュー対象者 | `Output/インタビュー対象者.md` |
| 報告書骨子 | `Output/報告書骨子.md` |
| 議事録 | `Output/議事録/` |
| インタビューまとめ | `Output/インタビューまとめ.md` |
| 分析結果 | `Output/分析結果.md` |
| 最終報告書 | `Output/最終報告書.md` |
| スライド構成（報告） | `Output/スライド構成.md` |
| 進捗状況 | `workflow.md` |

---

## ディレクトリ構成

```
consulting/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── README.md
├── commands/
│   └── pm.md                                  # Cursorコマンド（project-manager起動）
├── skills/
│   ├── project-manager/
│   ├── interview-research-proposal/
│   ├── interview-guide-creator/
│   ├── interview-candidate-selector/
│   ├── interview-minutes-creator/
│   ├── research-project-workflow/     # ワークフロースキル（調査）
│   │   ├── SKILL.md
│   │   └── references/phases.md
│   │   # 新しいワークフロータイプを追加する場合、同じ構造でディレクトリを作成
│   ├── agent-team-playbook/
│   ├── desk-research/
│   ├── docx-to-markdown-with-references/
│   ├── meeting-minutes-creator/
│   ├── report-outline-creator/
│   ├── skill-creator/
│   ├── slide-structure-designer/
│   └── subagent-creator/
└── agents/
    ├── quality-reviewer.md
    └── desk-researcher.md
```

---

## インストール

このリポジトリは Claude Code Plugin として構成されている。GitHubリポジトリから直接インストールできる。

### プラグインとしてインストール

```bash
# マーケットプレイスを追加
/plugin marketplace add masaki69/consultingskills_public

# プラグインをインストール
/plugin install consultingskills_public@consultingskills_public
```

または `~/.claude/settings.json` に直接追加する。

```json
{
  "extraKnownMarketplaces": {
    "consultingskills_public": {
      "source": {
        "source": "github",
        "repo": "masaki69/consultingskills_public"
      }
    }
  },
  "enabledPlugins": {
    "consultingskills_public@consultingskills_public": true
  }
}
```

### 更新

```bash
claude plugin update consultingskills_public@consultingskills_public
```

### 動作確認

```bash
# インストール済みプラグインの一覧
claude plugin list

# プラグインのバリデーション
claude plugin validate
```

### ファイル構成

| 種類 | パス |
|------|------|
| プラグインマニフェスト | `.claude-plugin/plugin.json` |
| マーケットプレイスカタログ | `.claude-plugin/marketplace.json` |
| Skills | `skills/` |
| Commands | `commands/` |
| Agents | `agents/` |
