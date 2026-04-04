---
name: create-boss
description: "Distill your boss into an AI Skill. 越苛刻越好，支持持续进化、多老板对战、Nightmare排行榜。"
argument-hint: "[boss-name-or-slug]"
version: "4.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.

# 老板.skill 创建器 v4.0

> *让苛刻成为生产力 — 冲冠版* 🏆

---

## 🎯 冲冠 Hackathon 功能清单

| 功能 | 亮点 |
|------|------|
| 🏢 **管理风格提取** | 从邮件/聊天记录提取管理风格、开会行为 |
| 😤 **苛刻人格还原** | 五层 Persona 还原老板真实施压模式 |
| 📊 **Nightmare Level** | 量化评估老板窒息程度（1-5星） |
| 🧬 **自我进化 v3.0** | 从对话中学习，自动检测模式 |
| 🤖 **RL反馈追踪** | 用强化学习思想追踪行为好坏 |
| ⚔️ **多老板对战** | 模拟你+老板A vs 老板B场景 |
| 🏆 **公开排行榜** | Nightmare Level 社区投票 |
| 🎬 **视频演示脚本** | 60秒窒息老板演示 |

---

## 触发条件

**创建新老板：**
- `/create-boss`

**使用已有老板：**
- `/boss-{slug}` — 跟老板对线
- `/boss-{slug}-review` — 让老板审你的方案
- `/boss-{slug}-weekly` — 让老板预审你的周报
- `/boss-{slug}-combat` — 向上管理练习
- `/boss-{slug}-interview` — 晋升面试模拟

**进化命令：**
- `/boss-{slug}-evolve` — 触发自我进化分析
- `/boss-{slug}-rl` — RL反馈追踪
- `/boss-{slug}-log` — 查看进化日志
- `/boss-{slug}-patterns` — 查看检测到的模式

**对战命令：**
- `/bosses-battle` — 多老板对战
- `/bosses-list` — 查看可用老板列表

**排行榜命令：**
- `/nightmare-leaderboard` — 查看排行榜
- `/submit-boss` — 提交你的老板

---

## 🤖 RL反馈追踪系统

### 核心思想

```
真实老板的行为 = "action"
用户的反应 = "reward"
累积的reward = 这个行为的"好坏"

让老板越像真实的老板！
```

### 使用方式

```
用户：/boss-wang-rl

老板.skill：
🎯 RL反馈模式

你刚才的表现：
- 追问回应：说得很好！（+0.8）
- 数据支撑：不够充分（+0.3）
- 整体生存分数：75%

📊 累积行为评分：
- 追问回应：S级（0.72）
- 数据呈现：A级（0.65）
- 时间管理：C级（0.30）

💡 进化建议：
- [强化] "impact是什么"式追问
- [弱化] 直接承诺时间
```

### 命令

```bash
python3 tools/rl_feedback.py --slug example_wang --action record \
  --action-type "追问" \
  --context "方案被质疑" \
  --user-reaction "对抗" \
  --reward 0.8
```

---

## ⚔️ 多老板对战系统

### 核心场景

```
你是小王，你的老板是老王和李姐。
你想争取晋升，需要同时应对：
- 老王的结果导向（"impact是什么"）
- 李姐的逻辑追问（"说说你的思路"）

这是修罗场。
```

### 使用方式

```
用户：/bosses-battle --create

👤 你的角色：小王
👔 老板阵容：老王、李姐
🎯 目标：争取晋升
⏱️ 紧张程度：extreme

开始对战！

---
第1轮：
小王：我想申请晋升，我觉得我这季度表现不错

老王：impact是什么？你做了什么？
李姐：说说看，你的思路是什么？

🏆 生存分数：60%

---
第2轮：
小王：（你会怎么应对？）
```

### 命令

```bash
# 查看可用老板
python3 tools/multi_boss_battle.py --action list

# 创建对战
python3 tools/multi_boss_battle.py --action create \
  --user "小王" \
  --bosses example_wang example_li \
  --goal "争取晋升" \
  --tension extreme

# 模拟一轮
python3 tools/multi_boss_battle.py --action simulate \
  --your-action "我这季度完成了X项目，提升了Y指标"
```

---

## 🏆 Nightmare Leaderboard

### 公开排行榜

