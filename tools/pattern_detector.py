#!/usr/bin/env python3
"""
Boss Skill Pattern Detector
从对话历史中检测老板的行为模式
"""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path


class PatternDetector:
    """老板行为模式检测器"""
    
    # 常见老板模式关键词
    PRESSURE_PATTERNS = [
        # 时间压力
        (r"(凌晨|深夜|半夜|晚上\d+点|周末|节假日)", "深夜/周末工作期望"),
        (r"(立刻|马上|尽快|\d+小时|\d+分钟|马上给我)", "时间紧迫感施压"),
        
        # 质疑类
        (r"(为什么|依据是什么|数据呢|impact|证据)", "质疑追问"),
        (r"(你确定|你保证|你敢保证)", "要求承诺"),
        (r"(不够好|不行|重做|重写|这不是我想要的)", "直接否定"),
        
        # 追问类
        (r"(再说一遍|然后呢|所以呢|接着说)", "连环追问"),
        (r"(具体点|详细说|展开说)", "要求细节"),
        
        # 威胁类
        (r"(不适合|可以考虑|优化|绩效|走人)", "职场威胁"),
        
        # 表扬类（稀缺）
        (r"(不错|还行|进步了|可以)", "难得表扬"),
    ]
    
    EMOTION_SIGNALS = [
        (r"！{2,}", "强烈情绪"),
        (r"\?{2,}", "质疑追问"),
        (r"\.\.\.{2,}|…{2,}", "无语/拖延"),
        (r"\[捂脸\]|\[尴尬\]|\[无奈\]", "负面情绪"),
    ]
    
    def __init__(self, boss_slug: str, base_dir: str = "./bosses"):
        self.boss_slug = boss_slug
        self.base_dir = Path(base_dir)
        
    def analyze_conversation(self, conversation: list) -> dict:
        """
        分析对话，检测老板行为模式
        
        conversation: [{"role": "boss/user", "content": "..."}, ...]
        """
        boss_messages = [m["content"] for m in conversation if m.get("role") == "boss"]
        user_messages = [m["content"] for m in conversation if m.get("role") == "user"]
        
        # 统计各种模式出现次数
        pattern_counts = defaultdict(int)
        emotion_counts = defaultdict(int)
        
        for msg in boss_messages:
            for pattern, name in self.PRESSURE_PATTERNS:
                if re.search(pattern, msg):
                    pattern_counts[name] += 1
            
            for pattern, name in self.EMOTION_SIGNALS:
                if re.search(pattern, msg):
                    emotion_counts[name] += 1
        
        # 检测新模式
        new_patterns = self._detect_new_patterns(boss_messages)
        
        # 计算压力指数
        pressure_index = self._calculate_pressure_index(pattern_counts, len(boss_messages))
        
        return {
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "total_boss_messages": len(boss_messages),
            "total_user_messages": len(user_messages),
            "pressure_index": pressure_index,  # 0-10
            "detected_patterns": dict(pattern_counts),
            "emotion_signals": dict(emotion_counts),
            "new_patterns": new_patterns,
            "boss_style_summary": self._summarize_style(pattern_counts, emotion_counts)
        }
    
    def _detect_new_patterns(self, messages: list) -> list:
        """检测新模式（不在预设列表中的）"""
        new_patterns = []
        
        # 检测重复句式
        sentence_patterns = defaultdict(list)
        for msg in messages:
            # 提取句子开头作为模式
            sentences = re.split(r"[。！？\n]", msg)
            for s in sentences:
                s = s.strip()
                if len(s) > 5 and len(s) < 50:
                    first_words = " ".join(s.split()[:3]) if s.split() else ""
                    if first_words:
                        sentence_patterns[first_words].append(s)
        
        # 找出重复3次以上的句式
        for pattern, examples in sentence_patterns.items():
            if len(examples) >= 3:
                new_patterns.append({
                    "pattern": pattern,
                    "count": len(examples),
                    "examples": examples[:3],
                    "confidence": min(0.5 + len(examples) * 0.1, 1.0)
                })
        
        return new_patterns
    
    def _calculate_pressure_index(self, pattern_counts: dict, total_messages: int) -> float:
        """计算压力指数 (0-10)"""
        if total_messages == 0:
            return 0.0
        
        # 权重
        weights = {
            "深夜/周末工作期望": 2.0,
            "时间紧迫感施压": 1.5,
            "质疑追问": 1.0,
            "要求承诺": 1.5,
            "直接否定": 1.5,
            "连环追问": 2.0,
            "要求细节": 0.5,
            "职场威胁": 3.0,
            "难得表扬": -1.0,  # 表扬减少压力
        }
        
        score = 0.0
        for pattern, count in pattern_counts.items():
            weight = weights.get(pattern, 1.0)
            score += count * weight
        
        # 归一化到0-10
        normalized = score / max(total_messages, 1) * 2
        return min(max(normalized, 0), 10)
    
    def _summarize_style(self, pattern_counts: dict, emotion_counts: dict) -> str:
        """总结老板风格"""
        summaries = []
        
        # 基于主要模式判断风格
        if pattern_counts.get("深夜/周末工作期望", 0) >= 3:
            summaries.append("工作狂类型")
        elif pattern_counts.get("职场威胁", 0) >= 2:
            summaries.append("高压管理类型")
        elif pattern_counts.get("连环追问", 0) >= 3:
            summaries.append("追问型管理")
        elif pattern_counts.get("直接否定", 0) >= 5:
            summaries.append("批评型管理")
        
        # 基于情绪信号
        if emotion_counts.get("强烈情绪", 0) >= 2:
            summaries.append("情绪化")
        elif emotion_counts.get("难得表扬", 0) >= 1:
            summaries.append("偶尔肯定")
        
        return " + ".join(summaries) if summaries else "标准型"
    
    def generate_evolution_suggestions(self, analysis: dict) -> list:
        """基于分析生成进化建议"""
        suggestions = []
        
        # 基于压力指数
        if analysis["pressure_index"] >= 7:
            suggestions.append({
                "type": "nightmare_level_up",
                "suggestion": f"压力指数已达 {analysis['pressure_index']:.1f}/10，建议更新 Nightmare Level"
            })
        
        # 基于检测到的模式
        for pattern, count in analysis["detected_patterns"].items():
            if count >= 5:
                suggestions.append({
                    "type": "pattern_strong",
                    "suggestion": f"'{pattern}' 出现 {count} 次，应作为核心特征强化"
                })
        
        # 基于新模式
        for new_p in analysis.get("new_patterns", []):
            if new_p["confidence"] >= 0.7:
                suggestions.append({
                    "type": "new_pattern",
                    "suggestion": f"发现重复句式: '{new_p['pattern']}...' (出现{new_p['count']}次)，建议加入 persona"
                })
        
        return suggestions


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Pattern Detector")
    parser.add_argument("--slug", required=True, help="Boss slug")
    parser.add_argument("--base-dir", default="./bosses", help="Base directory")
    parser.add_argument("--conversation", help="JSON conversation file")
    parser.add_argument("--output", help="Output file")
    
    args = parser.parse_args()
    
    detector = PatternDetector(args.slug, args.base_dir)
    
    # 如果提供了对话文件
    if args.conversation:
        with open(args.conversation, "r", encoding="utf-8") as f:
            conversation = json.load(f)
        
        analysis = detector.analyze_conversation(conversation)
        
        # 输出分析结果
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            print(f"分析结果已保存到: {args.output}")
        else:
            print(f"\n📊 模式分析结果:")
            print(f"   压力指数: {analysis['pressure_index']:.1f}/10")
            print(f"   老板风格: {analysis['boss_style_summary']}")
            print(f"\n🔍 检测到的模式:")
            for pattern, count in analysis["detected_patterns"].items():
                print(f"   - {pattern}: {count}次")
            print(f"\n💡 进化建议:")
            for s in detector.generate_evolution_suggestions(analysis):
                print(f"   - [{s['type']}] {s['suggestion']}")
    else:
        # 读取对话历史
        history_file = Path(args.base_dir) / args.slug / "conversation_history.jsonl"
        if not history_file.exists():
            print(f"未找到对话历史: {history_file}")
            return
        
        conversations = []
        with open(history_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    conversations.append(json.loads(line))
        
        if conversations:
            analysis = detector.analyze_conversation(conversations[-1].get("messages", []))
            print(f"\n📊 最新对话模式分析:")
            print(f"   压力指数: {analysis['pressure_index']:.1f}/10")
            print(f"   风格: {analysis['boss_style_summary']}")


if __name__ == "__main__":
    main()
