---
name: research-project-workflow
description: 調査プロジェクトのワークフロー定義。3フェーズ・13ステップで構成。提案書作成から報告書作成・スライド構成設計まで、デスクリサーチとインタビューを組み合わせた調査プロジェクトを管理する。project-managerから呼び出される。
---

# 調査プロジェクト ワークフロー

調査プロジェクト（技術動向調査、市場調査、インタビュー中心、デューデリジェンス）のための3フェーズ・13ステップのワークフロー定義。

## ワークフロー概要

```
Phase 0: 提案
  1. 提案書作成 [AI] → interview-research-proposal          review_level: full
  2. 提案用スライド構成設計 [AI] → slide-structure-designer    review_level: light
  3. 初期デスクトップ調査 [AI → SubAgent] → desk-research     review_level: light
  4. 提案書更新 [AI] → interview-research-proposal          review_level: full
  5. インタビューガイド作成 [AI] → interview-guide-creator     review_level: full
  6. 最終報告書骨子案作成 [AI] → report-outline-creator       review_level: full

Phase 1: 調査
  7. インタビュー対象者選定 [AI] → interview-candidate-selector  review_level: light
  (インタビュー実施) [人間]
  8. インタビュー議事メモ作成 [AI] → interview-minutes-creator   review_level: full
  9. インタビューまとめ [AI]                                    review_level: light
  10. デスクリサーチ [AI → SubAgent] → desk-research            review_level: light

Phase 2: 分析・とりまとめ
  11. 統合・分析 [AI]                                          review_level: full
  12. 報告書作成 [AI]                                          review_level: full
  13. 報告用スライド構成設計 [AI] → slide-structure-designer      review_level: light

※ review_level: full → quality-reviewer SubAgent + ユーザー確認
※ review_level: light → ユーザー確認のみ（quality-reviewerをスキップ）
```

## プロジェクト種類

このワークフローは以下のプロジェクト種類に対応。種類により各タスクの深さ・フォーカスが変化:

| 種類 | フォーカス |
|------|------------|
| **技術動向調査** | 先端技術・プレイヤー探索、技術課題・参入障壁 |
| **市場調査** | 市場規模・セグメント、競合分析 |
| **インタビュー中心** | インタビュー設計・実施が主、定性的示唆 |
| **デューデリジェンス** | 財務・事業・技術の深掘り、リスク評価 |

## ステップ詳細

各ステップの目的・入力・出力・実行手順・品質チェックは [references/phases.md](references/phases.md) を参照。

## 連携スキル・SubAgent

| ステップ | スキル / SubAgent | 用途 |
|----------|-------------------|------|
| Step 1, 4 | `interview-research-proposal` (Skill) | 提案書作成・更新 |
| Step 2, 13 | `slide-structure-designer` (Skill) | スライド構成設計（提案用・報告用） |
| Step 3, 10 | `desk-researcher` (SubAgent) → `desk-research` (Skill) | デスクリサーチ実行（コンテキスト分離） |
| Step 5 | `interview-guide-creator` (Skill) | インタビューガイド作成 |
| Step 6 | `report-outline-creator` (Skill) | 報告書骨子作成 |
| Step 7 | `interview-candidate-selector` (Skill) | インタビュー対象者選定・評価 |
| Step 8 | `interview-minutes-creator` (Skill) | インタビュー議事録作成 |
| Step 3 | `docx-to-markdown-with-references` (Skill) | docx変換（必要時） |
| 全ステップ | `quality-reviewer` (SubAgent) | レビューゲートでの品質チェック |

### スキル呼び出し手順

**Step 1, 4（提案書作成・更新）**:
```
1. skills/interview-research-proposal/SKILL.md を読み込む
2. references/quality_playbook.md も読み込む（品質基準）
3. スキルの指示に従って提案書を作成/更新
```

**Step 2（提案用スライド構成設計）**:
```
1. skills/slide-structure-designer/SKILL.md を読み込む
2. Output/提案書.md をソースとして渡す
3. スキルの指示に従って提案用スライド構成を設計
4. Output/スライド構成_提案.md に出力
```

