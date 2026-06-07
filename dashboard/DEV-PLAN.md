# Dashboard — Development Plan
## money-and-mode.com | Fun in the Life
**Created:** June 7, 2026  
**Status:** Phases 1–2 complete. This document plans Phases 3–5 + infrastructure work.

---

## Current State (as of Jun 7, 2026)

| Phase | Screens | Status |
|-------|---------|--------|
| Phase 1 | Overview, Pipeline, Social Matrix, Todos, Traffic | ✅ Done |
| Phase 2 | Performance charts, Content Calendar, Keyword Tracker | ✅ Done |
| Phase 3 | Digest Viewer, Sources Manager | 🔵 Next |
| Phase 4 | Revenue Tracker, SEO Dashboard | 🟡 Planned |
| Phase 5 | Social Queue, AI Writer, Alerts | ⚪ Future |
| Infra   | Settings screen, DB migrations, export/backup | 🔵 Alongside Phase 3 |

**Stack:** FastAPI + SQLite + Tailwind + Alpine.js + Chart.js  
**Run:** `bash dashboard/run.sh` → http://localhost:8765

---

## Phase 3 — Curation & Digest
**Goal:** See the weekly curated content from content_curator.py, edit it, publish it as a WordPress digest post — all from the dashboard.

---

### Screen 9 — Weekly Digest Viewer

**What problem it solves:**  
Every Monday, content_curator.py runs and drops a `digest-YYYY-WNN.json` into `social-media/digests/`. Right now you have to open that JSON file manually to read it, edit "Kabir's take" in a text editor, then hand-copy it to WordPress. This screen makes that one smooth flow inside the dashboard.

**UI layout:**
```
[ Week selector: ◀ Week 23 ▶ ]  [ Run Fetch Now button ]  [ Status: 9 items curated ]

[ 3 sections — one per topic: AI Technology | Financial Freedom | Life & Motivation ]

Each item card:
  Title + source + published date
  Summary (2–3 lines)
  [ Kabir's Take ] textarea — editable inline
  [ Skip ] [ Include ] toggle
  Link: "Read original →"

Bottom bar:
  [ Generate WordPress HTML ]  [ Copy to clipboard ]  [ Mark as Published ]
```

**Backend tasks:**
- `GET /api/digest` — reads `social-media/digests/digest-YYYY-WNN.json`, returns items
- `GET /api/digest/weeks` — lists all available week files (for week selector)
- `PUT /api/digest/{week}/item/{url_hash}` — save edits (kabirsTake, status: include/skip)
- `POST /api/digest/{week}/generate` — generates WordPress HTML from included items
- `POST /api/digest/{week}/fetch` — triggers `content_curator.py --fetch` as subprocess
- New DB table: `digest_edits` — stores kabirsTake + include/skip per item per week (so edits survive re-fetches)

**DB table — digest_edits:**
```sql
CREATE TABLE IF NOT EXISTS digest_edits (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    week        TEXT NOT NULL,         -- YYYY-WNN
    url         TEXT NOT NULL,
    kabirs_take TEXT,
    status      TEXT DEFAULT 'include',  -- include | skip
    updated_at  TEXT DEFAULT (datetime('now')),
    UNIQUE(week, url)
);
```

**WordPress HTML output format:**
```html
<h2>This Week in AI</h2>
<p><strong>Why I picked this:</strong> Kabir's take here...</p>
<p>→ <a href="[url]">[title]</a> — [source]</p>
...
```

**Effort estimate:** ~4 hours (backend: 2h, UI: 2h)

---

### Screen 10 — Sources Manager

**What problem it solves:**  
The 32 RSS sources in `marketing/sources.json` are edited manually in a JSON file. You can't quickly toggle a source off, see when it last fetched, or add a new source without opening a file. This screen is the visual editor for that file.

**UI layout:**
```
[ + Add Source ]  [ Filter: All | AI | Finance | Life | YouTube ]

Table:
  Name | URL | Topic | Type | Authority | Active | Last Fetched | Articles this week | Actions

Each row:
  Toggle: ON / OFF (active flag)
  Edit button → inline form
  Delete button

Add form (modal or inline):
  Name | RSS URL | Topic | Type (blog/youtube) | Authority (1–5)
```

