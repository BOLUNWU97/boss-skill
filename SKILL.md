---
name: create-boss
description: "Distill your boss into an AI Skill. 越苛刻越好，支持持续进化。" 
argument-hint: "[boss-name-or-slug]"
version: "3.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.

# 老板.skill 创建器 v3.0

> *让苛刻成为生产力 — 持续进化版*

---

## 触发条件

**创建新老板：**
- `/create-boss`
- "帮我创建一个老板 skill"
- "我想蒸馏我的老板"

**使用已有老板：**
- `/boss-{slug}` — 跟老板对线
- `/boss-{slug}-review` — 让老板审你的方案
- `/boss-{slug}-weekly` — 让老板预审你的周报
- `/boss-{slug}-combat` — 向上管理练习（对抗模式）
- `/boss-{slug}-interview` — 晋升/面试模拟

**进化命令：**
- `/boss-{slug}-evolve` — 触发自我进化分析
- `/boss-{slug}-log` — 查看进化日志
- `/boss-{slug}-patterns` — 查看检测到的模式
- `/boss-{slug}-learn` — 从对话中学习

**管理命令：**
- `/list-bosses` — 列出所有老板
- `/update-boss {slug}` — 进化模式（追加文件/纠正）
- `/boss-rollback {slug} {version}` — 回滚到历史版本
- `/nightmare-level {slug}` — 查看/更新 Nightmare Level
- `/delete-boss {slug}` — 删除老板

---

## 🧬 自我进化系统

### 核心机制

```
用户纠正 → 记录进化事件 → 检测模式 → 更新规则
     ↓
对话分析 → 发现新模式 → 强化特征
     ↓
版本存档 → 自我改进 → 持续学习
```

### 进化触发条件

| 触发 | 说明 |
|------|------|
| 用户纠正 | 说"他不会这样" |
| 对话结束 | 自动分析本次对话 |
| 模式检测 | 发现重复3次以上的句式 |
| Nightmare Level 变化 | 压力指数超过阈值 |

### 进化命令详解

#### `/boss-{slug}-evolve`

触发自我进化分析：
```
1. 分析对话历史
2. 检测行为模式
3. 计算压力指数
4. 生成进化建议
5. 自动更新（如需要）
```

#### `/boss-{slug}-log`

查看进化日志：
```
日期  | 类型 | 内容
------+------+------
04-04 | correction | "他不会说'好的'"
04-03 | pattern | 检测到新句式"impact呢"
04-02 | version | 创建版本v2
```

#### `/boss-{slug}-patterns`

查看检测到的模式：
```
检测到的老板特征：
- 深夜/周末工作期望: 12次
- 质疑追问: 28次
- 连环追问: 8次
- 直接否定: 15次

新发现的句式：
- "impact是什么": 出现5次
- "数据呢": 出现8次
- "这个方案...": 出现3次
```

#### `/boss-{slug}-learn`

从当前/最近对话中学习：
1. 分析本次对话
2. 提取老板的说话模式
3. 更新 persona.md 中的相关内容
4. 记录进化事件

---

## 进化状态追踪

### Nightmare Level 动态更新

Nightmare Level 不再是静态的，而是根据实际对话动态调整：

```
初始评级: 用户预估 4.5/5
    ↓
对话分析: 检测到压力行为
    ↓
压力指数: 计算公式 = (模式出现次数 × 权重) / 总消息数 × 2
    ↓
建议更新: 压力指数 > 7 → 建议 +0.1
         压力指数 < 3 → 建议 -0.1
```

### 版本控制

每次重大更新自动创建版本：
```
v1.0 - 初始创建
v1.1 - 用户纠正了CR相关行为
v1.2 - 检测到新的追问模式
v2.0 - Nightmare Level 从4.5升到4.8
```

### 进化事件日志（JSONL格式）

