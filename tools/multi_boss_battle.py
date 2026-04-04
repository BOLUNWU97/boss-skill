#!/usr/bin/env python3
"""
Boss Skill Multi-Boss Battle
多老板对战模式：模拟你和老板A vs 老板B的场景
"""

import json
import random
from datetime import datetime, timezone
from pathlib import Path


class MultiBossBattle:
    """
    多老板对战系统
    
    场景示例：
    - "你是小王，你的老板是老王和李姐，你想争取晋升，
      需要同时应对老王的结果导向和李姐的逻辑追问"
    
    训练目标：
    - 学会在不同老板之间周旋
    - 学会应对不同风格的施压
    - 学会借力打力
    """
    
    def __init__(self, base_dir: str = "./bosses"):
        self.base_dir = Path(base_dir)
        self.battles = []
    
    def load_boss(self, slug: str) -> dict:
        """加载老板数据"""
        meta_file = self.base_dir / slug / "meta.json"
        if not meta_file.exists():
            return None
        
        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_bosses(self) -> list:
        """列出所有可用的老板"""
        bosses = []
        if not self.base_dir.exists():
            return bosses
        
        for d in self.base_dir.iterdir():
            if d.is_dir() and (d / "meta.json").exists():
                meta = self.load_boss(d.name)
                if meta:
                    bosses.append(meta)
        return bosses
    
    def create_battle(self, user_profile: str, boss_slugs: list, 
                     goal: str, tension_level: str = "high") -> dict:
        """
        创建对战场景
        
        user_profile: 你的角色
        - "小王" / "李四" / "张工"
        
        boss_slugs: 参与的老板列表
        - ["example_wang", "example_li"]
        
        goal: 你想达成的目标
        - "争取晋升" / "请假一周" / "调薪30%"
        
        tension_level: 紧张程度
        - "low" / "medium" / "high" / "extreme"
        """
        bosses = []
        for slug in boss_slugs:
            boss = self.load_boss(slug)
            if boss:
                bosses.append(boss)
        
        if not bosses:
            return {"error": "没有找到指定的老板"}
        
        battle = {
            "battle_id": f"battle_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_profile": user_profile,
            "bosses": bosses,
            "goal": goal,
            "tension_level": tension_level,
            "rounds": [],
            "current_round": 0,
            "status": "ongoing"
        }
        
        self.battles.append(battle)
        return battle
    
    def generate_scenario(self, battle: dict) -> str:
        """生成对战场景描述"""
        boss_names = [b["name"] for b in battle["bosses"]]
        boss_list = "、".join(boss_names)
        
        tension_descriptions = {
            "low": "气氛相对轻松",
            "medium": "气氛有些紧张",
            "high": "气氛非常紧张",
            "extreme": "简直是修罗场"
        }
        
        scenario = f"""
{'='*60}
🎭 多老板对战场景

👤 你的角色：{battle['user_profile']}
👔 老板阵容：{boss_list}
🎯 你的目标：{battle['goal']}
⏱️ 紧张程度：{tension_descriptions[battle['tension_level']]}

老板档案：
"""
        
        for boss in battle["bosses"]:
            scenario += f"""
【{boss['name']}】
  Nightmare Level: {boss.get('tags', {}).get('nightmare_level', 'N/A')}
  管理风格: {', '.join(boss.get('tags', {}).get('management_style', [])[:3])}
  类型: {'轰炸型' if '轰炸' in str(boss.get('tags', {}).get('management_style', [])) else '冷处理型'}
"""
        
        scenario += f"""

{'='*60}
开始对战！
"""
        
        return scenario
    
    def simulate_round(self, battle: dict, user_action: str) -> dict:
        """
        模拟一轮对战
        
        user_action: 你说的话/做的事
        
        返回：
        - boss_responses: 老板们的反应
        - pressure_assessment: 压力评估
        - next_suggestion: 建议下一步
        """
        round_result = {
            "round": battle["current_round"] + 1,
            "user_action": user_action,
            "boss_responses": [],
            "pressure_assessment": {},
            "survival_score": 0
        }
        
        # 模拟每个老板的反应
        for boss in battle["bosses"]:
            nightmare = float(boss.get("tags", {}).get("nightmare_level", "3").split("/")[0])
            style = boss.get("tags", {}).get("management_style", [])
            
            # 根据nightmare level和user_action生成反应
            if nightmare >= 4.5:
                response = self._generate_wang_response(user_action, boss)
            elif nightmare >= 4.0:
                response = self._generate_li_response(user_action, boss)
            else:
                response = self._generate_normal_response(user_action, boss)
            
            round_result["boss_responses"].append({
                "boss_name": boss["name"],
                "response": response,
                "pressure_level": random.uniform(0.6, 0.95) if nightmare >= 4 else random.uniform(0.3, 0.7)
            })
            
            # 计算生存分数
            survival = self._calculate_survival_score(user_action, boss, response)
            round_result["survival_score"] += survival
        
        # 归一化生存分数
        round_result["survival_score"] /= len(battle["bosses"])
        
        battle["current_round"] += 1
        battle["rounds"].append(round_result)
        
        return round_result
    
    def _generate_wang_response(self, user_action: str, boss: dict) -> str:
        """生成老王式反应"""
        responses = [
            "impact 是什么？数据呢？",
            "不够好。回去重写。",
            "给我24小时，我要看到结果。",
            "为什么之前没想到这个问题？",
            "这不是我想要的。",
            "你保证能完成吗？",
        ]
        return random.choice(responses)
    
    def _generate_li_response(self, user_action: str, boss: dict) -> str:
        """生成李姐式反应"""
        responses = [
            "说说看，你的思路是什么？",
            "我不理解。你再解释一下。",
            "这个判断依据是什么？",
            "逻辑不够清晰。",
            "你有验证过吗？",
            "结论呢？数据呢？",
        ]
        return random.choice(responses)
    
    def _generate_normal_response(self, user_action: str, boss: dict) -> str:
        """生成普通老板反应"""
        responses = [
            "好的，我知道了。",
            "这个可以考虑。",
            "下次注意。",
        ]
        return random.choice(responses)
    
    def _calculate_survival_score(self, user_action: str, boss: dict, response: str) -> float:
        """
        计算生存分数
        
        基于你说的话是否应对了老板的追问
        """
        # 关键词匹配
        good_responses = {
            "impact": ["impact", "影响", "收益", "价值"],
            "data": ["数据", "数字", "指标", "量化"],
            "timeline": ["时间", "deadline", "完成", "计划"],
            "solution": ["方案", "解决", "处理", "应对"],
        }
        
        score = 0.5  # 基础分
        
        # 如果老板追问了，你有数据/方案/时间线吗？
        for key, keywords in good_responses.items():
            if any(k in response for k in ["呢", "什么", "吗"]) and any(kw in user_action for kw in keywords):
                score += 0.1
        
        return min(score, 1.0)
    
    def generate_final_report(self, battle: dict) -> str:
        """生成对战总结报告"""
        total_rounds = len(battle["rounds"])
        if total_rounds == 0:
            return "还没开始对战"
        
        avg_survival = sum(r["survival_score"] for r in battle["rounds"]) / total_rounds
        best_round = max(battle["rounds"], key=lambda x: x["survival_score"])
        
        report = f"""
{'='*60}
📊 对战总结报告

👤 角色：{battle['user_profile']}
🎯 目标：{battle['goal']}

📈 生存分数：{avg_survival:.1%}
🏆 最佳表现：第{best_round['round']}轮 ({best_round['survival_score']:.1%})

💪 生存建议：
"""
        
        if avg_survival >= 0.8:
            report += """
✅ 你很会应对老板！
  - 继续保持
  - 可以挑战更高难度
"""
        elif avg_survival >= 0.5:
            report += """
⚠️ 基本能应对
  - 注意老板的追问模式
  - 准备更多数据和方案支撑
"""
        else:
            report += """
❌ 需要提升
  - 学会先说结论
  - 永远准备数据和备选方案
  - 不要只说"尽力了"
"""
        
        return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Multi-Boss Battle")
    parser.add_argument("--base-dir", default="./bosses")
    parser.add_argument("--action", choices=["list", "create", "simulate", "report"])
    parser.add_argument("--user", help="你的角色")
    parser.add_argument("--bosses", nargs="+", help="老板slug列表")
    parser.add_argument("--goal", help="你的目标")
    parser.add_argument("--tension", default="high", choices=["low", "medium", "high", "extreme"])
    parser.add_argument("--your-action", help="你说的话")
    parser.add_argument("--battle-id", help="对战ID")
    
    args = parser.parse_args()
    battle_system = MultiBossBattle(args.base_dir)
    
    if args.action == "list":
        bosses = battle_system.list_bosses()
        print(f"可用老板 ({len(bosses)}个):")
        for b in bosses:
            print(f"  - {b['slug']}: {b['name']}")
    
    elif args.action == "create":
        if not all([args.user, args.bosses, args.goal]):
            print("错误：create需要 --user --bosses --goal")
            return
        
        battle = battle_system.create_battle(args.user, args.bosses, args.goal, args.tension)
        if "error" in battle:
            print(f"错误：{battle['error']}")
            return
        
        print(f"✅ 对战创建成功！")
        print(f"   对战ID: {battle['battle_id']}")
        print(battle_system.generate_scenario(battle))
    
    elif args.action == "simulate":
        if not args.your_action:
            print("错误：simulate需要 --your-action")
            return
        
        # 找到最新的对战
        if not battle_system.battles:
            print("错误：没有找到对战，请先创建")
            return
        
        battle = battle_system.battles[-1]
        result = battle_system.simulate_round(battle, args.your_action)
        
        print(f"\n第{result['round']}轮：")
        print(f"你的行动：{result['user_action']}")
        for r in result["boss_responses"]:
            print(f"\n{r['boss_name']}: {r['response']}")
        print(f"\n🏆 生存分数：{result['survival_score']:.1%}")
    
    elif args.action == "report":
        if not battle_system.battles:
            print("错误：没有找到对战")
            return
        
        battle = battle_system.battles[-1]
        print(battle_system.generate_final_report(battle))


if __name__ == "__main__":
    main()
