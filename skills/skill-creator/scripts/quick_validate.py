#!/usr/bin/env python3
"""
スキルの構造を簡易バリデーションする。

Usage:
    python quick_validate.py <skill-directory>

Example:
    python quick_validate.py skills/my-skill
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[error] PyYAML が必要です: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.+?)\n---", re.DOTALL)
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}


# ---------------------------------------------------------------------------
# バリデーション
# ---------------------------------------------------------------------------


def check_skill(skill_dir: Path) -> list[str]:
    """スキルディレクトリを検証し、問題のリストを返す。空なら合格。"""
    errors: list[str] = []

    md_path = skill_dir / "SKILL.md"
    if not md_path.exists():
        return ["SKILL.md が見つかりません"]

    text = md_path.read_text(encoding="utf-8")

    # --- frontmatter の抽出 ---
    if not text.startswith("---"):
        return ["YAML frontmatter がありません（先頭が --- で始まっていません）"]

    m = FRONTMATTER_RE.match(text)
    if m is None:
        return ["frontmatter の閉じ --- が見つかりません"]

    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        return [f"frontmatter の YAML パースに失敗しました: {exc}"]

    if not isinstance(fm, dict):
        return ["frontmatter が辞書形式ではありません"]

    # --- キーの検証 ---
    extra = set(fm.keys()) - ALLOWED_KEYS
    if extra:
        errors.append(f"許可されていないキーがあります: {', '.join(sorted(extra))}")

    # --- name ---
    name = fm.get("name")
    if name is None:
        errors.append("name フィールドがありません")
    elif not isinstance(name, str):
        errors.append(f"name は文字列である必要があります（実際の型: {type(name).__name__}）")
    else:
        name = name.strip()
        if not NAME_PATTERN.match(name):
            errors.append(
                f"name '{name}' はハイフン区切りの小文字英数字にしてください"
            )
        if len(name) > MAX_NAME_LENGTH:
            errors.append(
                f"name が長すぎます（{len(name)}文字）。上限は {MAX_NAME_LENGTH} 文字です"
            )

    # --- description ---
    desc = fm.get("description")
    if desc is None:
        errors.append("description フィールドがありません")
    elif not isinstance(desc, str):
        errors.append(
            f"description は文字列である必要があります（実際の型: {type(desc).__name__}）"
        )
    else:
        desc = desc.strip()
        if "<" in desc or ">" in desc:
            errors.append("description に山括弧（< >）は使えません")
        if len(desc) > MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"description が長すぎます（{len(desc)}文字）。上限は {MAX_DESCRIPTION_LENGTH} 文字です"
            )

    return errors


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <skill-directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.is_dir():
        print(f"[error] ディレクトリが見つかりません: {target}", file=sys.stderr)
        sys.exit(1)

    problems = check_skill(target)

    if problems:
        print("バリデーション失敗:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    else:
        print("バリデーション合格")
        sys.exit(0)


if __name__ == "__main__":
    main()