```json
{"event_type": "correction", "timestamp": "2026-04-04T...", "data": {...}}
{"event_type": "pattern_detected", "timestamp": "2026-04-04T...", "data": {...}}
{"event_type": "self_improvement", "timestamp": "2026-04-04T...", "data": {...}}
{"event_type": "version_created", "timestamp": "2026-04-04T...", "data": {...}}
```

---

## 安全边界 ⚠️

1. **仅用于自我认知与向上管理**
2. **不伪造老板言行**，所有输出基于真实数据
3. **Layer 0 硬规则**确保老板的"苛刻"是真实还原
4. **进化有记录**，所有变更可追溯可回滚

---

## 工具使用规则

| 任务 | 使用工具 |
|------|---------|
| 读取 PDF/图片/截图 | `Read` 工具 |
| 读取 MD/TXT 文件 | `Read` 工具 |
| 解析邮件 .eml/.mbox | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/email_parser.py` |
| 进化日志 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/evolution_logger.py` |
| 模式检测 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/pattern_detector.py` |
| 写入/更新 Skill 文件 | `Write` / `Edit` 工具 |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

---

## 完整使用流程

### 1. 创建老板
```
/create-boss
→ 回答问题 → 生成老板 Skill
```

### 2. 日常使用
```
/boss-wang -review
→ 粘贴方案 → 老板审阅 → 你准备应对
```

### 3. 纠正进化
```
用户：他不应该说'好的'，他从来不说

/boss-wang-learn
→ 记录纠正 → 更新 persona → 记录进化事件
```

### 4. 自动进化
```
定期运行 /boss-wang-evolve
→ 分析对话历史 → 检测模式 → 建议更新
```

---

## 示例进化对话

### 对话1：用户纠正

```
用户：等等，他不是这样的。他从来不说'好的'，只会说'不够好'。

老板.skill：
理解。他从来不说'好的'，只会说'不够好'。
这已记录为 Layer 0 核心规则。

更新中...
✅ 已追加到 Correction 记录
✅ 已更新 persona.md
✅ 已记录进化事件

现在的老王：
- 从不说"好的"
- 标准回复是"不够好"
- 偶尔说"还行"（60分）
```

### 对话2：自我进化

```
用户：/boss-wang-evolve

老板.skill：
🧬 开始自我进化分析...

📊 对话历史分析：
- 总对话数: 23次
- 总消息数: 156条
- 老板消息: 89条

🔍 模式检测：
- 质疑追问: 28次 (31%)
- 直接否定: 15次 (17%)
- 连环追问: 8次 (9%)
- 深夜消息: 5次 (6%)

📈 压力指数: 7.2/10

💡 进化建议：
1. [pattern_strong] 'impact是什么' 出现12次，建议加入口头禅
2. [nightmare_level_up] 压力指数7.2 > 7.0，建议更新 Nightmare Level

是否应用以上建议？(确认/拒绝/部分)
```

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v1.0 | 初始版本，基础创建功能 |
| v1.1 | 新增进化模式、邮件解析 |
| v2.0 | 新增5种使用模式、Nightmare Level评估、生存建议 |
| **v3.0** | **新增自我进化系统、模式检测、压力指数追踪** |

---

## 技术架构

```
┌─────────────────────────────────────────────────────┐
│                  Boss Skill v3.0                       │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐    │
│  │           用户交互层                           │    │
│  │  /boss-{slug} /-review /-evolve /-learn   │    │
│  └─────────────────────────────────────────────┘    │
│                      ↓                              │
│  ┌─────────────────────────────────────────────┐    │
│  │           进化引擎层                          │    │
│  │  evolution_logger.py                       │    │
│  │  pattern_detector.py                       │    │
│  │  version_manager.py                        │    │
│  └─────────────────────────────────────────────┘    │
│                      ↓                              │
│  ┌─────────────────────────────────────────────┐    │
│  │           Skill 文件层                       │    │
│  │  SKILL.md / management.md / persona.md      │    │
│  │  meta.json / evolutions/*.jsonl           │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

*老板.skill v3.0 — 让苛刻成为生产力，让进化成为习惯*
