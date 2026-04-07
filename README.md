# 老板.skill 🎭

> **Topics:** `hackathon` `老板AI` `角色扮演` `RL反馈` `生产力` `面试训练`

> *把老板蒸馏成AI，让苛刻成为生产力*

[![Version](https://img.shields.io/badge/version-7.0.0-blue.svg)](https://github.com/Bolun-wu/boss-skill)
[![Platform](https://img.shields.io/badge/platform-OpenClaw-green.svg)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## 一句话简介

**把真实老板蒸馏成AI，支持游戏化对战、情绪系统、社区分享和多模态输入** — 越苛刻越好。

---

## 功能说明

`boss-skill` 是一个全功能的老板AI模拟器，将你的真实老板（或自定义角色）蒸馏成可对线的AI助手。它不只是问答，而是一个完整的游戏化对战系统，支持：

- 🎮 **游戏化对战** — 难度等级（1-5级）、成就系统、XP升级
- 😤 **情绪系统** — 老板有心情波动，影响对你的反应
- 🌍 **社区系统** — 分享/继承/投票热门老板
- 🖼️ **多模态输入** — 直接发截图给老板看
- 🔄 **双层执行模式** — Ralplan（审方案）和 Ralph（施压追问）两种模式
- 📊 **Claude Code风格工具** — 成本追踪、会话管理、健康诊断
- 🐺 **多老板对战** — 修罗场模式，多个老板轮流施压

---

## 安装方法

```bash
# 通过 OpenClaw 安装
openclaw skills install boss-skill

# 或从源码安装
git clone https://github.com/Bolun-wu/boss-skill.git
cd boss-skill
```

## 使用方法

### 快速开始

```bash
# 1. 创建老板
/create-boss

# 2. 查看游戏状态
/game status

# 3. 设置难度（1-5级）
/game difficulty --level 4

# 4. 开始对线
/boss-wang

# 5. 查看成本
/boss-cost
```

### 双层执行模式

| 模式 | 命令 | 角色 |
|------|------|------|
| **Ralplan** | `/boss {name} ralplan` | 审批者，审方案、挑刺 |
| **Ralph** | `/boss {name} ralph` | 执行者，施压、追问进度 |
| **Direct** | `/boss {name}` | 直接对线 |

```bash
/boss-wang ralplan  → 粘贴方案让老王审
/boss-wang ralph    → 汇报任务让老王施压
```

### 游戏化系统

```bash
# 查看成就
/game achievements

# 查看老板情绪
/game emotion

# 查看排行榜
/boss-leaderboard
```

### 社区系统

```bash
# 查看社区状态
/community status

# 提交我的老板
/submit-boss --name "老王" --nightmare 4.5

# 继承别人的老板
/inherit-boss <boss_id>
```

---

## 难度等级

| 等级 | 名称 | 描述 |
|------|------|------|
| 1 | 🌱 萌新 | 鼓励为主，新手入门 |
| 2 | 🐣 入门 | 正常要求，合理反馈 |
| 3 | 💼 正常 | 标准老板，职场常态 |
| 4 | 🔥 地狱 | 高压追问，问题不断 |
| 5 | ☠️ 窒息 | 究极挑战，极限测试 |

---

## 参数说明

### 核心参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--level` | 3 | 难度等级 1-5 |
| `--mode` | direct | 执行模式：direct/ralplan/ralph |
| `--boss-name` | — | 老板名称（用于多老板对战） |

### 游戏参数

| 参数 | 说明 |
|------|------|
| `--xp` | 经验值 |
| `--achievements` | 查看成就列表 |
| `--emotion` | 查看老板当前情绪 |

---

## 输出示例

```
╔══════════════════════════════════════════╗
║     老板.skill v7.0  对线开始           ║
╠══════════════════════════════════════════╣
║  老板: 老王 (☠️ 窒息模式)                ║
║  心情: 😡 生气 (压力×1.6)               ║
║  你的XP: 850 | 等级: 8                   ║
║  当前成就: 对线老手 ×3                   ║
╚══════════════════════════════════════════╝

> 你: 方案我做好了，发您看看

😡 老王: 这个方案问题很多！
   1. 数据来源不明
   2. ROI计算逻辑有问题
   ...
```

---

## 前提条件

- **平台**: OpenClaw
- **可选**: Claude API（用于更真实的对话生成）
- **可选**: Docker（用于容器化部署）

---

## 核心工具一览

| 类别 | 工具 | 命令 |
|------|------|------|
| **基础** | cost_tracker.py | `/boss-cost` 成本追踪 |
| | session_manager.py | `/boss-session` 会话管理 |
| | doctor.py | `/boss-doctor` 健康诊断 |
| **执行** | ralplan_ralph.py | `/boss-mode` 双层模式 |
| **进化** | evolution_logger.py | `/boss-evolve` 进化追踪 |
| | pattern_detector.py | `/boss-patterns` 模式检测 |
| | rl_feedback.py | `/boss-rl` RL反馈 |
| **对战** | multi_boss_battle.py | `/boss-battle` 多老板对战 |
| | leaderboard.py | `/boss-leaderboard` 排行榜 |

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v1.0 | 初始版本 |
| v3.0 | 自我进化系统 |
| v4.0 | RL反馈+对战+排行榜 |
| v5.0 | Docker/CI-CD/测试 |
| v6.0 | Claude Code架构集成 |
| v6.1 | oh-my-codex双层执行模式 |
| **v7.0** | **全功能版：游戏化+情绪+社区+多模态** |

---

## 相关链接

- **GitHub**: https://github.com/Bolun-wu/boss-skill
- **OpenClaw**: https://clawhub.ai
