#!/usr/bin/env python3
"""
Boss Skill Evolution Logger
记录boss的进化事件，支持自我学习和回滚
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


class EvolutionLogger:
    """进化日志记录器"""
    
    def __init__(self, boss_slug: str, base_dir: str = "./bosses"):
        self.boss_slug = boss_slug
        self.base_dir = Path(base_dir)
        self.evolution_dir = self.base_dir / boss_slug / "evolutions"
        self.evolution_dir.mkdir(parents=True, exist_ok=True)
        
        # 日志文件
        self.log_file = self.evolution_dir / "evolution.jsonl"
        self.state_file = self.evolution_dir / "evolution_state.json"
        
    def log_event(self, event_type: str, data: dict, reason: str = "") -> str:
        """
        记录进化事件
        
        event_type:
        - correction: 用户纠正
        - pattern_detected: 检测到新模式
        - self_improvement: 自我改进
        - version_created: 新版本创建
        - rollback: 回滚
        """
        event = {
            "event_id": f"{event_type}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
            "reason": reason,
            "status": "pending"  # pending -> applied -> confirmed
        }
        
        # 追加写入JSONL
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        
        return event["event_id"]
    
    def log_correction(self, user_correction: str, context: str, 
                       before: str, after: str) -> str:
        """记录用户纠正"""
        return self.log_event("correction", {
            "user_correction": user_correction,
            "context": context,
            "before": before,
            "after": after
        }, reason=f"用户纠正: {user_correction[:50]}")
    
    def log_pattern(self, pattern: str, examples: list, confidence: float) -> str:
        """记录检测到的模式"""
        return self.log_event("pattern_detected", {
            "pattern": pattern,
            "examples": examples,
            "confidence": confidence
        }, reason=f"新模式: {pattern[:50]}")
    
    def log_self_improvement(self, improvement: str, 
                           trigger: str, result: str) -> str:
        """记录自我改进"""
        return self.log_event("self_improvement", {
            "improvement": improvement,
            "trigger": trigger,
            "result": result
        }, reason=f"自我改进: {improvement[:50]}")
    
    def create_version(self, version_name: str, note: str = "") -> str:
        """创建新版本快照"""
        version_dir = self.evolution_dir / "versions" / version_name
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制当前文件到版本目录
        boss_dir = self.base_dir / self.boss_slug
        for fname in ["SKILL.md", "management.md", "persona.md", "meta.json"]:
            src = boss_dir / fname
            if src.exists():
                import shutil
                shutil.copy2(src, version_dir / fname)
        
        # 记录版本创建
        event_id = self.log_event("version_created", {
            "version_name": version_name,
            "note": note,
            "files": [str(f) for f in version_dir.iterdir()]
        }, reason=f"创建版本: {version_name}")
        
        return event_id
    
    def get_evolution_log(self, event_type: str = None, limit: int = 50) -> list:
        """获取进化日志"""
        if not self.log_file.exists():
            return []
        
        events = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    if event_type is None or event["event_type"] == event_type:
                        events.append(event)
        
        return events[-limit:]
    
    def get_corrections(self) -> list:
        """获取所有纠正记录"""
        return self.get_evolution_log("correction")
    
    def get_patterns(self) -> list:
        """获取所有检测到的模式"""
        return self.get_evolution_log("pattern_detected")
    
    def summarize_evolution(self) -> dict:
        """总结进化状态"""
        corrections = self.get_corrections()
        patterns = self.get_patterns()
        
        return {
            "total_corrections": len(corrections),
            "total_patterns": len(patterns),
            "latest_correction": corrections[-1] if corrections else None,
            "latest_pattern": patterns[-1] if patterns else None,
            "log_file": str(self.log_file),
            "events_count": len(open(self.log_file).readlines()) if self.log_file.exists() else 0
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Evolution Logger")
    parser.add_argument("--action", required=True, 
                        choices=["log-correction", "log-pattern", "create-version", 
                                "show-log", "show-summary", "show-corrections"])
    parser.add_argument("--slug", required=True, help="Boss slug")
    parser.add_argument("--base-dir", default="./bosses", help="Base directory")
    parser.add_argument("--before", help="Before state (for correction)")
    parser.add_argument("--after", help="After state (for correction)")
    parser.add_argument("--context", help="Context of correction")
    parser.add_argument("--pattern", help="Pattern description")
    parser.add_argument("--examples", nargs="+", help="Pattern examples")
    parser.add_argument("--confidence", type=float, default=0.8, help="Confidence")
    parser.add_argument("--version", help="Version name")
    parser.add_argument("--note", help="Version note")
    parser.add_argument("--limit", type=int, default=50, help="Log limit")
    parser.add_argument("--user-correction", help="User correction text")
    
    args = parser.parse_args()
    logger = EvolutionLogger(args.slug, args.base_dir)
    
    if args.action == "log-correction":
        event_id = logger.log_correction(
            user_correction=args.user_correction or "",
            context=args.context or "",
            before=args.before or "",
            after=args.after or ""
        )
        print(f"记录纠正: {event_id}")
    
    elif args.action == "log-pattern":
        event_id = logger.log_pattern(
            pattern=args.pattern or "",
            examples=args.examples or [],
            confidence=args.confidence
        )
        print(f"记录模式: {event_id}")
    
    elif args.action == "create-version":
        event_id = logger.create_version(args.version, args.note or "")
        print(f"创建版本: {args.version}")
    
    elif args.action == "show-log":
        events = logger.get_evolution_log(limit=args.limit)
        for e in events:
            print(f"[{e['timestamp']}] {e['event_type']}: {e.get('reason', '')}")
    
    elif args.action == "show-corrections":
        corrections = logger.get_corrections()
        print(f"共 {len(corrections)} 条纠正记录:\n")
        for c in corrections:
            print(f"时间: {c['timestamp']}")
            print(f"纠正: {c['data'].get('user_correction', '')}")
            print(f"内容: {c['data'].get('before', '')} -> {c['data'].get('after', '')}")
            print()
    
    elif args.action == "show-summary":
        summary = logger.summarize_evolution()
        print(f"进化状态摘要:")
        print(f"  总纠正数: {summary['total_corrections']}")
        print(f"  总模式数: {summary['total_patterns']}")
        print(f"  日志文件: {summary['log_file']}")


if __name__ == "__main__":
    main()
