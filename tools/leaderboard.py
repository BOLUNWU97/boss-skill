#!/usr/bin/env python3
"""
Boss Skill Nightmare Leaderboard
公开排行榜：社区投票Nightmare Level
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict


class NightmareLeaderboard:
    """
    噩梦排行榜
    
    功能：
    - 记录用户的老板Nightmare Level
    - 社区匿名投票
    - 统计分布
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.leaderboard_file = self.base_dir / "nightmare_leaderboard.json"
        self.my_bosses_file = self.base_dir / "my_bosses.json"
    
    def submit_boss(self, name: str, company: str, 
                   nightmare_level: float, 
                   description: str = "",
                   submitter_id: str = "anonymous") -> dict:
        """
        提交你的老板到排行榜
        
        name: 老板称呼
        company: 公司/行业
        nightmare_level: 1-5
        description: 简短描述（可选）
        submitter_id: 提交者ID（匿名）
        """
        boss_entry = {
            "id": f"boss_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "name": name,
            "company": company,
            "nightmare_level": nightmare_level,
            "description": description,
            "submitter_id": submitter_id,
            "votes": 0,
            "voters": []
        }
        
        # 读取已有数据
        data = self._load_data()
        data["bosses"].append(boss_entry)
        self._save_data(data)
        
        return boss_entry
    
    def vote_boss(self, boss_id: str, voter_id: str = "anonymous") -> bool:
        """
        给一个老板投票（表示"我的老板也是这样"）
        
        返回：投票是否成功
        """
        data = self._load_data()
        
        for boss in data["bosses"]:
            if boss["id"] == boss_id:
                if voter_id not in boss["voters"]:
                    boss["votes"] += 1
                    boss["voters"].append(voter_id)
                    self._save_data(data)
                    return True
                else:
                    return False  # 已投过票
        
        return False  # 没找到
    
    def get_leaderboard(self, sort_by: str = "nightmare_level", 
                       limit: int = 20) -> List[Dict]:
        """
        获取排行榜
        
        sort_by: 排序方式
        - "nightmare_level": 按噩梦程度
        - "votes": 按投票数
        """
        data = self._load_data()
        bosses = data["bosses"]
        
        # 排序
        if sort_by == "nightmare_level":
            bosses = sorted(bosses, key=lambda x: x["nightmare_level"], reverse=True)
        elif sort_by == "votes":
            bosses = sorted(bosses, key=lambda x: x["votes"], reverse=True)
        
        return bosses[:limit]
    
    def get_statistics(self) -> Dict:
        """获取统计数据"""
        data = self._load_data()
        bosses = data["bosses"]
        
        if not bosses:
            return {
                "total_bosses": 0,
                "avg_nightmare": 0,
                "distribution": {}
            }
        
        # 计算平均
        total = sum(b["nightmare_level"] for b in bosses)
        avg = total / len(bosses)
        
        # 分布
        dist = {"1-2": 0, "2-3": 0, "3-4": 0, "4-5": 0}
        for b in bosses:
            nl = b["nightmare_level"]
            if nl < 2:
                dist["1-2"] += 1
            elif nl < 3:
                dist["2-3"] += 1
            elif nl < 4:
                dist["3-4"] += 1
            else:
                dist["4-5"] += 1
        
        return {
            "total_bosses": len(bosses),
            "avg_nightmare": round(avg, 2),
            "total_votes": sum(b["votes"] for b in bosses),
            "distribution": dist
        }
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if not self.leaderboard_file.exists():
            return {"bosses": []}
        
        with open(self.leaderboard_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        """保存数据"""
        self.leaderboard_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.leaderboard_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def print_leaderboard(self, limit: int = 10):
        """打印排行榜"""
        leaders = self.get_leaderboard(limit=limit)
        stats = self.get_statistics()
        
        print(f"""
{'='*60}
🏆 Nightmare Leaderboard 噩梦排行榜

📊 统计：
   总BOSS数：{stats['total_bosses']}
   平均噩梦：{stats['avg_nightmare']:.1f}/5
   总投票数：{stats['total_votes']}

📈 分布：
   ⭐1-2: {stats['distribution']['1-2']}人
   ⭐⭐2-3: {stats['distribution']['2-3']}人
   ⭐⭐⭐3-4: {stats['distribution']['3-4']}人
   ⭐⭐⭐⭐4-5: {stats['distribution']['4-5']}人

🏅 TOP {limit}：
""")
        
        for i, boss in enumerate(leaders, 1):
            stars = "⭐" * int(boss["nightmare_level"])
            print(f"  {i}. {boss['name']} ({boss['company']})")
            print(f"     {stars} {boss['nightmare_level']}/5 | {boss['votes']}票")
            if boss.get("description"):
                print(f"     \"{boss['description'][:50]}\"")
        
        print(f"\n{'='*60}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Nightmare Leaderboard")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--action", choices=["submit", "vote", "list", "stats"])
    parser.add_argument("--name", help="老板名字")
    parser.add_argument("--company", help="公司")
    parser.add_argument("--nightmare", type=float, help="Nightmare Level 1-5")
    parser.add_argument("--description", help="描述")
    parser.add_argument("--boss-id", help="BOSS ID")
    parser.add_argument("--limit", type=int, default=10, help="显示数量")
    
    args = parser.parse_args()
    lb = NightmareLeaderboard(args.base_dir)
    
    if args.action == "submit":
        if not all([args.name, args.company, args.nightmare]):
            print("错误：submit需要 --name --company --nightmare")
            return
        
        result = lb.submit_boss(
            args.name, args.company, args.nightmare,
            args.description or "", "anonymous"
        )
        print(f"✅ 提交成功！")
        print(f"   ID: {result['id']}")
        print(f"   {args.name} - {args.company} - ⭐{args.nightmare}/5")
    
    elif args.action == "vote":
        if not args.boss_id:
            print("错误：vote需要 --boss-id")
            return
        
        if lb.vote_boss(args.boss_id):
            print("✅ 投票成功！")
        else:
            print("❌ 已投过票或BOSS不存在")
    
    elif args.action == "list":
        lb.print_leaderboard(args.limit)
    
    elif args.action == "stats":
        stats = lb.get_statistics()
        print(f"📊 统计数据：")
        print(f"   总BOSS数：{stats['total_bosses']}")
        print(f"   平均噩梦：{stats['avg_nightmare']:.1f}/5")


if __name__ == "__main__":
    main()
