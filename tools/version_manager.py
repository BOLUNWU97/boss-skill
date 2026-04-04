#!/usr/bin/env python3
"""
Boss Skill 版本管理器
"""

import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

MAX_VERSIONS = 10

def list_versions(skill_dir):
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return []
    versions = []
    for v_dir in sorted(versions_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if v_dir.is_dir():
            mtime = datetime.fromtimestamp(v_dir.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            versions.append({"version": v_dir.name, "archived_at": mtime, "path": str(v_dir)})
    return versions

def rollback(skill_dir, target_version):
    version_dir = skill_dir / "versions" / target_version
    if not version_dir.exists():
        print(f"错误：版本 {target_version} 不存在", file=sys.stderr)
        return False
    # 备份当前版本
    meta_path = skill_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        current_version = meta.get("version", "v?")
        backup_dir = skill_dir / "versions" / f"{current_version}_before_rollback"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for fname in ("SKILL.md", "management.md", "persona.md"):
            src = skill_dir / fname
            if src.exists():
                shutil.copy2(src, backup_dir / fname)
    # 恢复目标版本
    for fname in ("SKILL.md", "management.md", "persona.md"):
        src = version_dir / fname
        if src.exists():
            shutil.copy2(src, skill_dir / fname)
    print(f"已回滚到 {target_version}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Boss Skill 版本管理器")
    parser.add_argument("--action", required=True, choices=["list", "rollback"])
    parser.add_argument("--slug", required=True)
    parser.add_argument("--version")
    parser.add_argument("--base-dir", default="./bosses")
    args = parser.parse_args()
    
    skill_dir = Path(args.base_dir) / args.slug
    if not skill_dir.exists():
        print(f"错误：找不到 Skill {args.slug}")
        sys.exit(1)
    
    if args.action == "list":
        versions = list_versions(skill_dir)
        if not versions:
            print(f"{args.slug} 暂无历史版本")
        else:
            print(f"{args.slug} 的历史版本：\n")
            for v in versions:
                print(f"  {v['version']}  存档时间: {v['archived_at']}")
    
    elif args.action == "rollback":
        if not args.version:
            print("错误：需要指定 --version")
            sys.exit(1)
        rollback(skill_dir, args.version)

if __name__ == "__main__":
    main()
