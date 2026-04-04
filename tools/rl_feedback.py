#!/usr/bin/env python3
"""
Boss Skill RL Feedback System
用RL思想追踪老板行为的好坏反馈
"""

import json
from datetime import datetime, timezone
from pathlib import Path


class RLFeedbackTracker:
    """
    RL反馈追踪器
    
    核心思想：
    - 每个老板行为 = 一个 "action"
    - 用户的反应 = "reward"
    - 累积的reward = 这个行为的"好坏"
    
    让老板越像真实的老板！
    """
    
    def __init__(self, boss_slug: str, base_dir: str = "./bosses"):
        self.boss_slug = boss_slug
        self.base_dir = Path(base_dir)
        self.feedback_file = self.base_dir / boss_slug / "evolutions" / "rl_feedback.jsonl"
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 行为评分表
        self.action_scores = self._load_action_scores()
    
    def _load_action_scores(self) -> dict:
        """加载已有的行为评分"""
        if not self.feedback_file.exists():
            return {}
        
        scores = {}
        with open(self.feedback_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    action = entry.get("action", "")
                    reward = entry.get("reward", 0)
                    if action:
                        if action not in scores:
                            scores[action] = []
                        scores[action].append(reward)
        return scores
    
    def record_action(self, action_type: str, context: str, 
                     user_reaction: str, reward: float) -> dict:
        """
        记录一个行为和它的反馈
        
        action_type: 行为类型
        - "追问" / "否定" / "沉默施压" / "威胁"
        - "表扬" / "中性"
        
        context: 场景描述
        
        user_reaction: 用户的反应
        - "对抗" / "顺从" / "沉默" / "反击"
        
        reward: 奖励值
        - 正数 = 这个行为"很像"真实老板
        - 负数 = 这个行为"不像"真实老板
        - 1.0 = 用户说"很像"
        - -1.0 = 用户说"一点都不像"
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action_type": action_type,
            "context": context[:100],  # 截断避免太长
            "user_reaction": user_reaction,
            "reward": reward,
            "cumulative_score": 0.0
        }
        
        # 计算累积分数
        if action_type in self.action_scores:
            self.action_scores[action_type].append(reward)
        else:
            self.action_scores[action_type] = [reward]
        
        entry["cumulative_score"] = sum(self.action_scores[action_type]) / len(self.action_scores[action_type])
        
        # 写入文件
        with open(self.feedback_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        return entry
    
    def get_behavior_grade(self, action_type: str) -> dict:
        """
        获取某个行为的评分
        
        返回：
        - score: 平均分 (-1 to 1)
        - count: 被评价次数
        - grade: 等级 (SSS/SS/S/A/B/C)
        """
        if action_type not in self.action_scores:
            return {"score": 0.0, "count": 0, "grade": "N/A"}
        
        scores = self.action_scores[action_type]
        avg = sum(scores) / len(scores)
        count = len(scores)
        
        # 评级
        if avg >= 0.9:
            grade = "SSS"
        elif avg >= 0.7:
            grade = "SS"
        elif avg >= 0.5:
            grade = "S"
        elif avg >= 0.3:
            grade = "A"
        elif avg >= 0.0:
            grade = "B"
        else:
            grade = "C"
        
        return {"score": avg, "count": count, "grade": grade}
    
    def get_all_behavior_grades(self) -> dict:
        """获取所有行为的评级"""
        grades = {}
        for action_type in self.action_scores:
            grades[action_type] = self.get_behavior_grade(action_type)
        return grades
    
    def suggest_actions(self) -> list:
        """
        基于RL反馈建议应该强化/弱化的行为
        
        返回：
        - 高分行为 = 应该更多使用
        - 低分行为 = 应该减少使用
        """
        suggestions = []
        
        for action_type, scores in self.action_scores.items():
            if len(scores) >= 3:  # 至少3次评价才建议
                avg = sum(scores) / len(scores)
                
                if avg >= 0.7:
                    suggestions.append({
                        "action": action_type,
                        "recommendation": "强化",
                        "reason": f"评分{avg:.2f}，用户反馈很像真实老板",
                        "priority": "high"
                    })
                elif avg <= 0.0:
                    suggestions.append({
                        "action": action_type,
                        "recommendation": "弱化",
                        "reason": f"评分{avg:.2f}，用户反馈不太像",
                        "priority": "high"
                    })
        
        # 按优先级排序
        return sorted(suggestions, key=lambda x: x["priority"] == "high", reverse=True)
    
    def print_feedback_report(self):
        """打印反馈报告"""
        grades = self.get_all_behavior_grades()
        suggestions = self.suggest_actions()
        
        print(f"\n📊 RL 反馈报告 - {self.boss_slug}")
        print("=" * 50)
        print("\n🎭 行为评分：")
        for action, info in grades.items():
            print(f"  {action}: {info['grade']} ({info['score']:.2f}) x{info['count']}")
        
        if suggestions:
            print("\n💡 进化建议：")
            for s in suggestions:
                print(f"  [{s['recommendation']}] {s['action']}: {s['reason']}")
        else:
            print("\n⏳ 收集更多反馈后给出建议")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill RL Feedback")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--base-dir", default="./bosses")
    parser.add_argument("--action", choices=["record", "report", "suggest"])
    parser.add_argument("--action-type", help="行为类型")
    parser.add_argument("--context", help="场景")
    parser.add_argument("--user-reaction", help="用户反应")
    parser.add_argument("--reward", type=float, help="奖励值 (-1 to 1)")
    
    args = parser.parse_args()
    tracker = RLFeedbackTracker(args.slug, args.base_dir)
    
    if args.action == "record":
        if not all([args.action_type, args.context, args.user_reaction, args.reward is not None]):
            print("错误：record需要 --action-type --context --user-reaction --reward")
            return
        
        entry = tracker.record_action(
            args.action_type,
            args.context,
            args.user_reaction,
            args.reward
        )
        print(f"✅ 已记录: {args.action_type} (reward={args.reward})")
        print(f"   累积评分: {entry['cumulative_score']:.2f}")
    
    elif args.action == "report":
        tracker.print_feedback_report()
    
    elif args.action == "suggest":
        suggestions = tracker.suggest_actions()
        if suggestions:
            print("进化建议：")
            for s in suggestions:
                print(f"  [{s['recommendation']}] {s['action']}")
        else:
            print("⏳ 数据不足，需要更多反馈")


if __name__ == "__main__":
    main()
