#!/usr/bin/env python3
"""
Boss Skill Cost Tracker
追踪API调用成本，实时显示费用
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class CostEntry:
    """单次API调用记录"""
    timestamp: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    duration_ms: int
    session_id: str
    action_type: str  # evolve/feedback/battle/chat


class CostTracker:
    """
    Claude Code风格的成本追踪器
    
    特性：
    - 实时累计成本
    - 分session追踪
    - 分action类型统计
    - 支持状态保存和恢复
    """
    
    # 模型价格（$/1M tokens）
    MODEL_PRICES = {
        "claude-3-5-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-opus": {"input": 15.0, "output": 75.0},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "default": {"input": 1.0, "output": 5.0},
    }
    
    def __init__(self, boss_slug: str, base_dir: str = "./bosses"):
        self.boss_slug = boss_slug
        self.base_dir = Path(base_dir)
        self.cost_dir = self.base_dir / boss_slug / "costs"
        self.cost_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_file = self.cost_dir / "sessions.jsonl"
        self.state_file = self.cost_dir / "state.json"
        
        self.current_session = self._load_or_create_session()
        self.entries = []
    
    def _load_or_create_session(self) -> dict:
        """加载或创建session"""
        session_id = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        
        if self.session_file.exists():
            # 读取已有sessions
            sessions = self._read_sessions()
            if sessions:
                last_session = sessions[-1]
                # 如果last session是今天的，继续使用
                if last_session["session_id"].startswith(
                    datetime.now(timezone.utc).strftime('%Y%m%d')
                ):
                    return last_session
        
        # 创建新session
        return {
            "session_id": session_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "total_cost": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_calls": 0,
            "actions": {}
        }
    
    def _read_sessions(self) -> list:
        """读取所有sessions"""
        if not self.session_file.exists():
            return []
        
        sessions = []
        with open(self.session_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    sessions.append(json.loads(line))
        return sessions
    
    def _save_session(self):
        """保存当前session到文件"""
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(self.current_session, ensure_ascii=False) + "\n")
    
    def _save_state(self):
        """保存状态（用于恢复）"""
        state = {
            "session_id": self.current_session["session_id"],
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "total_cost": self.current_session["total_cost"]
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def calculate_cost(self, model: str, input_tokens: int, 
                     output_tokens: int) -> float:
        """计算API调用成本"""
        prices = self.MODEL_PRICES.get(model, self.MODEL_PRICES["default"])
        input_cost = (input_tokens / 1_000_000) * prices["input"]
        output_cost = (output_tokens / 1_000_000) * prices["output"]
        return round(input_cost + output_cost, 6)
    
    def record(self, model: str, input_tokens: int, output_tokens: int,
              duration_ms: int, action_type: str = "chat") -> CostEntry:
        """记录一次API调用"""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        entry = CostEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            duration_ms=duration_ms,
            session_id=self.current_session["session_id"],
            action_type=action_type
        )
        
        self.entries.append(entry)
        
        # 更新session统计
        self.current_session["total_cost"] += cost
        self.current_session["total_input_tokens"] += input_tokens
        self.current_session["total_output_tokens"] += output_tokens
        self.current_session["total_calls"] += 1
        
        if action_type not in self.current_session["actions"]:
            self.current_session["actions"][action_type] = {
                "count": 0, "cost": 0.0
            }
        self.current_session["actions"][action_type]["count"] += 1
        self.current_session["actions"][action_type]["cost"] += cost
        
        return entry
    
    def get_session_cost(self) -> dict:
        """获取当前session的累计成本"""
        return {
            "session_id": self.current_session["session_id"],
            "total_cost": round(self.current_session["total_cost"], 6),
            "total_input_tokens": self.current_session["total_input_tokens"],
            "total_output_tokens": self.current_session["total_output_tokens"],
            "total_calls": self.current_session["total_calls"],
            "actions": self.current_session["actions"],
            "duration": sum(e.duration_ms for e in self.entries) if self.entries else 0
        }
    
    def format_cost_display(self) -> str:
        """格式化成本显示（Claude Code风格）"""
        cost = self.get_session_cost()
        
        lines = [
            "┌─────────────────────────────────────────┐",
            "│         Boss Skill Cost Tracker           │",
            "└─────────────────────────────────────────┘",
            f"│ Session: {cost['session_id']:<27} │",
            f"│ Total Cost: ${cost['total_cost']:<25.6f} │",
            f"│ Total Calls: {cost['total_calls']:<24} │",
            "├─────────────────────────────────────────┤",
            "│ Tokens:                                   │",
            f"│   Input:  {cost['total_input_tokens']:<25,} │",
            f"│   Output: {cost['total_output_tokens']:<25,} │",
        ]
        
        if cost["actions"]:
            lines.append("├─────────────────────────────────────────┤")
            lines.append("│ By Action Type:                            │")
            for action, stats in cost["actions"].items():
                lines.append(
                    f"│   {action:<8}: ${stats['cost']:.6f} ({stats['count']} calls)"
                )
        
        lines.append("└─────────────────────────────────────────┘")
        
        return "\n".join(lines)
    
    def save_and_close(self):
        """保存并关闭"""
        self._save_session()
        self._save_state()
    
    def get_all_time_cost(self) -> dict:
        """获取所有时间的累计成本"""
        sessions = self._read_sessions()
        
        total_cost = sum(s["total_cost"] for s in sessions)
        total_calls = sum(s["total_calls"] for s in sessions)
        
        return {
            "total_cost": round(total_cost, 6),
            "total_sessions": len(sessions),
            "total_calls": total_calls,
            "avg_cost_per_session": round(total_cost / max(len(sessions), 1), 6)
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Cost Tracker")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--base-dir", default="./bosses")
    parser.add_argument("--action", choices=["record", "show", "history", "stats"])
    parser.add_argument("--model", default="claude-3-5-sonnet")
    parser.add_argument("--input-tokens", type=int, default=1000)
    parser.add_argument("--output-tokens", type=int, default=500)
    parser.add_argument("--duration-ms", type=int, default=1000)
    parser.add_argument("--action-type", default="chat")
    
    args = parser.parse_args()
    tracker = CostTracker(args.slug, args.base_dir)
    
    if args.action == "record":
        entry = tracker.record(
            args.model,
            args.input_tokens,
            args.output_tokens,
            args.duration_ms,
            args.action_type
        )
        print(f"✅ 记录成功")
        print(f"   Cost: ${entry.cost_usd:.6f}")
        print(f"   Total: ${tracker.current_session['total_cost']:.6f}")
    
    elif args.action == "show":
        print(tracker.format_cost_display())
    
    elif args.action == "history":
        sessions = tracker._read_sessions()
        print(f"\n📊 历史 Sessions ({len(sessions)} 个):\n")
        for s in sessions[-10:]:
            print(f"  {s['session_id']}: ${s['total_cost']:.6f} ({s['total_calls']} calls)")
    
    elif args.action == "stats":
        all_time = tracker.get_all_time_cost()
        current = tracker.get_session_cost()
        print(f"""
📊 Boss Skill Cost Statistics

当前 Session:
  ID: {current['session_id']}
  Cost: ${current['total_cost']:.6f}
  Calls: {current['total_calls']}

所有时间:
  Total Cost: ${all_time['total_cost']:.6f}
  Total Sessions: {all_time['total_sessions']}
  Total Calls: {all_time['total_calls']}
  Avg/Session: ${all_time['avg_cost_per_session']:.6f}
""")


if __name__ == "__main__":
    main()
