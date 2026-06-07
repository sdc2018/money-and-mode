# Dashboard — Full Application Plan
## money-and-mode.com

Built like a real product. Add screens as we go.

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | FastAPI (Python) | Fast, clean API, you already use Python |
| Database | SQLite → PostgreSQL | Zero setup now, migrate when needed |
| Frontend | HTML + Tailwind + Alpine.js | No build tools, looks great, easy to extend |
| Charts | Chart.js (CDN) | Add in Phase 2 |
| Auth | None yet → add login in Phase 3 | Local only for now |

---

## Database Schema (current)

```
articles          — all content (planned/written/draft/published)
social_posts      — per-platform post status
metrics           — saves, comments, reach per post
todos             — Sandip's action items
traffic           — monthly visitor data
digest_items      — weekly curated content
```

---

## Screens — Build Order

### ✅ Phase 1 — MVP (built now)

**Screen 1: Overview**
- Stats: articles published, pending posts, overdue, open todos
- AdSense progress bar (visitors to 5,000 goal)
- Due soon (articles with upcoming publish dates)
- Recently posted

**Screen 2: Pipeline (Kanban)**
- 4 columns: Planned → Written → Draft → Published
- Article cards with series, date, live link

**Screen 3: Social Matrix**
- One row per article, 4 platform dots (🔴 pending, 🟢 posted)
- Quick scan: what still needs to be posted where
- Per-platform posted/pending counts

**Screen 4: Todos**
- Add/complete/delete tasks
- Priority levels (High/Medium/Low) with colour coding
- Category filter (Content/Social/SEO/Technical)
- Due dates

**Screen 5: Traffic**
- Monthly data entry (add each month's stats)
- Milestone cards (Ezoic at 1K, AdSense at 5K)
- Progress bar per month

---

### 🔵 Phase 2 — Analytics (Next)

**Screen 6: Performance Dashboard**
- Bar chart: saves per post (Chart.js)
- Line chart: reach over time
- Top 5 posts by saves/comments
- Platform comparison (which platform drives most engagement)
- Save rate = saves ÷ reach (target: >3%)

**Screen 7: Content Calendar**
- Monthly calendar view
- Green = published, Yellow = scheduled, Grey = planned
- Click a day to see what's due
- Drag to reschedule (future)

**Screen 8: Keyword Tracker**
- Table of target keywords
- Current Google ranking (manual entry)
- Monthly rank change
- Flag when a keyword enters top 10 → "push it" opportunity

---

### 🟡 Phase 3 — Curation & Digest

**Screen 9: Weekly Digest**
- Show this week's curated picks from content_curator.py output
- Edit "Kabir's take" for each in the browser
- One-click generate WordPress HTML
- Status: draft / reviewed / published

**Screen 10: Sources Manager**
- List all 32 RSS sources from sources.json
- Toggle active/inactive
- Add new sources with one form
- Last-fetched date, article count per source

---

### 🟢 Phase 4 — Revenue & Growth

**Screen 11: Revenue Tracker**
- Monthly AdSense earnings (manual entry)
- Monthly affiliate income (per source)
- Trend chart
- Projected: "at current growth, AdSense ready in X months"

**Screen 12: SEO Dashboard**
- Google Search Console data (paste or API)
- Top keywords by impressions
- Top articles by clicks
- Click-through rate per article
- Keyword gaps (impressions high, clicks low = fix the title)

---

### ⚪ Phase 5 — Automation (Future)

**Screen 13: Social Queue**
- Schedule posts for specific dates/times
- Instagram integration via Graph API
- One-click post from dashboard

**Screen 14: AI Writer**
- Pick a keyword → AI drafts the article
- Pick a post type → AI drafts the caption
- All in Kabir's voice

**Screen 15: Alerts**
- Notify when article is overdue
- Notify when traffic drops week-over-week
- Notify when a keyword reaches page 1

---

## Running Locally

```bash
# First time:
bash dashboard/run.sh

# Opens automatically at http://localhost:8765
```

## Adding to Git (what to commit / not commit)

```
✅ Commit: dashboard/*.py, dashboard/static/, dashboard/requirements.txt
❌ Don't commit: dashboard/data/dashboard.db  (local data, different per machine)
```

## Migrating to PostgreSQL (when ready)

Replace `sqlite3` in db.py with `psycopg2`.
Change `DB_PATH` to a connection string.
All SQL is standard — no SQLite-specific syntax.

---

## The Vision

This starts as a local tool for Sandip.
As it grows, it becomes the operations layer for the blog business.
Phase 4+ is a proper SaaS product for bloggers — but build for your own needs first.

*Every feature added should solve a real problem you have right now.*
