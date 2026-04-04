#!/usr/bin/env python3
"""
Boss Skill Voice Demo
语音对线模式 - 模拟老板的语音施压
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class VoiceDemo:
    """
    语音对线演示系统
    
    核心功能：
    - TTS 语音合成老板的回复
    - 模拟真实通话场景
    - 支持多种老板风格
    """
    
    def __init__(self, boss_slug: str, base_dir: str = "./bosses"):
        self.boss_slug = boss_slug
        self.base_dir = Path(base_dir)
        self.boss = self._load_boss()
    
    def _load_boss(self) -> dict:
        """加载老板数据"""
        meta_file = self.base_dir / self.boss_slug / "meta.json"
        if not meta_file.exists():
            return {}
        
        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def generate_voice_response(self, user_input: str, context: str = "") -> dict:
        """
        生成老板的语音回复
        
        返回：
        - text: 老板说的话
        - audio_path: 音频文件路径（如果有TTS）
        - emotion: 情绪强度 (0-1)
        - pressure_score: 压力指数 (0-10)
        """
        boss_name = self.boss.get("name", "老板")
        nightmare = float(self.boss.get("tags", {}).get("nightmare_level", "3").split("/")[0])
        style = self.boss.get("tags", {}).get("management_style", [])
        
        # 根据nightmare level选择不同的回复风格
        if nightmare >= 4.5:
            response = self._wang_style_response(user_input, boss_name)
            emotion = 0.8
            pressure_score = 8.5
        elif nightmare >= 4.0:
            response = self._li_style_response(user_input, boss_name)
            emotion = 0.6
            pressure_score = 7.0
        else:
            response = self._normal_style_response(user_input, boss_name)
            emotion = 0.3
            pressure_score = 4.0
        
        return {
            "text": response,
            "boss_name": boss_name,
            "emotion": emotion,
            "pressure_score": pressure_score,
            "nightmare_level": nightmare
        }
    
    def _wang_style_response(self, user_input: str, boss_name: str) -> str:
        """生成老王风格的回复"""
        import random
        
        # 根据用户输入生成合适的回应
        if any(k in user_input for k in ["晋升", "加薪", "涨薪"]):
            responses = [
                "你的KPI完成了多少？impact是什么？数据呢？",
                "晋升？你觉得你配吗？先说说你的贡献。",
                "我觉得你还需要再历练历练。",
            ]
        elif any(k in user_input for k in ["方案", "计划", "提案"]):
            responses = [
                "impact是什么？数据支撑在哪里？",
                "不够好。回去重写。",
                "这个方案有什么问题？你考虑过风险吗？",
            ]
        elif any(k in user_input for k in ["完成了", "做完了", "搞定了"]):
            responses = [
                "完成了？结果呢？数据在哪里？",
                "过程不重要，结果是什么？",
                "好，下一步呢？",
            ]
        elif any(k in user_input for k in ["困难", "问题", "做不了"]):
            responses = [
                "为什么做不了？试过哪些方案？",
                "给我24小时，我要看到结果。",
                "这是借口还是理由？",
            ]
        else:
            responses = [
                "嗯。（沉默3秒）继续说。",
                "impact是什么？",
                "数据呢？",
                "不够好。",
            ]
        
        return random.choice(responses)
    
    def _li_style_response(self, user_input: str, boss_name: str) -> str:
        """生成李姐风格的回复"""
        import random
        
        if any(k in user_input for k in ["晋升", "加薪"]):
            responses = [
                "说说看，你的思路是什么？",
                "我不理解。你再解释一下。",
                "你的判断依据是什么？",
            ]
        elif any(k in user_input for k in ["方案", "计划"]):
            responses = [
                "这个逻辑不够清晰。",
                "说说你的思路。",
                "数据呢？结论呢？",
            ]
        else:
            responses = [
                "我不理解。",
                "再说一遍。",
                "重点是什么？",
            ]
        
        return random.choice(responses)
    
    def _normal_style_response(self, user_input: str, boss_name: str) -> str:
        """生成普通风格的回复"""
        return "好的，我知道了。"


class VoiceDemoPlayer:
    """
    语音演示播放器
    
    可以播放老板的回复序列，模拟真实通话
    """
    
    def __init__(self):
        self.demos = self._load_demos()
    
    def _load_demos(self) -> dict:
        """加载预设演示"""
        return {
            "boss_intro": {
                "title": "老板自我介绍",
                "scenes": [
                    {"speaker": "boss", "text": "我是老王，P9技术总监。"},
                    {"speaker": "boss", "text": "我的标准很高，完成100%是及格线。"},
                    {"speaker": "boss", "text": "有问题随时找我，但先想清楚再来。"},
                ]
            },
            "weekly_review": {
                "title": "周报审阅",
                "scenes": [
                    {"speaker": "boss", "text": "你的周报我看了。"},
                    {"speaker": "boss", "text": "第一个问题：完成了什么？数据呢？"},
                    {"speaker": "boss", "text": "没有数据的完成度等于没说。"},
                    {"speaker": "boss", "text": "总结：不够好，重写。"},
                ]
            },
            "late_night": {
                "title": "深夜消息",
                "scenes": [
                    {"speaker": "boss", "text": "（晚上11:47）这个bug怎么回事？"},
                    {"speaker": "boss", "text": "为什么没第一时间通知我？"},
                    {"speaker": "boss", "text": "下次注意。随时向我汇报进度。"},
                ]
            },
            "7_strikes": {
                "title": "七连追问",
                "scenes": [
                    {"speaker": "boss", "text": "你的方案我看了。"},
                    {"speaker": "boss", "text": "第一个问题：impact是什么？"},
                    {"speaker": "boss", "text": "第二个问题：数据呢？"},
                    {"speaker": "boss", "text": "第三个问题：有什么风险？"},
                    {"speaker": "boss", "text": "第四个问题：为什么选这个方案？"},
                    {"speaker": "boss", "text": "第五个问题：谁来做？什么时候完成？"},
                    {"speaker": "boss", "text": "第六个问题：如果失败了呢？"},
                    {"speaker": "boss", "text": "第七个问题：你保证能完成吗？"},
                    {"speaker": "boss", "text": "你的方案不够成熟，回去想清楚再来。"},
                ]
            }
        }
    
    def play_demo(self, demo_name: str) -> list:
        """播放预设演示"""
        if demo_name not in self.demos:
            return []
        
        return self.demos[demo_name]["scenes"]
    
    def list_demos(self) -> list:
        """列出所有预设演示"""
        return [{"name": k, "title": v["title"], "scenes": len(v["scenes"])} 
                for k, v in self.demos.items()]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Voice Demo")
    parser.add_argument("--slug", default="example_wang")
    parser.add_argument("--base-dir", default="./bosses")
    parser.add_argument("--action", choices=["demo", "respond", "list-demos"])
    parser.add_argument("--demo-name", help="演示名称")
    parser.add_argument("--user-input", help="用户说的话")
    
    args = parser.parse_args()
    
    if args.action == "list-demos":
        player = VoiceDemoPlayer()
        demos = player.list_demos()
        print("\n📢 可用演示：\n")
        for d in demos:
            print(f"  {d['name']}: {d['title']} ({d['scenes']}个场景)")
    
    elif args.action == "demo":
        if not args.demo_name:
            print("错误：需要 --demo-name")
            return
        
        player = VoiceDemoPlayer()
        scenes = player.play_demo(args.demo_name)
        
        if not scenes:
            print(f"错误：未找到演示 '{args.demo_name}'")
            return
        
        print(f"\n🎬 演示: {args.demo_name}\n")
        print("="*60)
        
        for i, scene in enumerate(scenes, 1):
            print(f"\n[{scene['speaker'].upper()}] {scene['text']}")
    
    elif args.action == "respond":
        demo = VoiceDemo(args.slug, args.base_dir)
        
        if not args.user_input:
            print("错误：需要 --user-input")
            return
        
        response = demo.generate_voice_response(args.user_input)
        
        print(f"\n👔 {response['boss_name']}:")
        print(f"   \"{response['text']}\"")
        print(f"\n📊 压力指数: {response['pressure_score']}/10")
        print(f"   情绪强度: {response['emotion']:.0%}")


if __name__ == "__main__":
    main()
