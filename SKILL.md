---
name: create-boss
description: "Distill your boss into an AI Skill. 越苛刻越好，支持持续进化、Claude Code架构深度集成。"
argument-hint: "[boss-name-or-slug]"
version: "6.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.

# 老板.skill 创建器 v6.0

> *让苛刻成为生产力 — Claude Code架构深度集成版* 🏆

---

## 🎯 Claude Code架构深度集成

| Claude Code特性 | Boss Skill集成 |
|----------------|---------------|
| **Cost Tracker** | ✅ 实时成本追踪，API调用统计 |
| **Session Manager** | ✅ 会话保存/恢复/归档 |
| **/doctor** | ✅ 健康检查诊断工具 |
| **101 Commands** | ✅ 模块化命令系统 |
| **State Persistence** | ✅ 状态持久化 |
| **Health Monitor** | ✅ 系统健康监控 |

---

## 核心工具

| 工具 | 命令 | 说明 |
|------|------|------|
| **cost_tracker.py** | `/boss-cost` | 实时成本追踪 |
| **session_manager.py** | `/boss-session` | 会话管理 |
| **doctor.py** | `/boss-doctor` | 健康检查 |
| **evolution_logger.py** | `/boss-evolve` | 进化追踪 |
| **pattern_detector.py** | `/boss-patterns` | 模式检测 |
| **rl_feedback.py** | `/boss-rl` | RL反馈 |
| **multi_boss_battle.py** | `/boss-battle` | 多老板对战 |
| **ralplan_ralph.py** | `/boss-mode` | 双层执行模式切换 |
| **leaderboard.py** | `/boss-leaderboard` | 排行榜 |

---

## 🎭 双层执行模式 (Ralplan + Ralph)

借鉴 **oh-my-codex** 的双层执行架构：

| 模式 | 命令 | 角色 |
|------|------|------|
| **Ralplan** | `/boss {name} ralplan` | 老板=审批者，审方案、挑刺、质疑 |
| **Ralph** | `/boss {name} ralph` | 老板=执行者，施压、追问、给指令 |
| **Direct** | `/boss {name}` | 原有模式，直接对线 |

### Ralplan 模式

用户提交方案/周报/文档，老板以"审批者"身份审查：
- 连环追问数据和逻辑
- 挑战假设和风险
- 打回修改或勉强通过

```
/boss-wang ralplan
> [粘贴方案内容]

老板审阅意见：
状态：❌ 打回修改
主要问题：
  1. 数据来源不明确，样本量多少？
  2. 竞品分析缺失
  3. 时间线没有缓冲
老板批示："给我补充数据后再来"
```

### Ralph 模式

用户汇报任务进展，老板以"老板视角"施压：
- 追问具体进度和完成定义
- 质疑延迟和卡点
- 给出明确指令

```
/boss-wang ralph
> 任务A遇到了技术难点...

老板指令：
当前进度：45%
追问：
  1. 什么难点？尝试过什么方案？
  2. 为什么之前没发现这个问题？
  3. 需要我协调什么资源？
下一步指令：
  • 明天上午10点前给我3个可选方案
  • 每个方案标注优劣势和风险
⚡ "不要只给我问题，给我问题+解决方案"
```

---

## 💰 Cost Tracker - Claude Code风格成本追踪

### 实时成本显示

```
┌─────────────────────────────────────────┐
│         Boss Skill Cost Tracker           │
└─────────────────────────────────────────┘
│ Session: session_20260404_150000        │
│ Total Cost: $0.023456                  │
│ Total Calls: 47                        │
├─────────────────────────────────────────┤
│ Tokens:                                   │
│   Input:  12,345                        │
│   Output: 67,890                         │
├─────────────────────────────────────────┤
│ By Action Type:                            │
│   evolve  : $0.010234 (15 calls)
│   feedback: $0.008765 (20 calls)
│   battle  : $0.004457 (12 calls)
└─────────────────────────────────────────┘
```

### 使用方式

```bash
# 记录一次API调用
python tools/cost_tracker.py --slug example_wang --action record \
  --model claude-3-5-sonnet \
  --input-tokens 1000 --output-tokens 500

# 查看当前成本
python tools/cost_tracker.py --slug example_wang --action show

# 查看历史
python tools/cost_tracker.py --slug example_wang --action history
```

---

## 🩺 Doctor - 健康检查诊断

Claude Code `/doctor` 风格的一键诊断：

