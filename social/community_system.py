#!/usr/bin/env python3
"""
社区老板库 - Community Boss Library
分享、发现、继承其他用户的老板
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

class CommunitySystem:
    """社区老板系统"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.community_dir = self.base_dir / "community"
        self.community_dir.mkdir(parents=True, exist_ok=True)
        self.my_submissions_file = self.community_dir / "my_submissions.json"
        self.votes_file = self.community_dir / "votes.json"
        
        self.submissions = self._load_submissions()
        self.votes = self._load_votes()
    
    def _load_submissions(self) -> dict:
        if self.my_submissions_file.exists():
            return json.loads(self.my_submissions_file.read_text())
        return {
            "submitted": [],  # 我提交的老板
            "inherited": [],   # 我继承的老板
        }
    
    def _load_votes(self) -> dict:
        if self.votes_file.exists():
            return json.loads(self.votes_file.read_text())
        return {
            "voted_for": {},  # 投票给谁的老板
        }
    
    def _save_submissions(self):
        self.my_submissions_file.write_text(json.dumps(self.submissions, indent=2, ensure_ascii=False))
    
    def _save_votes(self):
        self.votes_file.write_text(json.dumps(self.votes, indent=2, ensure_ascii=False))
    
    def submit_boss(self, boss_data: dict) -> dict:
        """
        提交老板到社区
        boss_data 需要包含：
        - name: 老板花名（脱敏）
        - company: 公司类型（脱敏）
        - nightmare_level: 噩梦等级
        - tags: 苛刻标签
        - persona_summary: 老板画像摘要
        """
        submission = {
            "id": self._generate_boss_id(boss_data),
            "name": boss_data.get("name", "匿名老板"),
            "company_type": boss_data.get("company", "未知"),
            "nightmare_level": boss_data.get("nightmare_level", 3.0),
            "tags": boss_data.get("tags", []),
            "persona_summary": boss_data.get("persona_summary", ""),
            "submitted_at": datetime.now().isoformat(),
            "votes": 0,
            "inherited_count": 0,
        }
        
        self.submissions["submitted"].append(submission)
        self._save_submissions()
        
        return submission
    
    def _generate_boss_id(self, boss_data: dict) -> str:
        """生成唯一ID"""
        content = f"{boss_data.get('name', '')}{boss_data.get('mbti', '')}{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def inherit_boss(self, boss_id: str) -> Optional[dict]:
        """从社区继承一个老板"""
        # 在提交列表中找到这个老板
        for submission in self.submissions["submitted"]:
            if submission["id"] == boss_id:
                # 增加继承计数
                submission["inherited_count"] += 1
                
                # 添加到继承列表
                inherited = {
                    "id": submission["id"],
                    "name": submission["name"],
                    "company_type": submission["company_type"],
                    "nightmare_level": submission["nightmare_level"],
                    "tags": submission["tags"],
                    "inherited_at": datetime.now().isoformat(),
                }
                self.submissions["inherited"].append(inherited)
                self._save_submissions()
                
                return inherited
        
        return None
    
    def vote_for_boss(self, boss_id: str, vote: bool = True):
        """投票"""
        if boss_id not in self.votes["voted_for"]:
            self.votes["voted_for"][boss_id] = 0
        
        if vote:
            self.votes["voted_for"][boss_id] += 1
        
        # 更新对应老板的票数
        for submission in self.submissions["submitted"]:
            if submission["id"] == boss_id:
                submission["votes"] = self.votes["voted_for"][boss_id]
                break
        
        self._save_submissions()
        self._save_votes()
    
    def get_top_bosses(self, limit: int = 10) -> List[dict]:
        """获取排行榜（按票数）"""
        all_bosses = self.submissions["submitted"].copy()
        all_bosses.sort(key=lambda x: x.get("votes", 0), reverse=True)
        return all_bosses[:limit]
    
    def get_by_nightmare_level(self, min_level: float = 4.0) -> List[dict]:
        """按噩梦等级筛选"""
        return [b for b in self.submissions["submitted"] if b.get("nightmare_level", 0) >= min_level]
    
    def get_status(self) -> str:
        """获取社区状态"""
        submitted_count = len(self.submissions["submitted"])
        inherited_count = len(self.submissions["inherited"])
        
        top_bosses = self.get_top_bosses(3)
        
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║                 🌍 社区老板库状态                           ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 我提交的老板：{submitted_count:<42}║",
            f"║ 我继承的老板：{inherited_count:<42}║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║ 🏆 热门老板 TOP 3：                                         ║",
        ]
        
        if not top_bosses:
            lines.append("║   (暂无数据)                                                ║")
        else:
            for i, boss in enumerate(top_bosses, 1):
                stars = "⭐" * int(boss.get("nightmare_level", 3))
                lines.append(f"║   {i}. {boss['name']} {stars} ({boss.get('votes', 0)}票)        ║")
        
        lines.extend([
            "╠══════════════════════════════════════════════════════════════╣",
            "║ 提交老板：/submit-boss                                       ║",
            "║ 继承老板：/inherit-boss <id>                                ║",
            "║ 查看排行：/community-top                                    ║",
            "╚══════════════════════════════════════════════════════════════╝",
        ])
        
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="社区老板系统")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=["submit", "inherit", "vote", "top", "status"], required=True)
    parser.add_argument("--name")
    parser.add_argument("--company")
    parser.add_argument("--nightmare", type=float)
    parser.add_argument("--tags", nargs="*")
    parser.add_argument("--boss-id")
    parser.add_argument("--limit", type=int, default=10)
    
    args = parser.parse_args()
    system = CommunitySystem(args.base_dir)
    
    if args.action == "submit":
        result = system.submit_boss({
            "name": args.name or "测试老板",
            "company": args.company or "某大厂",
            "nightmare_level": args.nightmare or 3.5,
            "tags": args.tags or ["深夜轰炸"],
        })
        print(f"✅ 老板已提交：{result['id']}")
        print(f"   {result['name']} (⭐{result['nightmare_level']})")
    
    elif args.action == "inherit":
        result = system.inherit_boss(args.boss_id)
        if result:
            print(f"✅ 继承成功：{result['name']}")
        else:
            print("❌ 未找到该老板")
    
    elif args.action == "vote":
        system.vote_for_boss(args.boss_id, True)
        print(f"✅ 投票成功")
    
    elif args.action == "top":
        bosses = system.get_top_bosses(args.limit)
        for b in bosses:
            print(f"{b['id']}: {b['name']} ⭐{b['nightmare_level']} ({b.get('votes', 0)}票)")
    
    elif args.action == "status":
        print(system.get_status())


if __name__ == "__main__":
    main()
