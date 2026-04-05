---
name: create-boss
description: "Distill your boss into an AI Skill. 越苛刻越好，支持持续进化、Claude Code架构深度集成、游戏化、社区系统、多模态输入。"
argument-hint: "[boss-name-or-slug]"
version: 7.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.

# 老板.skill 创建器 v7.0

> *让苛刻成为生产力 — 全功能版* 🏆

---

## 🎯 版本说明

**v7.0 全功能版** 新增：
- 🎮 游戏化系统（难度等级/成就/XP）
- 😤 情绪系统（老板心情影响反应）
- 🌍 社区系统（分享/继承/投票）
- 🖼️ 多模态输入（图片/截图）

---

## 核心工具一览

| 类别 | 工具 | 命令 | 说明 |
|------|------|------|------|
| **基础** | cost_tracker.py | `/boss-cost` | 成本追踪 |
| | session_manager.py | `/boss-session` | 会话管理 |
| | doctor.py | `/boss-doctor` | 健康诊断 |
| **执行** | ralplan_ralph.py | `/boss-mode` | 双层模式 |
| **进化** | evolution_logger.py | `/boss-evolve` | 进化追踪 |
| | pattern_detector.py | `/boss-patterns` | 模式检测 |
| | rl_feedback.py | `/boss-rl` | RL反馈 |
| **对战** | multi_boss_battle.py | `/boss-battle` | 多老板对战 |
| | leaderboard.py | `/boss-leaderboard` | 排行榜 |
| **游戏化** | game_master.py | `/game` | 游戏总控 |
| | difficulty_system.py | `/game difficulty` | 难度等级 |
| | achievement_system.py | `/game achievements` | 成就系统 |
| | emotion_system.py | `/game emotion` | 情绪系统 |
| **社区** | community_system.py | `/community` | 社区老板库 |
| **多模态** | multimodal_input.py | (自动) | 图片处理 |

---

## 🎮 游戏化系统

### 难度等级

可选 1-5 级，老板从"温和"到"窒息"：

| 等级 | 名称 | 描述 |
|------|------|------|
| 1 | 🌱 萌新 | 鼓励为主，新手入门 |
| 2 | 🐣 入门 | 正常要求，合理反馈 |
| 3 | 💼 正常 | 标准老板，职场常态 |
| 4 | 🔥 地狱 | 高压追问，问题不断 |
| 5 | ☠️ 窒息 | 究极挑战，极限测试 |

```
# 设置难度
/game difficulty --level 5

# 查看状态
/game status
```

### 成就系统

| 成就 | 描述 | XP奖励 |
|------|------|--------|
| ⏱️ 十分钟玩家 | 对线10分钟没崩溃 | 50 |
| 🔥 三十分钟战士 | 对线30分钟依然坚挺 | 150 |
| 💀 一小时存活 | 对线1小时见过地狱 | 500 |
| ⚔️ 对线老手 | 对线10次 | 100 |
| 💪 对线达人 | 对线50次 | 300 |
| 🏆 对线王者 | 对线100次 | 1000 |
| ✅ 方案通过 | 方案一次性通过审批 | 100 |
| 📈 数据大师 | 用数据回答5连问 | 150 |
| 🎯 完美应对 | 连续3次正确回答追问 | 80 |
| ☠️ 五星噩梦 | 挑战最高难度并存活 | 500 |

```
# 查看成就
/game achievements

# 查看完整状态
/game status
```

### 玩家等级

- 每对线1次 = +10 XP
- 每解锁成就 = 成就XP奖励
- 100 XP 升级
- 等级越高，难度锁定越高

---

## 😤 情绪系统

老板有情绪波动，心情影响反应：

| 情绪 | 压力倍数 | 表扬概率 |
|------|----------|----------|
| 😊 心情好 | ×0.7 | 50% |
| 😐 平常心 | ×1.0 | 15% |
| 😰 焦虑 | ×1.3 | 5% |
| 😡 生气 | ×1.6 | 2% |
| 🤬 暴怒 | ×2.0 | 0% |

**触发情绪变化：**
- 失误 → 愤怒+2
- 好的回应 → 冷静+1
- 数据化回答 → 冷静+2

```
# 查看老板情绪
/game emotion
```

---

## 🎭 双层执行模式

借鉴 oh-my-codex：

| 模式 | 命令 | 角色 |
|------|------|------|
| **Ralplan** | `/boss {name} ralplan` | 审批者，审方案、挑刺 |
| **Ralph** | `/boss {name} ralph` | 执行者，施压、追问进度 |
| **Direct** | `/boss {name}` | 直接对线 |

```
/boss-wang ralplan  → 粘贴方案让老王审
/boss-wang ralph    → 汇报任务让老王施压
```

---

## 🌍 社区系统

分享你的老板到社区，或继承别人的：

```
# 查看社区状态
/community status

# 提交我的老板
/submit-boss --name "老王" --nightmare 4.5

# 继承别人的老板
/inherit-boss <boss_id>

# 投票
/vote-boss <boss_id>
```

**热门老板 TOP：**
- 按票数排行
- 按噩梦等级筛选
- 可直接继承到你的列表

---

## 🖼️ 多模态输入

支持直接发送图片给老板看：

- 截图直接丢给老板审
- PPT截图也能看
- 邮件截图解析
- 文档图片化

```
发送图片给老板即可，他会'看到'并评论
```

---

## 🚀 快速开始

```bash
# 1. 创建老板
/create-boss

# 2. 查看游戏状态
/game status

# 3. 设置难度
/game difficulty --level 4

# 4. 开始对线
/boss-wang

# 5. 查看成本
/boss-cost
```

---

## 📊 v7.0 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Boss Skill v7.0 全功能版                      │
├─────────────────────────────────────────────────────────────┤
│  用户交互层                                                  │
│  ├─ /boss, /ralplan, /ralph (双层执行)                     │
│  ├─ /game, /community (游戏化+社区)                        │
│  └─ /boss-cost, /session, /doctor (Claude Code风格)        │
├─────────────────────────────────────────────────────────────┤
│  🎮 游戏化层                                                 │
│  ├─ DifficultySystem: 1-5级难度                            │
│  ├─ AchievementSystem: 18+成就                            │
│  ├─ EmotionSystem: 5级情绪                                │
│  └─ GameMaster: 统一控制                                    │
├─────────────────────────────────────────────────────────────┤
│  🌍 社区层                                                   │
│  └─ CommunitySystem: 提交/继承/投票                        │
├─────────────────────────────────────────────────────────────┤
│  🖼️ 多模态层                                                │
│  └─ MultimodalProcessor: 图片处理                          │
├─────────────────────────────────────────────────────────────┤
│  核心服务层                                                  │
│  ├─ CostTracker, SessionManager                            │
│  ├─ EvolutionLogger, PatternDetector                       │
│  └─ RLFeedbackTracker, MultiBossBattle                     │
└─────────────────────────────────────────────────────────────┘
```

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

*老板.skill v7.0 — 让苛刻成为传奇* 🏆
