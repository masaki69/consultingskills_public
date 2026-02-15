#!/usr/bin/env python3
"""
スキルを .skill ファイル（zip 形式）にパッケージする。

Usage:
    python package_skill.py <skill-directory> [output-directory]

Example:
    python package_skill.py skills/my-skill
    python package_skill.py skills/my-skill dist/
"""

import sys
import zipfile
from pathlib import Path

# quick_validate を同ディレクトリからインポート
sys.path.insert(0, str(Path(__file__).resolve().parent))
from quick_validate import check_skill  # noqa: E402


def build_package(skill_dir: Path, output_dir: Path | None = None) -> Path:
    """スキルディレクトリを検証し、.skill ファイルを生成する。"""

    if not skill_dir.is_dir():
        print(f"[error] ディレクトリが見つかりません: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    if not (skill_dir / "SKILL.md").exists():
        print(f"[error] SKILL.md が見つかりません: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # バリデーション
    print("バリデーション中...")
    problems = check_skill(skill_dir)
    if problems:
        print("バリデーション失敗:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("バリデーション合格\n")

    # 出力先
    dest = (output_dir or Path.cwd()).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    archive_path = dest / f"{skill_dir.name}.skill"

    # zip 作成
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(skill_dir.rglob("*")):
            if not file.is_file():
                continue
            arc_name = file.relative_to(skill_dir.parent)
            zf.write(file, arc_name)
            print(f"  + {arc_name}")

    print(f"\nパッケージを作成しました: {archive_path}")
    return archive_path


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {Path(__file__).name} <skill-directory> [output-directory]")
        sys.exit(1)

    skill_dir = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None

    build_package(skill_dir, output_dir)


if __name__ == "__main__":
    main()
