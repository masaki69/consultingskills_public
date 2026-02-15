#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調査レポート形式の Markdown 文書の可読性を向上させる整形スクリプト

処理内容:
- 「主張:」「根拠:」を独立セクション化
- 箇条書き項目名を太字に統一
- 見出し前に空行を追加

使用方法:
    python format_structure.py <input.md> <output.md>
"""

import re
import sys


def format_document_structure(input_path: str, output_path: str) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 参考文献セクションを分離（整形対象外）
    ref_marker = "\n---\n\n## 参考文献"
    if ref_marker in content:
        main_text, ref_section = content.split(ref_marker)
        ref_section = ref_marker + ref_section
    else:
        main_text = content
        ref_section = ""

    # 「主張:」「根拠:」を独立セクション化
    main_text = re.sub(r'\n(主張: )', r'\n\n**主張**\n\n', main_text)
    main_text = re.sub(r'^(主張: )', r'**主張**\n\n', main_text)
    main_text = re.sub(r'\n(根拠: )', r'\n\n**根拠**\n\n', main_text)
    main_text = re.sub(r'^(根拠: )', r'**根拠**\n\n', main_text)

    # 箇条書き項目を改行で分離し、項目名を太字に
    main_text = re.sub(r' - ([^:]+): ', r'\n\n- **\1**: ', main_text)

    # 太字でない箇条書き項目も太字に統一
    main_text = re.sub(r'\n- ([^*\n]+): ', r'\n- **\1**: ', main_text)

    # 小論点・大論点の見出し前に空行を追加
    main_text = re.sub(r'([^\n])\n(小論点)', r'\1\n\n\2', main_text)
    main_text = re.sub(r'([^\n])\n(### 小論点)', r'\1\n\n### 小論点', main_text)
    main_text = re.sub(r'([^\n])\n(## 大論点)', r'\1\n\n## 大論点', main_text)

    final_content = main_text + ref_section

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.md>")
        sys.exit(1)

    format_document_structure(sys.argv[1], sys.argv[2])
    print(f"整形完了: {sys.argv[2]}")
