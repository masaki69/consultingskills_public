#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown内の参考文献を整理するスクリプト

機能:
- 同じベースURLを持つ参考文献を統合（フラグメント・クエリパラメータ除去）
- 本文中のハイパーリンク付き参照 [\\[N\\]](URL) を [N] 形式に変換
- 連続する重複参照番号をマージ
- 末尾に整理された参考文献リストを生成

使用方法:
    python consolidate_references.py <input.md> <output.md>
"""

import re
import sys
from urllib.parse import urlparse, urlunparse
from collections import OrderedDict


def get_base_url(url: str) -> str:
    """URLからフラグメント(#以降)とクエリパラメータを除去してベースURLを取得"""
    parsed = urlparse(url)
    base = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    return base


def extract_references(content: str) -> list:
    """Markdown内の参照パターンを抽出
    
    パターン: [\\[N\\]](URL) - エスケープされた角括弧を含む
    """
    pattern = r'\[\\\[(\d+)\\\]\]\((https?://[^\)]+)\)'
    return re.findall(pattern, content)


def build_url_mapping(matches: list) -> tuple:
    """参照番号とURLのマッピングを構築
    
    Returns:
        old_to_new: 旧番号→新番号のマッピング
        new_ref_list: (新番号, ベースURL)のリスト
    """
    url_to_refs = OrderedDict()  # {base_url: [original_ref_numbers]}
    
    for ref_num, url in matches:
        base_url = get_base_url(url)
        
        if base_url not in url_to_refs:
            url_to_refs[base_url] = []
        if ref_num not in url_to_refs[base_url]:
            url_to_refs[base_url].append(ref_num)
    
    # 新しい番号付けを作成
    old_to_new = {}
    new_ref_list = []
    
    new_num = 1
    for base_url, old_refs in url_to_refs.items():
        for old_ref in old_refs:
            old_to_new[old_ref] = str(new_num)
        new_ref_list.append((new_num, base_url))
        new_num += 1
    
    return old_to_new, new_ref_list


def replace_inline_references(content: str, old_to_new: dict) -> str:
    """本文中のハイパーリンク付き参照を単純な [N] 形式に置換"""
    pattern = r'\[\\\[(\d+)\\\]\]\((https?://[^\)]+)\)'
    
    def replace_ref(match):
        old_num = match.group(1)
        new_num = old_to_new.get(old_num, old_num)
        return f'[{new_num}]'
    
    return re.sub(pattern, replace_ref, content)


def merge_duplicate_refs(content: str) -> str:
    """連続する同じ参照番号をマージ（例：[5][5] -> [5]）"""
    prev = ''
    while prev != content:
        prev = content
        content = re.sub(r'\[(\d+)\]\[\1\]', r'[\1]', content)
    return content


def find_main_content_end(lines: list) -> int:
    """本文の終了位置を特定（末尾の参考文献セクション手前）"""
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        # 本文らしい行（長い文章、または見出し）
        if line.startswith('##') or (len(line) > 100 and '。' in line):
            end = i + 1
            # 後続の空行も含める
            while end < len(lines) and not lines[end].strip():
                end += 1
            return end
    return len(lines)


def generate_reference_section(ref_list: list) -> str:
    """参考文献セクションを生成"""
    section = '\n\n---\n\n## 参考文献\n\n'
    for num, url in ref_list:
        section += f'[{num}] {url}\n\n'
    return section


def consolidate_references(input_path: str, output_path: str) -> dict:
    """メイン処理: 参考文献を整理してファイルに出力
    
    Returns:
        処理結果の統計情報
    """
    # ファイル読み込み
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 参照を抽出
    matches = extract_references(content)
    
    if not matches:
        # 参照が見つからない場合はそのまま出力
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {'original_refs': 0, 'consolidated_refs': 0}
    
    # URLマッピングを構築
    old_to_new, new_ref_list = build_url_mapping(matches)
    
    # 本文中の参照を置換
    content = replace_inline_references(content, old_to_new)
    
    # 重複参照番号をマージ
    content = merge_duplicate_refs(content)
    
    # 本文部分を抽出（末尾の既存参考文献リストを除去）
    lines = content.split('\n')
    main_end = find_main_content_end(lines)
    main_content = '\n'.join(lines[:main_end])
    
    # 参考文献セクションを追加
    ref_section = generate_reference_section(new_ref_list)
    final_content = main_content + ref_section
    
    # 出力
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return {
        'original_refs': len(matches),
        'consolidated_refs': len(new_ref_list),
        'mapping': old_to_new
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.md>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    result = consolidate_references(input_file, output_file)
    
    print(f"参考文献整理完了:")
    print(f"  元の参照数: {result['original_refs']}")
    print(f"  統合後の参照数: {result['consolidated_refs']}")
    print(f"  出力ファイル: {output_file}")