**Step 3（初期デスクトップ調査）** ※ SubAgent経由:
```
1. ユーザーに提案書のパスと出力先フォルダを確認
2. desk-researcher SubAgent（agents/desk-researcher.md）を起動
   - 提案書パス、出力先フォルダ、モード: initial を指定
3. SubAgentの返却結果（ファイルパス、発見事項、仮説検証要約）を受け取る
4. レビューゲートへ進む
```

**Step 10（詳細デスクリサーチ）** ※ SubAgent経由:
```
1. 提案書、インタビューまとめ、既存調査結果のパスを確認
2. ユーザーに出力先フォルダを確認
3. desk-researcher SubAgent（agents/desk-researcher.md）を起動
   - 提案書パス、インタビューまとめパス、既存調査パス、出力先フォルダ、モード: detailed を指定
4. SubAgentの返却結果（ファイルパス、発見事項、仮説検証要約）を受け取る
5. レビューゲートへ進む
```

**Step 5（インタビューガイド作成）**:
```
1. skills/interview-guide-creator/SKILL.md を読み込む
2. Output/提案書.md から論点・仮説を確認
3. Input/初期調査結果.md から未検証事項を把握
4. スキルの指示に従ってインタビューガイドを作成
```

**Step 6（報告書骨子作成）**:
```
1. skills/report-outline-creator/SKILL.md を読み込む
2. Output/提案書.md から論点・仮説・納品物定義を確認
3. Output/インタビューガイド.md から検証事項を確認
4. Input/初期調査結果.md から調査で得た情報を把握
5. プロジェクト種類を判定し、references/structure_templates.md を参照
6. スキルの指示に従って報告書骨子を作成
```

**Step 7（インタビュー対象者選定）**:
```
1. skills/interview-candidate-selector/SKILL.md を読み込む
2. Output/インタビューガイド.md から対象者タイプ定義を抽出
3. Interview/ 内の候補者リストを読み込む（xlsxスキルを活用）
4. スキルの指示に従って対象者を選定・評価
```

**Step 8（インタビュー議事録作成）**:
```
1. skills/interview-minutes-creator/SKILL.md を読み込む
2. Input/インタビュー/ 内の文字起こしファイルを確認
3. Output/インタビューガイド.md の質問リストを参照
4. スキルの指示に従って議事録を作成
```

**Step 13（報告用スライド構成設計）**:
```
1. skills/slide-structure-designer/SKILL.md を読み込む
2. Output/最終報告書.md をソースとして渡す（必要に応じて Output/報告書骨子.md・Output/分析結果.md も参照）
3. スキルの指示に従って報告用スライド構成を設計
4. Output/スライド構成.md に出力
```

## 成果物一覧

| ステップ | 成果物 | 格納先 |
|----------|--------|--------|
| 初期化, Step 1〜 | プロジェクトサマリ | `Output/プロジェクトサマリ.md` |
| Step 1, 4 | 提案書 | `Output/提案書.md` |
| Step 2 | スライド構成（提案） | `Output/スライド構成_提案.md` |
| Step 3 | 初期調査結果 | ユーザー指定の出力先フォルダ |
| Step 5 | インタビューガイド | `Output/インタビューガイド.md` |
| Step 6 | 報告書骨子 | `Output/報告書骨子.md` |
| Step 7 | インタビュー対象者 | `Output/インタビュー対象者.md` |
| Step 8 | 議事録 | `Output/議事録/` |
| Step 9 | インタビューまとめ | `Output/インタビューまとめ.md` |
| Step 10 | デスクリサーチ結果 | ユーザー指定の出力先フォルダ |
| Step 11 | 分析結果 | `Output/分析結果.md` |
| Step 12 | 最終報告書 | `Output/最終報告書.md` |
| Step 13 | スライド構成（報告） | `Output/スライド構成.md` |
