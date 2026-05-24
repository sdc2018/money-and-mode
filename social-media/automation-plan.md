# Social Media Automation Plan
**Site:** money-and-mode.com | **Created:** May 24, 2026

This document describes how social media posting is automated using Claude and Claude Code.

---

## Architecture Overview

```
New Article Published (WordPress)
         │
         ▼
Claude adds to queue.json
(captions pre-written for all 3 platforms)
         │
         ▼
Claude Code runs /social-post
(reads queue → verifies accounts → posts → marks done)
         │
    ┌────┴─────────┬──────────────┐
    ▼              ▼              ▼
 Pinterest      Instagram        X/Twitter
 (via browser) (via browser)  (via browser)
    │              │              │
    ▼              ▼              ▼
queue.json updated: status → "posted"
```

---

## Files

| File | Purpose |
|------|---------|
| `social-media/queue.json` | The single source of truth — all pending + posted items |
| `social-media/automation-plan.md` | This file — architecture reference |
| `social-media/growth-plan.md` | Strategy and milestones |
| `CLAUDE.md` | Publishing workflow — social step is Step 5 |

---

## How queue.json Works

Every article gets entries added for each platform when it is published. Structure:

```json
{
  "accounts": {
    "instagram": "fun_in_life71",
    "twitter": "justIndia25",
    "pinterest": "sandip2787"
  },
  "pending": [ ... posts to be made ... ],
  "posted":  [ ... completed posts ... ],
  "threads_pending": [ ... Twitter threads ... ]
}
```

Each pending item has:
- `id` — unique identifier (e.g. `post-74-instagram`)
- `article_id`, `article_url`, `article_title`
- `platform` — `instagram`, `twitter`, `pinterest`
- `post_type` — `tweet`, `thread`, `pin` (for twitter)
- `caption` — ready-to-paste text
- `image_wp_id` — WordPress media ID for the diagram
- `board` — Pinterest board name (for pins)
- `status` — `pending` | `posted` | `skipped`
- `added` — date added

---

## Claude Code Automation — How to Trigger

### Option A: Run on demand (now)
In Claude Code, type:
```
Process the social media queue at social-media/queue.json
Post all pending items. Verify account handles first.
```

### Option B: Slash command (recommended)
Add to `.claude/commands/social-post.md`:
```
Process social-media/queue.json.
For each pending item:
1. Open the platform in the browser MCP tab
2. Verify the active account matches accounts.{platform}
3. If wrong account — STOP and report. Do not post.
4. Post the content using browser automation
5. Update queue.json: move to posted[], add posted_date
Report a summary when done.
```
Then run: `/social-post`

### Option C: Scheduled automatic posting (Phase 2)
Use Claude Code's scheduled tasks to run the queue processor:
- Every Tuesday and Friday (publish days) at 10am IST
- Checks for new pending items and posts them
- Sends a summary notification when done

---

## Step-by-Step Posting Process (Claude follows this)

### Before ANY post:
1. Read `queue.json` — identify first pending item
2. Navigate to `accounts.verify_urls[platform]`
3. Confirm active username matches `accounts[platform]`
4. **If mismatch: STOP. Tell Sandip. Do not proceed.**

### Posting to Instagram:
1. Navigate to `https://www.instagram.com/`
2. Click "+" (New Post)
3. Upload image from WordPress (fetch URL from WP media ID, save locally if needed)
4. Paste caption from queue item
5. Submit post
6. Confirm post appears on profile
7. Update queue.json: status → "posted", add posted_date

### Posting to X/Twitter (tweet):
1. Navigate to `https://x.com/`
2. Confirm logged-in handle is @justIndia25
3. Click "Post" / compose box
4. Paste caption (already includes URL)
5. Click Post
6. Confirm tweet appears
7. Update queue.json

### Posting to X/Twitter (thread):
1. Navigate to `https://x.com/`
2. Confirm handle
3. Open compose, paste Tweet 1
4. Click "+" to add next tweet in thread
5. Paste Tweet 2 through 6
6. Post all
7. Update queue.json

### Posting to Pinterest (pin):
1. Navigate to `https://www.pinterest.com/`
2. Confirm logged in as sandip2787
3. Click "Create" → "Create Pin"
4. Upload image (from WP media URL)
5. Paste title and description from queue item
6. Select board from `board` field
7. Add destination URL from `article_url`
8. Publish pin
9. Update queue.json

---

## When a New Article is Published — Claude's Checklist

After creating the WordPress post, Claude must:

1. **Write captions** for all 3 platforms (Instagram, X tweet, Pinterest)
2. **Write Twitter thread** (6 tweets) if article is featured/major
3. **Add all entries to queue.json** under `pending`
4. **If Sandip confirms "post now"** → run the posting process immediately
5. **Otherwise** → leave in queue for next posting session

Caption template to follow is in `growth-plan.md` → Caption Templates section.

---

## Image Handling for Social Posts

For posts with `image_wp_id`:
1. Fetch image URL from WordPress: `GET /wp-json/wp/v2/media/{image_wp_id}`
2. The `source_url` gives the full PNG URL
3. For Instagram/Pinterest: download the image to a temp file, then upload via browser

For posts with `image_wp_id: null` (no diagram yet):
1. Create a simple quote card using the article's key insight
2. Use brand colours (#2D6A4F green, #1a1a2e dark, #F9F7F4 background)
3. Size: 1080×1080 for Instagram, 1000×1500 for Pinterest

---

## Phase Rollout

### Phase 1 (Now — active)
- Manual trigger: Sandip asks Claude to post
- Claude reads queue, verifies handles, posts
- Queue.json updated after each post

### Phase 2 (Month 2–3)
- Claude Code slash command: `/social-post`
- Run after each article publishes
- Sandip reviews the summary and approves

### Phase 3 (Month 4+)
- Scheduled task: auto-runs every Tue + Fri
- Claude posts and sends completion summary
- Sandip only needs to intervene for errors or account issues

---

## Safety Rules (Hardcoded — Cannot Be Skipped)

1. **Always verify active account handle** before any post
2. **Never switch accounts** without explicit Sandip instruction
3. **Never post** if the wrong account is active
4. **Always read** captions from queue.json — never improvise
5. **Always update** queue.json after posting (posted vs pending)
6. **Report any errors** immediately — don't retry silently

---

## Current Queue Status

Run this to check: open `social-media/queue.json` and count items by status.

As of May 24, 2026:
- **Pending:** 18 posts (6 articles × 3 platforms) + 3 Twitter threads
- **Posted:** 0
- **Platforms:** Instagram @fun_in_life71, Twitter @justIndia25, Pinterest @sandip2787

---

*Maintained by Claude | money-and-mode project*
