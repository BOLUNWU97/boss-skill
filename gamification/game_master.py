#!/usr/bin/env python3
"""
Game Master - 游戏化系统总入口
整合难度、成就、情绪三大系统
"""

import sys
import os
from pathlib import Path

# 添加上级目录到路径以便导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from gamification.difficulty_system import DifficultySystem
from gamification.achievement_system import AchievementSystem
from gamification.emotion_system import EmotionSystem

class GameMaster:
    """
    游戏大师 - 总控制系统
    整合难度等级、成就系统、情绪系统
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.difficulty = DifficultySystem(base_dir)
        self.achievement = AchievementSystem(base_dir)
        self.emotion = EmotionSystem(base_dir)
    
    def record_battle_start(self, boss_slug: str):
        """记录开始对线"""
        # 每次对线开始时随机决定初始情绪
        import random
        emotions = ["neutral", "neutral", "happy", "anxious", "anxious"]
        emotion = random.choice(emotions)
        self.emotion.set_emotion(emotion)
        
        # 检查并解锁相关成就
        self.achievement.check_and_unlock("first_boss")
        self.achievement.update_progress("battle_10", 
            len(self.achievement.state.get("progress", {}).get("battle_10", [])))
    
    def record_good_response(self, boss_slug: str):
        """记录好的回应"""
        self.emotion.record_good_response()
        
        # 检查完美应对成就
        progress = self.achievement.state.get("progress", {}).get("perfect_response", 0)
        progress += 1
        self.achievement.update_progress("perfect_response", progress)
        
        if progress >= 3:
            self.achievement.unlock("perfect_response")
    
    def record_data_response(self, boss_slug: str):
        """记录数据化回答"""
        self.emotion.record_data_response()
        
        # 数据大师
        progress = self.achievement.state.get("progress", {}).get("data_master", 0)
        progress += 1
        self.achievement.update_progress("data_master", progress)
        
        if progress >= 5:
            self.achievement.unlock("data_master")
    
    def record_mistake(self, boss_slug: str):
        """记录失误"""
        self.emotion.record_mistake()
    
    def calculate_pressure(self, base_pressure: float) -> float:
        """计算实际压力（考虑情绪和难度）"""
        emotion_modifier = self.emotion.get_pressure_modifier()
        level_info = self.difficulty.get_level()
        
        return base_pressure * emotion_modifier * (1 + level_info.get("pressure_modifier", 0) * 0.1)
    
    def add_xp(self, amount: int):
        """增加经验值"""
        result = self.difficulty.add_xp(amount)
        
        # 检查升级成就
        if result['upgrades'] > 0:
            self.achievement.unlock("survive_10m")  # 简单起见，升级就当存活过
    
    def check_battle_achievements(self, battle_count: int):
        """检查对线相关成就"""
        if battle_count >= 1:
            self.achievement.check_and_unlock("first_boss")
        if battle_count >= 10:
            self.achievement.unlock("battle_10")
        if battle_count >= 50:
            self.achievement.unlock("battle_50")
        if battle_count >= 100:
            self.achievement.unlock("battle_100")
    
    def get_full_status(self) -> str:
        """获取完整状态"""
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║               🎮 游戏大师 - 全状态面板                       ║",
            "╠══════════════════════════════════════════════════════════════╣",
        ]
        
        # 难度信息
        level_info = self.difficulty.get_level()
        lines.append(f"║ 🎚️  难度等级：{level_info['name']:<45}║")
        
        # 玩家状态
        lines.append(f"║ 👤 玩家等级：Lv.{self.difficulty.state['player_level']:<44}║")
        lines.append(f"║ ✨ 经验值：{self.difficulty.state['player_xp']}/{self.difficulty.state['player_level']*100} XP{' '*38}║")
        
        # 情绪状态
        emotion = self.emotion.get_emotion()
        lines.append(f"║ 😤 老板情绪：{emotion['name']:<45}║")
        lines.append(f"║    压力倍数：×{emotion['pressure_multiplier']:<47}║")
        
        # 成就
        unlocked_count = len(self.achievement.state["unlocked"])
        total_count = len(self.achievement.ACHIEVEMENTS)
        lines.append(f"║ 🏆 成就：{unlocked_count}/{total_count} 已解锁{' '*36}║")
        
        lines.extend([
            "╠══════════════════════════════════════════════════════════════╣",
            "║ 常用命令：                                                    ║",
            "║   /game status     - 查看完整状态                            ║",
            "║   /game difficulty - 设置难度(1-5)                           ║",
            "║   /game achievements - 查看成就                            ║",
            "║   /game emotion    - 查看老板情绪                            ║",
            "╚══════════════════════════════════════════════════════════════╝",
        ])
        
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="游戏大师")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=[
        "status", "difficulty", "achievements", "emotion",
        "start-battle", "good-response", "mistake", "data-response"
    ], required=True)
    parser.add_argument("--level", type=int)
    parser.add_argument("--boss")
    
    args = parser.parse_args()
    gm = GameMaster(args.base_dir)
    
    if args.action == "status":
        print(gm.get_full_status())
    
    elif args.action == "difficulty":
        if args.level:
            result = gm.difficulty.set_level(args.level, args.boss)
            print(f"✅ 难度已设置为：{result['name']}")
        else:
            print(gm.difficulty.get_status())
    
    elif args.action == "achievements":
        print(gm.achievement.get_status())
    
    elif args.action == "emotion":
        print(gm.emotion.get_status())
    
    elif args.action == "start-battle":
        gm.record_battle_start(args.boss or "unknown")
        print("⚔️ 对线开始！")
        print(gm.emotion.get_status())
    
    elif args.action == "good-response":
        gm.record_good_response(args.boss or "unknown")
        print("✅ 好的回应！老板稍微冷静了一点")
    
    elif args.action == "mistake":
        gm.record_mistake(args.boss or "unknown")
        print("❌ 失误！老板更生气了")
    
    elif args.action == "data-response":
        gm.record_data_response(args.boss or "unknown")
        print("📊 数据化回答！老板明显被安抚了")


if __name__ == "__main__":
    main()
