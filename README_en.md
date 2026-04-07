# 🎭 Boss Skill

[![Stars](https://img.shields.io/github/stars/BOLUNWU97/boss-skill?style=for-the-badge)](https://github.com/BOLUNWU97/boss-skill/stargazers)
[![Forks](https://img.shields.io/github/forks/BOLUNWU97/boss-skill?style=for-the-badge)](https://github.com/BOLUNWU97/boss-skill/network/members)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> 🎮 **[Live Demo](https://BOLUNWU97.github.io/boss-skill/demo/)** — See the boss simulation in action!

---

> **Simulate your boss with AI. Practice dealing with demanding bosses through realistic conversations.**

Train for performance reviews, promotion interviews, project presentations, and handling pressure — all through AI-powered boss simulations.

---

## What is this?

Your boss asks questions you can't answer. Deadlines that don't make sense. Meetings that go on forever questioning your every word.

This tool does one thing: **turns your boss into an AI** so you can practice dealing with them — without real consequences.

What can you practice?
-向上管理 (managing up)
- Presenting proposals
- Performance reviews & promotions
- Handling unreasonable pressure

---

## Features

| Feature | What it does |
|---------|-------------|
| 🏢 **Boss Extraction** | Feed your boss's emails/chats, AI learns their style |
| 😤 **Realistic Dialogue** | Boss questions, challenges, and pressures you |
| 📊 **Nightmare Level** | Rate how demanding your boss is (1-5 stars) |
| 🧬 **Self-Evolution** | The more you chat, the more accurate it gets |
| ⚔️ **Battle Mode** | Two bosses pressuring you at once |
| 🏆 **Leaderboard** | See whose boss is the most demanding |
| 🎮 **Gamification** | Achievements, XP, levels — growth while you train |
| 😤 **Emotion System** | Boss mood affects their intensity |
| 🖼️ **Multi-modal** | Send screenshots directly |

---

## Quick Start

```bash
# Clone
git clone https://github.com/BOLUNWU97/boss-skill.git
cd boss-skill

# Install
pip install -r requirements.txt

# Create your boss
python tools/skill_writer.py --create
```

### Example

```
You: Boss, I finished the monthly proposal

Boss (Lao Wang):
  Stop.
  
  Question 1: How do you quantify the impact?
  Question 2: Did you calculate the ROI?
  Question 3: You said Friday for delivery.
             How did you arrive at that date?
  
  Think it through again.
```

---

## Dual Execution Mode

Same boss, two different interaction styles:

**ralplan mode** — Reviewer perspective
For: Proposal review, promotion interviews, project presentations
Behavior: Cross-examination, pointing out flaws, demanding data

**ralph mode** — Pressure perspective  
For: Handling pressure, managing up training
Behavior: Sustained pressure, questioning attitude, deadline emphasis

```
/boss-wang ralplan  "Here's my proposal..."
/boss-wang ralph    "I'm having some trouble..."
```

---

## Battle Mode

Two bosses pressuring you simultaneously:

```
👤 You: Pitching for a promotion

😤 Boss Wang: What's the impact?!
😰 Boss Li: What's your thought process?

⏱️ Survival time: 23 minutes
💀 Times caught off guard: 3
🏆 Rating: S
```

---

## Evolution System

After each conversation, you give feedback:

```
"sounds like him"  →  +1 point for this behavior
"not like him"    →  -1 point for this behavior

Behaviors with high scores get reinforced
Behaviors with low scores get weakened

After a few sessions, you'll think:
"This is exactly how my boss talks"
```

---

## Example Bosses

**Lao Wang** · Tech Giant · ⭐⭐⭐⭐⭐ 4.8/5
> "Impact", "ROI", "Deadline" — the classic trio
> Meetings always drilling into details
> You say a number, he asks how you got that number

**Sister Li** · Internet Company · ⭐⭐⭐⭐ 4.2/5
> Seems gentle on surface, but questions are actually sharper
> "I don't quite follow your thinking, explain?"
> Lets you dig your own grave

---

## Project Structure

```
boss-skill/
├── SKILL.md                    # Main entry
├── prompts/                    # Prompt templates
│   ├── intake.md              # Boss info input
│   ├── boss_persona_builder.md
│   ├── boss_work_builder.md
│   └── ...
├── tools/                      # Python tools
│   ├── skill_writer.py        # Create boss
│   ├── evolution_logger.py     # Evolution log
│   ├── rl_feedback.py         # RL feedback
│   ├── multi_boss_battle.py   # Battle mode
│   └── leaderboard.py          # Leaderboard
├── bosses/                     # Boss database
│   ├── example_wang/          # Lao Wang
│   └── example_li/           # Sister Li
├── gamification/               # Gamification
├── community/                 # Community
├── multimodal_input.py        # Multi-modal input
└── docker-compose.yml         # Docker deployment
```

---

## Tech Stack

- **Python** — Core logic
- **OpenAI API** — LLM for conversation
- **OpenClaw** — Agent runtime
- **Docker** — Easy deployment

---

## Disclaimer

- For self-awareness and upward management training only
- Boss behavior based on real data you input, not fabricated
- Evolution records are saved and can be rolled back

---

## License

MIT

---

<p align="center">
  让苛刻成为生产力 🏆
</p>
