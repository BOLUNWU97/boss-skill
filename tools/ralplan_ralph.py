#!/usr/bin/env python3
"""
Ralplan + Ralph 双层执行模式管理器
借鉴 oh-my-codex 的双层执行架构
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

class RalplanRalphManager:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.state_file = self.base_dir / ".boss" / "ralph_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "current_mode": None,  # ralplan | ralph | direct
            "current_boss": None,
            "current_task": None,
            "ralplan_history": [],
            "ralph_progress": {},
            "last_updated": None
        }
    
    def _save_state(self):
        self.state["last_updated"] = datetime.now().isoformat()
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
    
    def set_mode(self, mode: str, boss: str = None, task: str = None):
        """切换执行模式"""
        valid_modes = ["ralplan", "ralph", "direct"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode. Choose from: {valid_modes}")
        
        self.state["current_mode"] = mode
        if boss:
            self.state["current_boss"] = boss
        if task:
            self.state["current_task"] = task
        self._save_state()
        
        return self._format_mode_intro(mode, boss)
    
    def _format_mode_intro(self, mode: str, boss: str = None) -> str:
        boss_name = boss or "老板"
        
        if mode == "ralplan":
            return f"""
╔══════════════════════════════════════════════════════════════╗
║              🎭 Ralplan 模式 - 方案审批                        ║
╠══════════════════════════════════════════════════════════════╣
║ 角色：{boss_name}正在审阅你的方案                               ║
║ 任务：挑刺、质疑、追问数据、挑战假设                           ║
║ 目标：只有完美的方案才能通过                                   ║
╠══════════════════════════════════════════════════════════════╣
║ 发送你的方案/周报/文档，{boss_name}会连环追问                  ║
║ 输入 'exit' 切换回直接对线模式                                  ║
╚══════════════════════════════════════════════════════════════╝
"""
        elif mode == "ralph":
            return f"""
╔══════════════════════════════════════════════════════════════╗
║              ⚡ Ralph 模式 - 任务施压                          ║
╠══════════════════════════════════════════════════════════════╣
║ 角色：{boss_name}在追问你的任务进度                             ║
║ 任务：质疑延迟、追问完成定义、给出指令                         ║
║ 目标：推动任务高效完成                                         ║
╠══════════════════════════════════════════════════════════════╣
║ 汇报你的任务进展，{boss_name}会连环追问                          ║
║ 输入 'exit' 切换回直接对线模式                                  ║
╚══════════════════════════════════════════════════════════════╝
"""
        else:
            return f"""
╔══════════════════════════════════════════════════════════════╗
║              💬 直接对线模式                                    ║
╠══════════════════════════════════════════════════════════════╣
║ 模式：直接与{boss_name}对线                                     ║
║ 输入 'ralplan' 切换到方案审批模式                               ║
║ 输入 'ralph' 切换到任务施压模式                                 ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    def log_ralplan(self, content: str, verdict: str, feedback: str):
        """记录一次ralplan审查"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "verdict": verdict,
            "feedback": feedback
        }
        self.state["ralplan_history"].append(entry)
        self._save_state()
    
    def log_ralph_progress(self, task: str, progress: int, issues: list):
        """记录任务进度"""
        self.state["ralph_progress"][task] = {
            "progress": progress,
            "issues": issues,
            "last_update": datetime.now().isoformat()
        }
        self._save_state()
    
    def get_status(self) -> str:
        """获取当前状态"""
        mode = self.state.get("current_mode", "direct")
        boss = self.state.get("current_boss", "unknown")
        
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║           🎭 Ralplan + Ralph 双层模式状态                    ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 当前模式：{(mode or 'None'):^50}║",
            f"║ 当前老板：{(boss or 'None'):^50}║",
        ]
        
        if mode == "ralplan":
            history_count = len(self.state.get("ralplan_history", []))
            lines.append(f"║ 审阅次数：{history_count:^50}║")
        elif mode == "ralph":
            tasks = self.state.get("ralph_progress", {})
            lines.append(f"║ 追踪任务：{len(tasks):^50}║")
        
        lines.extend([
            "╚══════════════════════════════════════════════════════════════╝"
        ])
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Ralplan + Ralph 双层执行模式管理器")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=["mode", "status", "log-ralplan", "log-ralph", "reset"], required=True)
    parser.add_argument("--mode", choices=["ralplan", "ralph", "direct"])
    parser.add_argument("--boss")
    parser.add_argument("--task")
    parser.add_argument("--content")
    parser.add_argument("--verdict")
    parser.add_argument("--feedback")
    parser.add_argument("--progress", type=int)
    parser.add_argument("--issues", nargs="*")
    
    args = parser.parse_args()
    
    manager = RalplanRalphManager(args.base_dir)
    
    if args.action == "mode":
        result = manager.set_mode(args.mode, args.boss, args.task)
        print(result)
    
    elif args.action == "status":
        print(manager.get_status())
    
    elif args.action == "log-ralplan":
        manager.log_ralplan(args.content, args.verdict, args.feedback)
        print("✅ Ralplan 记录已保存")
    
    elif args.action == "log-ralph":
        manager.log_ralph_progress(args.task, args.progress, args.issues)
        print("✅ Ralph 进度已记录")
    
    elif args.action == "reset":
        manager.state = {"current_mode": None, "current_boss": None, "current_task": None}
        manager._save_state()
        print("✅ 状态已重置")


if __name__ == "__main__":
    main()
