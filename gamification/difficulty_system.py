#!/usr/bin/env python3
"""
难度等级系统 - Boss Difficulty System
可选1-5级，老板从"温和"到"窒息"
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class DifficultySystem:
    """难度等级系统"""
    
    # 难度等级定义
    LEVELS = {
        1: {
            "name": "🌱 萌新",
            "description": "温和型老板，鼓励为主",
            "nightmare_modifier": -1.5,
            "pressure_modifier": -3,
            "praise_chance": 0.4,  # 40%概率会说好话
            "patience": 5,  # 初始耐心值
            "timeout_bonus": 2,  # 延期容忍度
        },
        2: {
            "name": "🐣 入门",
            "description": "正常老板，有要求但合理",
            "nightmare_modifier": -0.5,
            "pressure_modifier": -1,
            "praise_chance": 0.25,
            "patience": 4,
            "timeout_bonus": 1,
        },
        3: {
            "name": "💼 正常",
            "description": "标准老板，职场常态",
            "nightmare_modifier": 0,
            "pressure_modifier": 0,
            "praise_chance": 0.15,
            "patience": 3,
            "timeout_bonus": 0,
        },
        4: {
            "name": "🔥 地狱",
            "description": "高压老板，问题不断",
            "nightmare_modifier": +0.5,
            "pressure_modifier": +2,
            "praise_chance": 0.08,
            "patience": 2,
            "timeout_bonus": -1,
        },
        5: {
            "name": "☠️ 窒息",
            "description": "究极老板，极限挑战",
            "nightmare_modifier": +1.5,
            "pressure_modifier": +4,
            "praise_chance": 0.02,
            "patience": 1,
            "timeout_bonus": -2,
        },
    }
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.state_file = self.base_dir / ".boss" / "difficulty_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "current_level": 3,  # 默认正常难度
            "player_xp": 0,
            "player_level": 1,
            "boss_levels": {},  # 每个老板的难度设置
        }
    
    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
    
    def get_level(self, boss_slug: str = None) -> dict:
        """获取当前难度等级配置"""
        if boss_slug and boss_slug in self.state.get("boss_levels", {}):
            level = self.state["boss_levels"][boss_slug]
        else:
            level = self.state.get("current_level", 3)
        return self.LEVELS.get(level, self.LEVELS[3])
    
    def set_level(self, level: int, boss_slug: str = None) -> dict:
        """设置难度等级"""
        if level not in self.LEVELS:
            raise ValueError(f"Invalid level. Choose from: {list(self.LEVELS.keys())}")
        
        if boss_slug:
            if "boss_levels" not in self.state:
                self.state["boss_levels"] = {}
            self.state["boss_levels"][boss_slug] = level
        else:
            self.state["current_level"] = level
        
        self._save_state()
        return self.get_level(boss_slug)
    
    def add_xp(self, amount: int) -> dict:
        """增加经验值，可能触发升级"""
        self.state["player_xp"] += amount
        
        # 检查升级
        xp_needed = self.state["player_level"] * 100
        upgrades = 0
        while self.state["player_xp"] >= xp_needed:
            self.state["player_xp"] -= xp_needed
            self.state["player_level"] += 1
            upgrades += 1
            xp_needed = self.state["player_level"] * 100
        
        self._save_state()
        
        return {
            "xp_gained": amount,
            "total_xp": self.state["player_xp"],
            "level": self.state["player_level"],
            "xp_needed": xp_needed,
            "upgrades": upgrades,
        }
    
    def get_status(self) -> str:
        """获取当前状态"""
        level_info = self.get_level()
        player_level = self.state["player_level"]
        player_xp = self.state["player_xp"]
        xp_needed = player_level * 100
        
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║              🎮 难度等级 & 玩家状态                          ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 当前难度：{level_info['name']:<45}║",
            f"║ 难度描述：{level_info['description']:<43}║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 👤 玩家等级：Lv.{player_level:<45}║",
            f"║ ✨ 经验值：{player_xp}/{xp_needed:<41}║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║  难度等级说明：                                              ║",
            "║  1🌱萌新 - 鼓励为主，新手入门                              ║",
            "║  2🐣入门 - 正常要求，合理反馈                              ║",
            "║  3💼正常 - 标准老板，职场常态                              ║",
            "║  4🔥地狱 - 高压追问，问题不断                              ║",
            "║  5☠️窒息 - 究极挑战，极限测试                              ║",
            "╚══════════════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="难度等级系统")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=["get", "set", "xp", "status"], required=True)
    parser.add_argument("--level", type=int, choices=[1, 2, 3, 4, 5])
    parser.add_argument("--boss")
    parser.add_argument("--xp", type=int)
    
    args = parser.parse_args()
    system = DifficultySystem(args.base_dir)
    
    if args.action == "get":
        print(system.get_level(args.boss))
    
    elif args.action == "set":
        level_info = system.set_level(args.level, args.boss)
        print(f"✅ 难度已设置为：{level_info['name']}")
    
    elif args.action == "xp":
        result = system.add_xp(args.xp)
        print(f"✅ +{args.xp} XP")
        if result['upgrades'] > 0:
            print(f"🎉 升级！当前 Lv.{result['level']}")
        print(f"📊 {result['total_xp']}/{result['xp_needed']} XP")
    
    elif args.action == "status":
        print(system.get_status())


if __name__ == "__main__":
    main()
