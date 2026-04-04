#!/usr/bin/env python3
"""
Boss Skill 邮件解析器

解析工作邮件，提取老板的管理风格特征。

支持格式：.eml .mbox

Usage:
    python3 email_parser.py --file <path> --boss <name> --output <output_path>
"""

import argparse
import re
import os
import sys
from pathlib import Path
from datetime import datetime


def parse_eml(file_path: str) -> dict:
    """解析 .eml 格式邮件"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 提取时间
    date_match = re.search(r'^Date:\s*(.+)$', content, re.MULTILINE)
    sent_time = date_match.group(1).strip() if date_match else "未知"
    
    # 提取主题
    subject_match = re.search(r'^Subject:\s*(.+)$', content, re.MULTILINE)
    subject = subject_match.group(1).strip() if subject_match else "无主题"
    
    # 提取发送者
    from_match = re.search(r'^From:\s*(.+)$', content, re.MULTILINE)
    sender = from_match.group(1).strip() if from_match else "未知"
    
    # 提取正文（简单版，去掉邮件头）
    body_start = content.find('\n\n')
    body = content[body_start+2:] if body_start != -1 else content
    
    return {
        'sent_time': sent_time,
        'subject': subject,
        'sender': sender,
        'body_preview': body[:500],
        'full_body': body
    }


def parse_mbox(file_path: str) -> list:
    """解析 .mbox 格式（简化版）"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 简单按 From 分割（不完美，但够用）
    messages = re.split(r'\nFrom .+?@.+?\n', content)
    results = []
    for msg in messages[1:]:  # 跳过第一段空内容
        if len(msg.strip()) > 50:
            results.append(msg.strip()[:1000])
    return results


def analyze_email_style(emails: list) -> dict:
    """分析邮件风格"""
    all_text = ' '.join([e.get('full_body', '') for e in emails if isinstance(e, dict)])
    
    # 时间分布
    time_pattern = re.compile(r'(\d{1,2}):\d{2}')
    times = time_pattern.findall(all_text)
    
    # 句子长度
    sentences = re.split(r'[。！？\n]', all_text)
    avg_sentence_len = sum(len(s) for s in sentences if s) / max(len(sentences), 1)
    
    # 问号频率（追问信号）
    question_count = all_text.count('？') + all_text.count('?')
    
    # 感叹号频率（情绪信号）
    exclaim_count = all_text.count('！') + all_text.count('!')
    
    # 常见施压词
    pressure_words = ['为什么', '依据', '数据', '结论', '思路', '验证', '不够好', '不行', '重做']
    pressure_count = sum(all_text.count(w) for w in pressure_words)
    
    return {
        'total_emails': len(emails),
        'avg_sentence_length': round(avg_sentence_len, 1),
        'question_count': question_count,
        'exclaim_count': exclaim_count,
        'pressure_word_count': pressure_count,
        'time_distribution': '需要从邮件头解析',
        'style': '追问型' if question_count > 10 else ('情绪型' if exclaim_count > 5 else '冷静型')
    }


def main():
    parser = argparse.ArgumentParser(description='Boss Skill 邮件解析器')
    parser.add_argument('--file', required=True, help='邮件文件路径')
    parser.add_argument('--boss', required=True, help='老板称呼')
    parser.add_argument('--output', required=True, help='输出文件路径')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)
    
    ext = Path(args.file).suffix.lower()
    
    if ext == '.eml':
        emails = [parse_eml(args.file)]
    elif ext == '.mbox':
        emails = [{'body_preview': m, 'full_body': m} for m in parse_mbox(args.file)]
    else:
        print(f"不支持的格式：{ext}", file=sys.stderr)
        sys.exit(1)
    
    analysis = analyze_email_style(emails)
    
    # 写入输出
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# 邮件分析 — {args.boss}\n\n")
        f.write(f"来源文件：{args.file}\n")
        f.write(f"邮件数量：{analysis['total_emails']}\n\n")
        
        f.write("## 邮件风格分析\n")
        f.write(f"- 平均句子长度：{analysis['avg_sentence_length']} 字\n")
        f.write(f"- 问号数量：{analysis['question_count']}（追问频率）\n")
        f.write(f"- 感叹号数量：{analysis['exclaim_count']}（情绪强度）\n")
        f.write(f"- 施压词出现：{analysis['pressure_word_count']} 次\n")
        f.write(f"- 风格判断：{analysis['style']}\n\n")
        
        if emails and isinstance(emails[0], dict):
            f.write("## 样本邮件\n\n")
            for i, email in enumerate(emails[:3], 1):
                f.write(f"### 邮件 {i}\n")
                f.write(f"- 时间：{email.get('sent_time', '未知')}\n")
                f.write(f"- 主题：{email.get('subject', '无主题')}\n")
                f.write(f"- 正文预览：{email.get('body_preview', '')[:300]}...\n\n")
    
    print(f"分析完成，结果已写入 {args.output}")


if __name__ == '__main__':
    main()
