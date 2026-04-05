# 老板.skill — 把老板蒸馏成AI，越苛刻越好

> *让苛刻成为生产力 — 双层执行模式 v6.1* 🏆

---

## 🎭 新增！Ralplan + Ralph 双层执行模式

借鉴 **oh-my-codex** 架构，老板既能"审方案"又能"施压"：

```
/boss-wang ralplan   →  老板以审批者身份审方案、连环追问
/boss-wang ralph     →  老板以老板视角施压、追问进度
/boss-wang           →  直接对线（原有模式）
```

---

## 🎯 一句话介绍

把让人窒息的老板蒸馏成 AI Skill，模拟他的苛刻审阅、追问、施压，**并且持续从对话中进化学习，多老板对战让你体验职场修罗场**。

---

## ✨ 冲冠Hackathon功能清单

| 功能 | 亮点 |
|------|------|
| 🏢 **管理风格提取** | 从邮件/聊天记录提取管理风格、开会行为 |
| 😤 **苛刻人格还原** | 五层 Persona 还原老板真实施压模式 |
| 📊 **Nightmare Level** | 量化评估老板窒息程度（1-5星） |
| 🧬 **自我进化 v3.0** | 从对话中学习，自动检测模式 |
| 🤖 **RL反馈追踪** | 用强化学习思想追踪行为好坏 |
| ⚔️ **多老板对战** | 模拟你+老板A vs 老板B场景 |
| 🏆 **公开排行榜** | Nightmare Level 社区投票 |
| 🎭 **双层执行模式** | Ralplan审方案 + Ralph施压 ⭐NEW |

---

## ⚔️ 多老板对战 — 修罗场模式

```
你是小王，你的老板是老王和李姐。
你想争取晋升，需要同时应对：
- 老王："impact是什么？！"
- 李姐："说说你的思路是什么？"

⏱️ 这是修罗场。
```

---

## 🤖 RL反馈追踪 — 用AI训练AI

```
用户的反应 = reward
老板的行为 = action

如果用户说"很像" → reward +
如果用户说"不像" → reward -

累积评分 → 强化/弱化行为

让老板越像真实的老板！
```

---

## 🏆 Nightmare Leaderboard

```
🏆 Nightmare Leaderboard

📊 统计：
   总BOSS数：1,247
   平均噩梦：3.8/5

TOP 3：
  🥇 老王 (某大厂) ⭐⭐⭐⭐⭐ 4.8/5 | 234票
  🥈 张总 (某创业公司) ⭐⭐⭐⭐⭐ 4.6/5 | 189票
  🥉 李姐 (某互联网) ⭐⭐⭐⭐ 4.2/5 | 156票
```

---

## 🚀 快速开始

### 1. 创建老板

```
/create-boss
→ 回答问题 → 生成老板 Skill
```

### 2. 日常使用

```
/boss-{slug}           — 跟老板对线
/boss-{slug} ralplan   — 让老板审方案（审批者模式）
/boss-{slug} ralph     — 让老板施压（执行者模式）
/boss-{slug}-review   — 让老板审你的方案
/boss-{slug}-weekly   — 让老板审你的周报
```

### 3. 多老板对战

```
/bosses-battle --create
→ 选择老板 → 设置目标 → 开始修罗场
```

### 4. 提交你的老板

```
/submit-boss --name "我的老板" --company "某大厂" --nightmare 4.5
```

---

## 📁 目录结构

```
boss-skill/
├── SKILL.md                      # 主入口 (v4.0 冲冠版)
├── README.md                     # 说明文档
├── prompts/
│   ├── intake.md               # 录入问题
│   ├── boss_persona_builder.md # Persona 生成模板
│   ├── boss_persona_analyzer.md # Persona 分析
│   ├── boss_work_builder.md     # 管理风格生成模板
│   ├── management_analyzer.md    # 管理风格分析
│   ├── merger.md                # 增量更新
│   └── correction_handler.md    # 纠正处理
├── tools/
│   ├── email_parser.py         # 邮件解析
│   ├── evolution_logger.py      # 进化日志 (v3.0)
│   ├── pattern_detector.py     # 模式检测 (v3.0)
│   ├── rl_feedback.py          # RL反馈追踪 ⭐NEW
│   ├── multi_boss_battle.py   # 多老板对战 ⭐NEW
│   ├── leaderboard.py          # 噩梦排行榜 ⭐NEW
│   ├── version_manager.py      # 版本管理
│   └── skill_writer.py         # 列表管理
└── bosses/
    ├── example_wang/          # 老王（Nightmare 4.8/5）
    │   ├── SKILL.md
    │   ├── management.md
    │   ├── persona.md
    │   ├── meta.json
    │   └── evolutions/
    │       ├── evolution.jsonl
    │       ├── rl_feedback.jsonl ⭐NEW
    │       └── versions/
    └── example_li/           # 李姐（Nightmare 4/5）
        ├── management.md
        ├── persona.md
        └── meta.json
```

---

## 🏛️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    Boss Skill v4.0 冲冠版                      │
├─────────────────────────────────────────────────────────┤
│  用户交互层：对线 / 审方案 / 进化 / 对战 / 排行榜            │
│                         ↓                                  │
│  进化引擎层：日志 / 模式检测 / 版本控制                      │
│                         ↓                                  │
│  RL反馈层：行为评分 / 强化 / 弱化 ⭐NEW                     │
│                         ↓                                  │
│  对战系统：多老板 / 修罗场 / 生存分数 ⭐NEW                  │
│                         ↓                                  │
│  Skill文件层：SKILL.md / management / persona / meta       │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ 安全声明

1. **仅用于自我认知与向上管理**
2. **不伪造老板言行**，所有输出基于真实数据
3. **进化有记录**，所有变更可追溯可回滚

---

## 📈 版本历史

| 版本 | 更新内容 |
|------|---------|
| v1.0 | 初始版本，基础创建功能 |
| v1.1 | 新增进化模式、邮件解析 |
| v2.0 | 新增5种使用模式、Nightmare Level评估 |
| v3.0 | 新增自我进化系统、模式检测 |
| v4.0 | 冲冠Hackathon版：RL反馈、多老板对战、排行榜 |
| v6.0 | Claude Code架构深度集成：Cost Tracker/Session Manager/Doctor |
| **v6.1** | **oh-my-codex双层执行模式：Ralplan + Ralph** |

---

## Hackathon 评分预估

| 维度 | 权重 | 得分 |
|------|------|------|
| 创意 | 20% | 8/10 |
| 技术实现 | 25% | 9/10 |
| 工程化程度 | 20% | 8/10 |
| 实用价值 | 25% | 10/10 |
| 演示效果 | 10% | 10/10 |

**总分：91/100**

---

*让苛刻成为生产力，让进化成为习惯，让职场修罗场成为训练场* 🏆