```bash
python tools/doctor.py --base-dir .

# 输出：
╔══════════════════════════════════════════════════════════════╗
║   🩺  Boss Skill Doctor - 健康检查                          ║
╚══════════════════════════════════════════════════════════════╝

✅ File Structure        All required files present
✅ Boss Examples        2 bosses: example_wang, example_li
✅ Tools                8 tools: evolution_logger.py, ...
✅ Evolution System     2/2 bosses have evolution data
✅ Prompt Templates     7 templates
⚠️  Config Files        Optional: Missing kubernetes configs

📊 检查结果: ✅ 6 passed, ⚠️ 1 warnings

🎉 所有检查通过！你的 Boss Skill 正常运行中
```

---

## 💾 Session Manager - 会话管理

### 特性
- **自动保存** - 每5分钟自动保存
- **会话恢复** - 任意历史会话恢复
- **归档备份** - 保存到indexed JSONL
- **状态追踪** - Nightmare Level / Pressure Index

### 使用方式

```bash
# 查看当前状态
python tools/session_manager.py --slug example_wang --action status

# 保存会话
python tools/session_manager.py --slug example_wang --action save

# 归档并开始新会话
python tools/session_manager.py --slug example_wang --action archive

# 列出历史会话
python tools/session_manager.py --slug example_wang --action list

# 恢复指定会话
python tools/session_manager.py --slug example_wang --action restore \
  --session-id session_20260404_140000
```

---

## 📊 Session状态输出示例

```
╔══════════════════════════════════════════════════════════════╗
║                  Boss Skill Session Status                   ║
╠══════════════════════════════════════════════════════════════╣
║ Session ID: session_20260404_150000_123456                ║
║ Created: 2026-04-04T15:00:00+08:00                         ║
║ Updated: 2026-04-04T15:30:00+08:00                         ║
╠══════════════════════════════════════════════════════════════╣
║ Stats:                                                      ║
║   Messages: 47                                              ║
║   Corrections: 5                                            ║
║   Evolutions: 3                                            ║
╠══════════════════════════════════════════════════════════════╣
║ State:                                                      ║
║   Nightmare Level: 4.8/5                                    ║
║   Pressure Index: 7.2/10                                     ║
║   Version: v2                                               ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🚀 快速开始

### 1. 创建老板
```
/create-boss
```

### 2. 运行健康检查
```
/boss-doctor
```

### 3. 跟老板对线
```
/boss-wang
```

### 4. 查看成本
```
/boss-cost
```

### 5. 保存会话
```
/boss-session --action archive
```

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v1.0 | 初始版本 |
| v3.0 | 自我进化系统 |
| v4.0 | RL反馈+对战+排行榜 |
| v5.0 | Docker/CI-CD/测试 |
| **v6.0** | Claude Code架构深度集成：Cost Tracker/Session Manager/Doctor |
| **v6.1** | **oh-my-codex双层执行模式：Ralplan(审方案) + Ralph(施压)** |

---

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Boss Skill v6.1                               │
│           Claude Code + oh-my-codex 双架构                     │
├─────────────────────────────────────────────────────────────┤
│  🎭 双层执行模式 (Ralplan + Ralph)                           │
│  ├─ Ralplan: 方案审批 - 挑刺/质疑/追问数据                    │
│  ├─ Ralph: 任务施压 - 质疑延迟/追问完成定义                  │
│  └─ Direct: 直接对线 - 保留原有模式                           │
├─────────────────────────────────────────────────────────────┤
│  Commands Layer (101+ style modular commands)                 │
│  ├─ /boss, /boss-review, /boss-evolve, /boss-rl           │
│  ├─ /boss-battle, /boss-leaderboard                        │
│  ├─ /boss-cost, /boss-session, /boss-doctor                │
│  └─ /boss-mode: 双层模式切换                                 │
├─────────────────────────────────────────────────────────────┤
│  Core Services                                              │
│  ├─ CostTracker: 实时成本追踪                               │
│  ├─ SessionManager: 会话保存/恢复/归档                      │
│  ├─ EvolutionLogger: JSONL进化事件                         │
│  ├─ PatternDetector: 行为模式检测                          │
│  └─ RLFeedbackTracker: action-reward追踪                    │
├─────────────────────────────────────────────────────────────┤
│  State Management                                           │
│  ├─ State Persistence: JSON自动保存                         │
│  ├─ Session Recovery: 任意历史恢复                          │
│  └─ Cost History: 全量追踪                                 │
└─────────────────────────────────────────────────────────────┘
```

---

*老板.skill v6.0 — Claude Code架构，让苛刻成为传奇* 🏆