**Backend tasks:**
- `GET /api/sources` — reads `marketing/sources.json`, returns all sources
- `PUT /api/sources/{name}` — toggle active/inactive, update authority
- `POST /api/sources` — add new source to sources.json
- `DELETE /api/sources/{name}` — remove from sources.json
- `GET /api/sources/stats` — reads digest JSON files, returns per-source article counts

**Note:** Sources live in `marketing/sources.json` (not DB). The API reads/writes that file directly. No DB table needed for sources — keep them in the file so content_curator.py can read them without DB access.

**Effort estimate:** ~3 hours (backend: 1.5h, UI: 1.5h)

---

## Phase 4 — Revenue & Growth
**Goal:** Track money coming in. Know if you're on track for AdSense.

---

### Screen 11 — Revenue Tracker

**What problem it solves:**  
Right now there's no way to see AdSense earnings, affiliate income, or whether you're on track. This screen is the financial dashboard for the blog business.

**UI layout:**
```
[ This month: ₹0 AdSense | ₹0 Affiliate | Total: ₹0 ]

[ Add monthly entry form ]
  Month | AdSense earnings | Affiliate income | Notes | Save

Chart: Monthly revenue bar chart (Chart.js, stacked: AdSense + Affiliate)

Milestones:
  □ First ₹100 from blog
  □ AdSense approved (after 5,000 visitors)
  □ ₹1,000/month
  □ ₹10,000/month (hobby→business)

Projection card:
  "At current traffic growth (+X%/mo), you'll hit AdSense threshold in ~N months"

Affiliate opportunities table:
  Product | Commission | Articles that could link to it | Status
  Amazon Kindle Unlimited | 8% | Index Funds, 10 Free AI Tools
  Zerodha (stock broker) | ₹300/signup | Savings Rate, 4% Rule
  MailerLite | $20/referral | (email list article when written)
```

**Backend tasks:**
- New DB columns in `traffic` table: `adsense_revenue`, `affiliate_revenue` (already has `adsense_revenue`)
- `GET /api/revenue` — monthly revenue history + projection calc
- `PUT /api/revenue/{month}` — update AdSense + affiliate amounts
- Projection formula: extrapolate traffic growth rate × assumed ₹RPM (revenue per thousand visitors)

**DB change:**
```sql
-- Add to traffic table (already has adsense_revenue):
ALTER TABLE traffic ADD COLUMN affiliate_revenue REAL DEFAULT 0;
ALTER TABLE traffic ADD COLUMN notes TEXT;
```
*(These may already exist — check before running)*

**Effort estimate:** ~3 hours (backend: 1h, UI: 2h)

---

### Screen 12 — SEO Dashboard

**What problem it solves:**  
Google Search Console has all the data — impressions, clicks, CTR, position — but you have to log in to GSC and manually dig through it. This screen lets you paste or import GSC data and see it in context with your articles.

**Two modes:**

**Mode A — Paste CSV (Phase 4a, quick to build):**  
- Export CSV from GSC → paste into dashboard → parsed and stored
- Shows: keyword, impressions, clicks, CTR%, avg position
- Highlights: "high impressions + low CTR = fix the title/meta"

**Mode B — GSC API (Phase 4b, harder, needs OAuth):**  
- Connect Google account → pull GSC data automatically
- Skip this unless Mode A proves useful first

**UI layout (Mode A):**
```
[ Paste GSC data ]  or  [ Import CSV file ]

Last imported: June 1, 2026 (142 rows)

Table:
  Keyword | Article (matched) | Impressions | Clicks | CTR | Avg Position | Action needed?

Opportunities panel:
  🔴 "High impressions, low CTR" — fix title/meta description (CTR < 2%)
  🟡 "Position 11–20 for this keyword" — push with internal links
  🟢 "Already page 1" — maintain

Top articles by clicks chart
```

**Backend tasks:**
- New DB table: `gsc_data`
- `POST /api/seo/import` — parse pasted CSV, store rows
- `GET /api/seo/summary` — return aggregated stats + opportunity flags
- Match keywords to articles via fuzzy match on `articles.keyword` column

**DB table — gsc_data:**
```sql
CREATE TABLE IF NOT EXISTS gsc_data (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    imported_at  TEXT DEFAULT (datetime('now')),
    query        TEXT,
    page         TEXT,
    impressions  INTEGER,
    clicks       INTEGER,
    ctr          REAL,
    position     REAL
);
```