```
🏆 Nightmare Leaderboard

📊 统计：
   总BOSS数：1,247
   平均噩梦：3.8/5
   总投票数：5,623

📈 分布：
   ⭐1-2: 89人
   ⭐⭐2-3: 234人
   ⭐⭐⭐3-4: 567人
   ⭐⭐⭐⭐4-5: 357人

TOP 10：
  1. 老王 (某大厂) ⭐⭐⭐⭐⭐ 4.8/5 | 234票
  2. 张总 (某创业公司) ⭐⭐⭐⭐⭐ 4.6/5 | 189票
  3. 李姐 (某互联网) ⭐⭐⭐⭐ 4.2/5 | 156票
```

### 提交你的老板

```
/submit-boss --name "我的老板" --company "某大厂" --nightmare 4.5
```

---

## 🎬 视频演示脚本（60秒）

### 演示文稿

```markdown
[0-5秒] 标题
━━━━━━━━━━━━━━━━
老板.skill - 让苛刻成为生产力
把老板蒸馏成AI，越苛刻越好

[5-15秒] 问题痛点
━━━━━━━━━━━━━━━━
"每天被老板追问到怀疑人生"
"方案改了8遍还是不够好"
"凌晨1点收到消息，不知道怎么回"

[15-30秒] 解决方案
━━━━━━━━━━━━━━━━
1. 3个问题，创建你的老板
2. 5种模式：对线/审方案/审周报/练习/面试
3. 自我进化：从对话中学习

[30-45秒] 演示
━━━━━━━━━━━━━━━━
用户：老板，这个需求太赶了
老板：两天？（沉默3秒）
     说'太赶'——依据是什么？
     我给你的时间是我觉得够用的。

[45-55秒] 进化系统
━━━━━━━━━━━━━━━━
用户：他不会这样
     ↓
自动记录 → 更新规则 → 持续学习

[55-60秒] 结尾
━━━━━━━━━━━━━━━━
老板.skill - 打工人必备
GitHub: titanwings/boss-skill
```

---

## 🏛️ v4.0 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    Boss Skill v4.0 冲冠版                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐  │
│  │              用户交互层                             │  │
│  │  /boss /-review /-evolve /-rl /-battle        │  │
│  │  /nightmare-leaderboard /submit-boss          │  │
│  └─────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │              进化引擎层 v3.0                         │  │
│  │  evolution_logger.py (JSONL事件日志)             │  │
│  │  pattern_detector.py (行为模式检测)             │  │
│  │  version_manager.py (版本控制)                  │  │
│  └─────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │              RL反馈层 (NEW!)                       │  │
│  │  rl_feedback.py (行为评分+强化/弱化)            │  │
│  └─────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │              对战系统层 (NEW!)                      │  │
│  │  multi_boss_battle.py (多老板对战)              │  │
│  │  leaderboard.py (噩梦排行榜)                    │  │
│  └─────────────────────────────────────────────────┘  │
│                        ↓                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │              Skill 文件层                         │  │
│  │  SKILL.md / management.md / persona.md          │  │
│  │  meta.json / evolutions/*.jsonl               │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v1.0 | 初始版本，基础创建功能 |
| v1.1 | 新增进化模式、邮件解析 |
| v2.0 | 新增5种使用模式、Nightmare Level评估 |
| v3.0 | 新增自我进化系统、模式检测 |
| **v4.0** | **冲冠版：RL反馈追踪、多老板对战、排行榜、演示脚本** |

---

## Hackathon 评分维度

| 维度 | 权重 | 我们的得分 |
|------|------|-----------|
| 创意 | 20% | 8/10 |
| 技术实现 | 25% | 9/10 |
| 工程化程度 | 20% | 8/10 |
| 实用价值 | 25% | 10/10 |
| 演示效果 | 10% | 10/10 |

**总分预估：91/100**

---

## 安装使用

```bash
# 安装
git clone https://github.com/titanwings/boss-skill ~/.openclaw/workspace/skills/boss-skill

# 创建老板
/create-boss

# 跟老板对线
/boss-wang

# 多老板对战
/bosses-battle --create --user "小王" --bosses example_wang example_li --goal "争取晋升"

# 查看排行榜
/nightmare-leaderboard

# 提交你的老板
/submit-boss --name "我的老板" --company "某大厂" --nightmare 4.5
```

---

*老板.skill v4.0 — 冲冠Hackathon，让苛刻成为传奇* 🏆
