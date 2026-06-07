# Self-Improving Social Media System
## money-and-mode.com | Fun in the Life

This is the autonomous content + social media engine. It runs on a schedule, learns from what works, and presents plans for Sandip to approve before anything goes out.

---

## How the Loop Works

```
WEEK 1–3: Post → Collect Data
     ↓
WEEK 4: Claude reviews what worked
     ↓
MONTH START: Claude researches trends → builds 4-week plan → Sandip approves
     ↓
EXECUTE the plan → repeat
```

**Human intervention points:**
- Monthly plan: Claude presents → Sandip says "go" or adjusts
- Any new platform or campaign: always ask first
- Publishing: Claude creates draft → Sandip publishes
- Anything irreversible: always ask first

---

## Scheduled Tasks

| Task | When | What it does |
|------|------|-------------|
| Weekly check-in | Every Monday 9am | Reviews last week's posts, flags what's working |
| Monthly research | 1st of each month, 8am | Trend research + 4-week content plan |
| Publishing reminder | Every Tue + Fri 9am | Reminds what to post/publish today |

---

## Files in This System

| File | Purpose |
|------|---------|
| `performance-log.json` | Track Instagram metrics per post — Sandip fills in weekly |
| `README.md` | This file — how the system works |
| `../monthly-reports/` | Monthly research reports + 4-week plans |
| `../future-posts/batch-2-instagram.md` | Next batch of posts ready to go |
| `../queue.json` | All pending + posted social items |

---

## Sandip's Weekly Input (2 min)

After each post, wait 5 days then add the numbers to `performance-log.json`:
- **Saves** — most important. Find in Instagram Insights → Post → Saves
- **Comments** — second most important
- **Reach** — how many unique accounts saw it
- **Likes** — least important but still track

You don't need to check every day. Once a week is enough.

---

## What Claude Does Automatically

1. **Reads performance data** → finds which topics, formats, hashtags are working
2. **Researches trends** → what's getting traction in AI / financial freedom / life niches
3. **Builds content plan** → 4 weeks of posts across all platforms
4. **Writes captions** → saves-first format with targeted hashtags
5. **Updates queue.json** → ready for posting

## What Sandip Does

1. **Approves the monthly plan** — takes 5 minutes
2. **Inputs weekly metrics** — takes 2 minutes
3. **Posts the content** — captions pre-written, images ready, just paste and post
4. **Publishes WordPress drafts** — Claude creates them, Sandip hits Publish

---

## The Improvement Loop

Each month, Claude looks at:
- Which 2 posts had the highest saves → those topics get more content
- Which hashtags drove new followers → use more of those
- Which caption formats got most comments → replicate the structure
- Which topics got zero engagement → retire or rethink

This is written into `learnings` array in `performance-log.json` so every future month builds on the last.

---

*System designed: June 2026 | Runs autonomously with human approval gates*