**Effort estimate:** ~4 hours (parsing: 1h, backend: 1h, UI: 2h)

---

## Phase 5 — Automation
**Goal:** Reduce manual steps. Push the "post this to Instagram" button from the dashboard.

---

### Screen 13 — Social Queue

**What problem it solves:**  
Right now posting requires: open queue.json → copy caption → open Instagram → paste → find image → post. This screen queues posts with scheduled dates and shows what's due to post today.

**UI layout:**
```
TODAY'S QUEUE (Jun 10)
  📸 Instagram — Article 5 "10 Free AI Tools" — [Post Now] [Skip]
  📌 Pinterest — Article 5 "10 Free AI Tools" — [Post Now] [Skip]

UPCOMING
  Jun 12: 🐦 X — Will AI Take My Job (Thread)
  Jun 14: 👥 Facebook — Article 74

SCHEDULE NEW POST
  Article: [dropdown]
  Platform: [IG / X / FB / Pinterest]
  Date: [date picker]
  Caption: [textarea — pre-filled from queue.json]
  Image: [select from WP images or upload]
  [ Schedule ]
```

**"Post Now" flow (Instagram):**
- Copies caption to clipboard automatically
- Opens `https://www.instagram.com` in browser
- Shows checklist: 1. Verify handle = fun_in_life71 ✅ 2. Paste caption ✅ 3. Select image ✅
- After Sandip confirms posted → dashboard marks it done

**Backend tasks:**
- `GET /api/queue/today` — posts scheduled for today
- `GET /api/queue/upcoming` — next 14 days
- `POST /api/queue` — add scheduled post
- `PUT /api/queue/{id}/status` — mark posted/skipped

**Note:** Instagram API blocks programmatic posting — keep the clipboard-assist approach. Twitter API can post directly if Bearer Token is added to .env.

**Effort estimate:** ~5 hours (backend: 2h, UI: 3h)

---

### Screen 14 — AI Writer

**What problem it solves:**  
Writing article drafts and social captions is the biggest time consumer. This screen calls Claude API to draft in Kabir's voice.

**Two modes:**

**Mode A — Article Drafter:**
- Input: keyword + series + 3 bullet points of angle
- Output: full 1,000-word article in Kabir's voice (warm, wise, no jargon)
- Saves as draft in `/articles/` folder
- One click → create WordPress draft via REST API

**Mode B — Caption Generator:**
- Input: select article + platform
- Output: platform-optimised caption (IG saves-first, X punchy, FB story-format, Pinterest keyword-rich)
- Copies to clipboard → paste into social matrix

**Backend tasks:**
- `POST /api/ai/article` — calls Claude API, returns draft text
- `POST /api/ai/caption` — calls Claude API with platform-specific prompt
- Needs `CLAUDE_API_KEY` in `.env`

**Prompt templates (saved in `dashboard/prompts/`):**
- `article-prompt.txt` — full system prompt with Kabir's voice + rules
- `caption-instagram.txt` — saves-first format, 8 hashtags
- `caption-twitter.txt` — punchy thread format
- `caption-facebook.txt` — warm story format
- `caption-pinterest.txt` — keyword-rich description

**Effort estimate:** ~6 hours (prompts: 2h, backend: 2h, UI: 2h)

---

### Screen 15 — Alerts

**What problem it solves:**  
Currently nothing tells you when an article is overdue, when traffic dropped, or when a keyword hit page 1. This screen is the notification center.

**UI layout:**
```
ACTIVE ALERTS  (3 new)
  🔴 Article 93 "What is ChatGPT" — overdue 1 day (was due Jun 6)
  🟡 Traffic dropped: May had 200 real humans, Jun (week 1) tracking 120 — 40% drop
  🟢 Keyword "will AI take my job" moved to #8 — PAGE 1! Push it now.

ALERT RULES (configure)
  [x] Overdue articles — notify if past publish_date and not published
  [x] Traffic drop — notify if real_humans this month < last month - 20%
  [x] Keyword page 1 — notify when rank ≤ 10
  [x] Keyword entered top 3 — notify when rank ≤ 3 (double down!)
  [ ] Metrics due — notify 7 days after a post for entering Instagram Insights
```

