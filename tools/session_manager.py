#!/usr/bin/env python3
"""
Boss Skill Session Manager
会话管理：保存、恢复、自动保存
Claude Code风格
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, List


class SessionManager:
    """
    Claude Code风格的会话管理器
    
    特性：
    - 自动保存状态
    - 会话恢复
    - 会话历史
    - 自动备份
    """
    
    def __init__(self, boss_slug: str, base_dir: str = "./bosses"):
        self.boss_slug = boss_slug
        self.base_dir = Path(base_dir)
        self.session_dir = self.base_dir / boss_slug / ".sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session_file = self.session_dir / "current.json"
        self.session_index_file = self.session_dir / "index.jsonl"
        
        self.current_session = self._load_current_session()
    
    def _load_current_session(self) -> Dict:
        """加载当前会话"""
        if self.current_session_file.exists():
            with open(self.current_session_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # 创建新会话
        return self._create_new_session()
    
    def _create_new_session(self) -> Dict:
        """创建新会话"""
        session_id = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}"
        
        session = {
            "session_id": session_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "state": {
                "conversation": [],
                "corrections": [],
                "patterns": [],
                "nightmare_level": None,
                "pressure_index": 0.0,
                "version": "v1"
            },
            "metadata": {
                "boss_slug": self.boss_slug,
                "total_messages": 0,
                "total_corrections": 0,
                "total_evolutions": 0
            }
        }
        
        self._save_current_session(session)
        return session
    
    def _save_current_session(self, session: Optional[Dict] = None):
        """保存当前会话"""
        if session is None:
            session = self.current_session
        
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        with open(self.current_session_file, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
    
    def save_and_archive(self):
        """保存并归档当前会话"""
        # 保存到index
        with open(self.session_index_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(self.current_session, ensure_ascii=False) + "\n")
        
        # 备份文件
        backup_file = self.session_dir / f"backup_{self.current_session['session_id']}.json"
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(self.current_session, f, ensure_ascii=False, indent=2)
        
        # 创建新会话
        self.current_session = self._create_new_session()
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加对话消息"""
        message = {
            "role": role,  # "user" or "boss"
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        
        self.current_session["state"]["conversation"].append(message)
        self.current_session["metadata"]["total_messages"] += 1
        
        self._save_current_session()
    
    def add_correction(self, correction: str, context: str, 
                       before: str, after: str):
        """添加纠正记录"""
        entry = {
            "correction": correction,
            "context": context,
            "before": before,
            "after": after,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.current_session["state"]["corrections"].append(entry)
        self.current_session["metadata"]["total_corrections"] += 1
        
        self._save_current_session()
    
    def update_nightmare_level(self, level: float):
        """更新Nightmare Level"""
        self.current_session["state"]["nightmare_level"] = level
        self._save_current_session()
    
    def update_pressure_index(self, index: float):
        """更新压力指数"""
        self.current_session["state"]["pressure_index"] = index
        self._save_current_session()
    
    def increment_evolution(self):
        """增加进化次数"""
        self.current_session["metadata"]["total_evolutions"] += 1
        self._save_current_session()
    
    def get_state(self) -> Dict:
        """获取当前状态"""
        return self.current_session["state"]
    
    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        messages = self.current_session["state"]["conversation"]
        
        if not messages:
            return "Empty conversation"
        
        lines = [f"共 {len(messages)} 条消息:\n"]
        
        for i, msg in enumerate(messages[-10:], 1):
            role = "👤" if msg["role"] == "user" else "👔"
            content = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
            lines.append(f"  {i}. {role} {content}")
        
        return "\n".join(lines)
    
    def restore_session(self, session_id: str) -> bool:
        """恢复指定会话"""
        if not self.session_index_file.exists():
            return False
        
        with open(self.session_index_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    session = json.loads(line)
                    if session["session_id"] == session_id:
                        self.current_session = session
                        self._save_current_session()
                        return True
        
        return False
    
    def list_sessions(self, limit: int = 10) -> List[Dict]:
        """列出历史会话"""
        sessions = []
        
        if self.session_index_file.exists():
            with open(self.session_index_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        sessions.append(json.loads(line))
        
        # 添加当前会话
        sessions.append(self.current_session)
        
        # 按时间倒序
        sessions = sorted(sessions, 
                        key=lambda x: x.get("updated_at", ""), 
                        reverse=True)
        
        return sessions[:limit]
    
    def print_session_status(self):
        """打印当前会话状态"""
        s = self.current_session
        meta = s["metadata"]
        state = s["state"]
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  Boss Skill Session Status                   ║
╠══════════════════════════════════════════════════════════════╣
║ Session ID: {s['session_id']:<45}║
║ Created: {s['created_at']:<47}║
║ Updated: {s['updated_at']:<47}║
╠══════════════════════════════════════════════════════════════╣
║ Stats:                                                      ║
║   Messages: {meta['total_messages']:<47}║
║   Corrections: {meta['total_corrections']:<44}║
║   Evolutions: {meta['total_evolutions']:<44}║
╠══════════════════════════════════════════════════════════════╣
║ State:                                                      ║
║   Nightmare Level: {state.get('nightmare_level', 'N/A'):<39}║
║   Pressure Index: {state.get('pressure_index', 0):<40.1f}║
║   Version: {state.get('version', 'v1'):<47}║
╚══════════════════════════════════════════════════════════════╝
""")
        
        # 最近对话
        print("\n📝 Recent Conversation:")
        print(self.get_conversation_summary())


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Session Manager")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--base-dir", default="./bosses")
    parser.add_argument("--action", choices=[
        "status", "save", "archive", "list", "restore", "add-message"
    ])
    parser.add_argument("--session-id", help="Session ID for restore")
    parser.add_argument("--role", choices=["user", "boss"], help="Message role")
    parser.add_argument("--content", help="Message content")
    
    args = parser.parse_args()
    manager = SessionManager(args.slug, args.base_dir)
    
    if args.action == "status":
        manager.print_session_status()
    
    elif args.action == "save":
        manager._save_current_session()
        print("✅ Session saved")
    
    elif args.action == "archive":
        manager.save_and_archive()
        print("✅ Session archived and new session started")
    
    elif args.action == "list":
        sessions = manager.list_sessions()
        print(f"\n📋 Sessions ({len(sessions)}):\n")
        for s in sessions:
            print(f"  {s['session_id']}")
            print(f"    Updated: {s['updated_at']}")
            print(f"    Messages: {s['metadata']['total_messages']}")
            print()
    
    elif args.action == "restore":
        if not args.session_id:
            print("❌ Need --session-id")
            return
        if manager.restore_session(args.session_id):
            print(f"✅ Restored session {args.session_id}")
        else:
            print(f"❌ Session {args.session_id} not found")
    
    elif args.action == "add-message":
        if not args.role or not args.content:
            print("❌ Need --role and --content")
            return
        manager.add_message(args.role, args.content)
        print("✅ Message added")


if __name__ == "__main__":
    main()
