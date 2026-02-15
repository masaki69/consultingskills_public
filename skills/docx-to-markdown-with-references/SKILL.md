---
name: docx-to-markdown-with-references
description: Word文書（.docx）をMarkdownに変換し、参考文献を整理するスキル。「Wordをマークダウンに変換して」「docxをmdに変換して参考文献を整理して」「Word文書の参考文献を統合して」「レポートをMarkdownに変換して」などのリクエスト時に使用。pandoc（またはpython-docxフォールバック）による変換と、重複URL統合・番号再割当て・参考文献リスト生成・文書構造整形を行う。
---

# Word to Markdown with Reference Consolidation

Word文書をMarkdownに変換し、参考文献を整理するスキル。

## 処理フロー

```
処理フロー
├── Step 1: Word → Markdown変換
│   ├── pandoc（推奨）
│   └── python-docx（フォールバック）
├── Step 2: 参考文献の整理・番号再割当て
│   ├── URL重複の統合
│   ├── 番号の再割当て
│   └── 本文中の参照番号更新
└── Step 3: 文書構造の整形（オプション）
    ├── セクション分離
    ├── 改行挿入
    └── 箇条書き整形
```

---

## Step 1: Word → Markdown変換

pandoc を推奨。利用できない場合は `scripts/convert_docx.py` にフォールバック。

```bash
# pandoc（推奨）
pandoc -f docx -t markdown --wrap=none -o output.md input.docx

# python-docx フォールバック（pip install python-docx が必要）
python scripts/convert_docx.py input.docx output.md
```

---

## Step 2: 参考文献の整理・番号再割当て

同じURLが異なる番号で参照されている場合、番号を統合して再割当てする。

```bash
python scripts/consolidate_references.py input.md output.md
```

---

## Step 3: 文書構造の整形（オプション）

調査レポート形式の文書向けに、可読性を向上させる整形処理。

```bash
python scripts/format_structure.py input.md output.md
```

---

## 出力形式

**本文中の参照**: `[1]`, `[2]` 等のシンプルな番号形式（同一URLは同じ番号）

**文書構造**:
```markdown
## 大論点①：タイトル

**主張**

主張の内容...[1]

**根拠**

- **項目名1**: 説明文...[1]

- **項目名2**: 説明文...[2]
```

**参考文献セクション**:
```markdown
---

## 参考文献

[1] https://example.com/article1

[2] https://example.com/article2
```

---

## 注意事項

- pandocがインストールされていない場合は `pip install python-docx` が必要
- 入力ファイルはUTF-8エンコーディングを想定
- 参考文献パターンが `[N] URL` 形式でない場合は正規表現を調整
- Step 3の文書構造整形は調査レポート形式を想定（必要に応じてスキップ可能）
