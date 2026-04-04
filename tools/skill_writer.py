#!/usr/bin/env python3
"""
Boss Skill 列表管理工具
"""

import json
import argparse
from pathlib import Path

def list_skills(base_dir):
    base_path = Path(base_dir)
    if not base_path.exists():
        print("暂无 Boss Skill")
        return
    
    bosses = []
    for d in sorted(base_path.iterdir()):
        if d.is_dir() and (d / "meta.json").exists():
            meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
            bosses.append(meta)
    
    if not bosses:
        print("暂无 Boss Skill")
        return
    
    print(f"共有 {len(bosses)} 个 Boss Skill：\n")
    for b in bosses:
        print(f"  👔 {b['name']} ({b['slug']})")
        print(f"     级别：{b['profile'].get('level', 'N/A')} | Nightmare: {b.get('nightmare_level', 'N/A')}")
        print(f"     标签：{', '.join(b['tags'].get('pain_points', [])[:3])}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Boss Skill 管理")
    parser.add_argument("--action", required=True, choices=["list"])
    parser.add_argument("--base-dir", default="./bosses")
    args = parser.parse_args()
    
    if args.action == "list":
        list_skills(args.base_dir)

if __name__ == "__main__":
    main()
