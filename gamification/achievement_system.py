#!/usr/bin/env python3
"""
成就系统 - Achievement System
解锁各种成就，记录玩家里程碑
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AchievementSystem:
    """成就系统"""
    
    # 成就定义
    ACHIEVEMENTS = {
        # 生存类
        "survive_10m": {
            "id": "survive_10m",
            "name": "⏱️ 十分钟玩家",
            "description": "和老板对线10分钟没崩溃",
            "category": "survival",
            "xp_reward": 50,
        },
        "survive_30m": {
            "id": "survive_30m",
            "name": "🔥 三十分钟战士",
            "description": "和老板对线30分钟依然坚挺",
            "category": "survival",
            "xp_reward": 150,
        },
        "survive_1h": {
            "id": "survive_1h",
            "name": "💀 一小时存活",
            "description": "和老板对线1小时，见过地狱",
            "category": "survival",
            "xp_reward": 500,
        },
        
        # 对线类
        "first_boss": {
            "id": "first_boss",
            "name": "👋 初见老板",
            "description": "创建第一个老板",
            "category": "battle",
            "xp_reward": 20,
        },
        "battle_10": {
            "id": "battle_10",
            "name": "⚔️ 对线老手",
            "description": "和老板对线10次",
            "category": "battle",
            "xp_reward": 100,
        },
        "battle_50": {
            "id": "battle_50",
            "name": "💪 对线达人",
            "description": "和老板对线50次",
            "category": "battle",
            "xp_reward": 300,
        },
        "battle_100": {
            "id": "battle_100",
            "name": "🏆 对线王者",
            "description": "和老板对线100次",
            "category": "battle",
            "xp_reward": 1000,
        },
        
        # 方案类
        "first_ralplan": {
            "id": "first_ralplan",
            "name": "📋 首次审方案",
            "description": "使用Ralplan模式审阅方案",
            "category": "plan",
            "xp_reward": 30,
        },
        "ralplan_pass": {
            "id": "ralplan_pass",
            "name": "✅ 方案通过",
            "description": "方案一次性通过老板审批",
            "category": "plan",
            "xp_reward": 100,
        },
        "ralplan_5": {
            "id": "ralplan_5",
            "name": "📝 五轮审阅",
            "description": "一个方案被审了5轮还在改",
            "category": "plan",
            "xp_reward": 80,
        },
        
        # 任务类
        "first_ralph": {
            "id": "first_ralph",
            "name": "📊 首次汇报",
            "description": "使用Ralph模式汇报任务",
            "category": "task",
            "xp_reward": 30,
        },
        "task_delivered": {
            "id": "task_delivered",
            "name": "🚀 准时交付",
            "description": "在老板的压迫下准时完成任务",
            "category": "task",
            "xp_reward": 120,
        },
        
        # 应对类
        "perfect_response": {
            "id": "perfect_response",
            "name": "🎯 完美应对",
            "description": "连续3次正确回答老板追问",
            "category": "skill",
            "xp_reward": 80,
        },
        "anger_management": {
            "id": "anger_management",
            "name": "🧘 情绪管理",
            "description": "老板发了3次火都被你化解",
            "category": "skill",
            "xp_reward": 100,
        },
        "data_master": {
            "id": "data_master",
            "name": "📈 数据大师",
            "description": "用数据回答了老板的5连问",
            "category": "skill",
            "xp_reward": 150,
        },
        
        # 进阶类
        "nightmare_5": {
            "id": "nightmare_5",
            "name": "☠️ 五星噩梦",
            "description": "挑战最高难度(Nightmare 5)并存活",
            "category": "extreme",
            "xp_reward": 500,
        },
        "all_modes": {
            "id": "all_modes",
            "name": "🎭 全能选手",
            "description": "使用过所有三种对线模式",
            "category": "explore",
            "xp_reward": 100,
        },
        "multi_battle": {
            "id": "multi_battle",
            "name": "⚔️ 修罗场体验",
            "description": "参与多老板对战",
            "category": "extreme",
            "xp_reward": 200,
        },
        
        # 收集类
        "boss_collector": {
            "id": "boss_collector",
            "name": "📚 老板收藏家",
            "description": "创建3个不同的老板",
            "category": "collect",
            "xp_reward": 150,
        },
        "boss_hunter": {
            "id": "boss_hunter",
            "name": "🎯 老板猎人",
            "description": "创建10个不同的老板",
            "category": "collect",
            "xp_reward": 500,
        },
    }
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.state_file = self.base_dir / ".boss" / "achievements_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "unlocked": [],  # 已解锁的成就ID列表
            "progress": {},  # 各成就进度
            "recent_unlock": None,  # 最近解锁的成就
        }
    
    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
    
    def unlock(self, achievement_id: str) -> Optional[dict]:
        """解锁成就"""
        if achievement_id in self.state["unlocked"]:
            return None  # 已经解锁过了
        
        if achievement_id not in self.ACHIEVEMENTS:
            raise ValueError(f"Unknown achievement: {achievement_id}")
        
        achievement = self.ACHIEVEMENTS[achievement_id]
        self.state["unlocked"].append(achievement_id)
        self.state["recent_unlock"] = {
            "id": achievement_id,
            "name": achievement["name"],
            "description": achievement["description"],
            "unlocked_at": datetime.now().isoformat(),
        }
        self._save_state()
        
        return achievement
    
    def update_progress(self, achievement_id: str, progress: int):
        """更新成就进度"""
        if achievement_id not in self.ACHIEVEMENTS:
            return
        
        if achievement_id not in self.state["progress"]:
            self.state["progress"][achievement_id] = 0
        
        self.state["progress"][achievement_id] = progress
        self._save_state()
    
    def check_and_unlock(self, achievement_id: str) -> Optional[dict]:
        """检查进度并解锁"""
        if achievement_id in self.state["unlocked"]:
            return None
        
        achievement = self.ACHIEVEMENTS.get(achievement_id)
        if not achievement:
            return None
        
        # 检查是否有进度要求
        progress = self.state.get("progress", {}).get(achievement_id, 0)
        
        # 自动解锁无条件成就
        if achievement_id in ["first_boss", "first_ralplan", "first_ralph"]:
            return self.unlock(achievement_id)
        
        return None
    
    def get_status(self) -> str:
        """获取成就状态"""
        unlocked = self.state["unlocked"]
        total = len(self.ACHIEVEMENTS)
        percentage = len(unlocked) / total * 100 if total > 0 else 0
        
        recent = self.state.get("recent_unlock")
        
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║                    🏆 成就系统                               ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 已解锁：{len(unlocked)}/{total} ({percentage:.1f}%){' ':<30}║",
        ]
        
        if recent:
            lines.append(f"║ 最近解锁：{recent['name']:<43}║")
        
        lines.append("╠══════════════════════════════════════════════════════════════╣")
        lines.append("║ 已解锁成就：                                                  ║")
        
        if not unlocked:
            lines.append("║   (暂无)                                                      ║")
        else:
            for ach_id in unlocked[-5:]:  # 显示最近5个
                ach = self.ACHIEVEMENTS.get(ach_id)
                if ach:
                    lines.append(f"║   {ach['name']:<54}║")
        
        lines.append("╚══════════════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)
    
    def get_xp_from_achievements(self) -> int:
        """计算已解锁成就的总XP奖励"""
        total = 0
        for ach_id in self.state["unlocked"]:
            ach = self.ACHIEVEMENTS.get(ach_id)
            if ach:
                total += ach.get("xp_reward", 0)
        return total


def main():
    import argparse
    parser = argparse.ArgumentParser(description="成就系统")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=["unlock", "progress", "status", "list"], required=True)
    parser.add_argument("--achievement")
    parser.add_argument("--value", type=int)
    
    args = parser.parse_args()
    system = AchievementSystem(args.base_dir)
    
    if args.action == "unlock":
        result = system.unlock(args.achievement)
        if result:
            print(f"🎉 成就解锁：{result['name']}")
            print(f"   {result['description']}")
            print(f"   +{result['xp_reward']} XP")
        else:
            print("⚠️ 成就已解锁或不存在")
    
    elif args.action == "progress":
        system.update_progress(args.achievement, args.value)
        print(f"✅ 进度更新：{args.achievement} = {args.value}")
    
    elif args.action == "status":
        print(system.get_status())
    
    elif args.action == "list":
        print("📋 所有成就：")
        for ach in system.ACHIEVEMENTS.values():
            unlocked = "✅" if ach["id"] in system.state["unlocked"] else "🔒"
            print(f"  {unlocked} {ach['name']}: {ach['description']} (+{ach['xp_reward']} XP)")


if __name__ == "__main__":
    main()
