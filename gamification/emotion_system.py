#!/usr/bin/env python3
"""
情绪系统 - Boss Emotion System
老板有情绪波动，心情影响反应
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class EmotionSystem:
    """老板情绪系统"""
    
    # 情绪状态定义
    EMOTIONS = {
        "happy": {
            "name": "😊 心情好",
            "description": "老板今天心情不错",
            "pressure_multiplier": 0.7,  # 压力降低
            "praise_chance": 0.5,  # 更可能说好话
            "response_templates": [
                "嗯，不错。",
                "这个思路可以。",
                "还行，继续。",
            ],
        },
        "neutral": {
            "name": "😐 平常心",
            "description": "老板处于正常状态",
            "pressure_multiplier": 1.0,
            "praise_chance": 0.15,
            "response_templates": [
                "说说你的理由。",
                "为什么这么做？",
                "然后呢？",
            ],
        },
        "anxious": {
            "name": "😰 焦虑",
            "description": "老板有点焦虑",
            "pressure_multiplier": 1.3,
            "praise_chance": 0.05,
            "response_templates": [
                "这个能按时完成吗？",
                "时间够不够？",
                "有没有风险？",
            ],
        },
        "angry": {
            "name": "😡 生气",
            "description": "老板火气很大",
            "pressure_multiplier": 1.6,
            "praise_chance": 0.02,
            "response_templates": [
                "这都行？",
                "你认真的？",
                "重做。",
            ],
        },
        "furious": {
            "name": "🤬 暴怒",
            "description": "老板快炸了",
            "pressure_multiplier": 2.0,
            "praise_chance": 0.0,
            "response_templates": [
                "你是故意的吧？",
                "给我解释一下！",
                "这报告是认真的吗？！",
            ],
        },
    }
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.state_file = self.base_dir / ".boss" / "emotion_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {
            "current_emotion": "neutral",
            "emotion_history": [],
            "anger_accumulator": 0,  # 愤怒累积值
            "calmdown_timer": 0,  # 冷静倒计时
        }
    
    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))
    
    def get_emotion(self) -> dict:
        """获取当前情绪"""
        emotion_key = self.state.get("current_emotion", "neutral")
        return self.EMOTIONS.get(emotion_key, self.EMOTIONS["neutral"])
    
    def set_emotion(self, emotion: str) -> dict:
        """设置情绪"""
        if emotion not in self.EMOTIONS:
            raise ValueError(f"Invalid emotion. Choose from: {list(self.EMOTIONS.keys())}")
        
        old_emotion = self.state.get("current_emotion")
        self.state["current_emotion"] = emotion
        self.state["emotion_history"].append({
            "from": old_emotion,
            "to": emotion,
            "timestamp": datetime.now().isoformat(),
        })
        self._save_state()
        return self.EMOTIONS[emotion]
    
    def trigger_anger(self, intensity: int = 1) -> dict:
        """激怒老板"""
        self.state["anger_accumulator"] += intensity
        
        # 根据累积值决定情绪
        if self.state["anger_accumulator"] >= 8:
            new_emotion = "furious"
        elif self.state["anger_accumulator"] >= 5:
            new_emotion = "angry"
        elif self.state["anger_accumulator"] >= 3:
            new_emotion = "anxious"
        elif self.state["anger_accumulator"] <= -3:
            new_emotion = "happy"
        else:
            new_emotion = "neutral"
        
        return self.set_emotion(new_emotion)
    
    def calm_down(self, amount: int = 1) -> dict:
        """安抚老板"""
        self.state["anger_accumulator"] -= amount
        return self.set_emotion(self._calculate_emotion())
    
    def _calculate_emotion(self) -> str:
        """根据愤怒值计算情绪"""
        anger = self.state.get("anger_accumulator", 0)
        if anger >= 8:
            return "furious"
        elif anger >= 5:
            return "angry"
        elif anger >= 3:
            return "anxious"
        elif anger <= -3:
            return "happy"
        else:
            return "neutral"
    
    def record_mistake(self):
        """记录一次失误，激怒老板"""
        return self.trigger_anger(intensity=2)
    
    def record_good_response(self):
        """记录一次好的回应，安抚老板"""
        return self.calm_down(amount=1)
    
    def record_data_response(self):
        """记录一次数据化回答，较大安抚"""
        return self.calm_down(amount=2)
    
    def get_pressure_modifier(self) -> float:
        """获取当前压力倍数"""
        return self.get_emotion().get("pressure_multiplier", 1.0)
    
    def get_random_response(self) -> str:
        """获取当前情绪下的随机回复"""
        emotion = self.get_emotion()
        templates = emotion.get("response_templates", [])
        return random.choice(templates) if templates else "..."
    
    def decay(self):
        """情绪衰减（随时间）"""
        if self.state.get("calmdown_timer", 0) > 0:
            self.state["calmdown_timer"] -= 1
            if self.state["anger_accumulator"] > 0:
                self.state["anger_accumulator"] -= 1
            self.set_emotion(self._calculate_emotion())
    
    def get_status(self) -> str:
        """获取情绪状态"""
        emotion = self.get_emotion()
        anger = self.state.get("anger_accumulator", 0)
        
        anger_bar = "🔴" * min(max(anger, 0), 10) if anger > 0 else "🟢" * min(max(-anger, 0), 10)
        
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║                    😤 老板情绪状态                           ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 当前情绪：{emotion['name']:<47}║",
            f"║ 描述：{emotion['description']:<48}║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 愤怒值：{anger_bar:<39}║",
            f"║ 愤怒累积：{anger:<44}║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║ 压力倍数：                                              ║",
            f"║   ×{emotion['pressure_multiplier']:<51}║",
            f"║ 表扬概率：{emotion['praise_chance']*100:.0f}%{' '*45}║",
            "╚══════════════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="情绪系统")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=["get", "set", "anger", "calm", "status"], required=True)
    parser.add_argument("--emotion")
    parser.add_argument("--intensity", type=int, default=1)
    
    args = parser.parse_args()
    system = EmotionSystem(args.base_dir)
    
    if args.action == "get":
        print(system.get_emotion())
    
    elif args.action == "set":
        result = system.set_emotion(args.emotion)
        print(f"✅ 情绪已设置为：{result['name']}")
        print(f"   {result['description']}")
    
    elif args.action == "anger":
        result = system.trigger_anger(args.intensity)
        print(f"😡 老板被激怒了！")
        print(f"   当前：{result['name']}")
        print(f"   压力倍数：×{result['pressure_multiplier']}")
    
    elif args.action == "calm":
        result = system.calm_down()
        print(f"🧘 老板冷静了一些")
        print(f"   当前：{result['name']}")
    
    elif args.action == "status":
        print(system.get_status())


if __name__ == "__main__":
    main()