**Backend tasks:**
- `GET /api/alerts` — runs all alert checks, returns active alerts list
- Alert checks are pure SQL queries (no external calls):
  - Overdue: `WHERE publish_date < today AND status != 'published'`
  - Traffic drop: compare last 2 months from traffic table
  - Keyword rank: compare latest vs previous keyword_rankings entry
  - Metrics due: posts > 7 days old with no metrics entry

**Effort estimate:** ~3 hours (backend: 2h, UI: 1h)

---

## Infrastructure Tasks (do alongside Phase 3)

These aren't screens — they're under-the-hood improvements.

---

### Infra 1 — Settings Screen

**What:** A settings tab in the dashboard for things that shouldn't be hardcoded.

**Settings to expose:**
- Blog URL (currently hardcoded as `money-and-mode.com`)
- Author name (currently "Kabir Shah" — hardcoded in prompts)
- AdSense target (currently 5,000 — hardcoded in overview)
- Ezoic target (currently 1,000 — hardcoded)
- Publishing schedule (currently Tue+Fri — hardcoded in calendar)
- API keys: WordPress URL + auth, Claude API key, Pinterest token, Twitter token

**Backend:**
- New DB table: `settings` (key-value store)
- `GET /api/settings` → returns all settings as key-value dict
- `PUT /api/settings` → bulk update
- Replace all hardcoded values in app.py with `get_setting("key", default)` helper

**DB table — settings:**
```sql
CREATE TABLE IF NOT EXISTS settings (
    key        TEXT PRIMARY KEY,
    value      TEXT,
    label      TEXT,              -- human-readable label for the UI
    category   TEXT DEFAULT 'general',
    updated_at TEXT DEFAULT (datetime('now'))
);
```

**Default settings to seed:**
```python
SETTINGS = [
    ("blog_url",       "https://money-and-mode.com", "Blog URL",         "general"),
    ("author_name",    "Kabir Shah",                 "Author/Pen Name",  "general"),
    ("adsense_target", "5000",                       "AdSense Threshold","traffic"),
    ("ezoic_target",   "1000",                       "Ezoic Threshold",  "traffic"),
    ("pub_days",       "Tuesday,Friday",             "Publish Days",     "content"),
]
```

**Effort estimate:** ~2 hours

---

### Infra 2 — DB Migrations

**What:** Right now if db.py changes (new table), you have to manually run `init_db()` or delete the DB. Need a clean migration system.

**Approach:** Simple version-counter in DB. On startup, compare `db_version` setting to current code version. If code > DB, run the migration SQL.

```python
MIGRATIONS = {
    1: """ALTER TABLE traffic ADD COLUMN affiliate_revenue REAL DEFAULT 0;""",
    2: """CREATE TABLE IF NOT EXISTS digest_edits (...);""",
    3: """CREATE TABLE IF NOT EXISTS gsc_data (...);""",
    4: """CREATE TABLE IF NOT EXISTS settings (...);""",
}
```

**Effort estimate:** ~1 hour

---

### Infra 3 — Article Quick-Add Form

**What:** Right now adding a new article to the dashboard means editing `seed.py` and reseeding. Need a form inside Pipeline tab to add planned articles.

**Add to Pipeline tab:**
```
[ + Add Article ]
  Title | Keyword | Series | Publish Date | Status
  [ Save ]
```

**Backend:**
- `POST /api/articles` — create article row
- `PUT /api/articles/{id}` — update status, publish_date
- `DELETE /api/articles/{id}` — remove planned article

**Effort estimate:** ~2 hours

---

### Infra 4 — Export / Backup

**What:** One-click export of all dashboard data as JSON. Useful before any big changes.

**Button:** In settings or overview → "Export All Data (JSON)"

**Backend:**
- `GET /api/export` — dumps all tables to JSON, returns as downloadable file

**Effort estimate:** ~1 hour

---

## Build Order Recommendation

Do these in sequence — each phase takes 1–2 sessions:

| Order | Phase | Task | Est. Time | Why first |
|-------|-------|------|-----------|-----------|
| 1 | Infra | **DB Migrations** | 1h | Needed before adding any new tables |
| 2 | Infra | **Settings Screen** | 2h | Removes hardcoded values; needed for AI Writer later |
| 3 | Infra | **Article Quick-Add form** | 2h | Stop editing seed.py just to add a planned article |
| 4 | **Phase 3** | **Screen 9 — Digest Editor** | 4h | content_curator.py already exists — just needs a UI |
| 5 | **Phase 3** | **Screen 10 — Sources Manager** | 3h | Natural companion to Digest Editor |
| 6 | Phase 5 | **Screen 13 — Social Queue** | 5h | Biggest daily time-saver after Phase 3 |
| 7 | Phase 4 | **Screen 11 — Revenue Tracker** | 3h | Needed once AdSense starts |
| 8 | Phase 4 | **Screen 12 — SEO Dashboard** | 4h | GSC paste mode — drives organic growth decisions |
| 9 | Phase 5 | **Screen 15 — Alerts** | 3h | Never miss a deadline or keyword milestone |
| 10 | Phase 5 | **Screen 14 — AI Writer** | 6h | Most complex — needs Claude API key + prompt tuning |
| 11 | Infra | **Export / Backup** | 1h | Nice to have, do last |

---

## Effort Summary

| Phase | Task | Est. Hours |
|-------|------|-----------|
| Infra | DB Migrations | 1h |
| Infra | Settings Screen | 2h |
| Infra | Article Quick-Add form | 2h |
| **Phase 3** | **Screen 9 — Digest Editor** | **4h** |
| **Phase 3** | **Screen 10 — Sources Manager** | **3h** |
| Phase 5 | Screen 13 — Social Queue | 5h |
| Phase 4 | Screen 11 — Revenue Tracker | 3h |
| Phase 4 | Screen 12 — SEO Dashboard | 4h |
| Phase 5 | Screen 15 — Alerts | 3h |
| Phase 5 | Screen 14 — AI Writer | 6h |
| Infra | Export / Backup | 1h |
| | **Total** | **~34h** |

At 2–3 hours per session: ~12–17 sessions to complete everything.

---

## What Each Phase Unlocks

| After completing… | You can… |
|-------------------|----------|
| Infra 2+3 | Add new articles from the dashboard (no more seed.py edits) |
| Screen 9+10 | Run content_curator.py on Monday, edit Kabir's take in browser, publish digest to WordPress — 30 min/week |
| Screen 13 | See exactly what to post today + clipboard-assist Instagram — saves 15 min/post |
| Screen 11 | Know your monthly blog income at a glance |
| Screen 12 | Spot keyword gaps and fix them — drives organic growth |
| Screen 15 | Never miss a publish deadline or keyword milestone |
| Screen 14 | Draft new articles in 10 min instead of 2 hours |

---

## Files That Need Changing (per task)

| Task | Files to edit |
|------|--------------|
| Infra 2 (migrations) | `db.py` |
| Infra 1 (settings) | `db.py`, `app.py`, `seed.py`, `static/index.html` |
| Infra 3 (quick-add) | `app.py`, `static/index.html` |
| Screen 9 (digest) | `app.py`, `db.py`, `static/index.html` |
| Screen 10 (sources) | `app.py`, `static/index.html` (reads sources.json directly) |
| Screen 13 (queue) | `app.py`, `static/index.html` |
| Screen 11 (revenue) | `db.py`, `app.py`, `static/index.html` |
| Screen 12 (SEO) | `db.py`, `app.py`, `static/index.html` |
| Screen 15 (alerts) | `app.py`, `static/index.html` |
| Screen 14 (AI writer) | `app.py`, `static/index.html`, `dashboard/prompts/` (new folder) |
| Infra 4 (export) | `app.py`, `static/index.html` |

---

## Decisions Needed from Sandip

Before building, confirm these:

1. **Screen 14 (AI Writer)** — do you want to use Claude API directly from the dashboard? Needs `CLAUDE_API_KEY` in `.env` and costs per call (~$0.01 per article draft). Worth it?

2. **Screen 12 (SEO)** — start with paste-CSV mode first (simpler), or should I build GSC API integration from the start? GSC API needs OAuth setup.

3. **Screen 13 (Social Queue)** — Twitter posting can be automated (via Bearer Token + tweepy). Instagram must remain clipboard-assist (Instagram blocks bots). OK with hybrid?

4. **Revenue currency** — track in ₹ (INR) or $ (USD) or both? AdSense pays in $ but you think in ₹.

5. **Phase priority** — the build order above prioritises Digest and Social Queue first. Is that right, or do you want Revenue Tracker sooner?

---

*Plan saved: June 7, 2026*  
*Review this → tell Claude which task to start with → build in sequence*
