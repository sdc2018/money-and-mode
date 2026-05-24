# Social Media Scripts — Setup Guide

How to get your API credentials and run the growth automation scripts.

---

## Quick Start

```bash
cd /Users/sandip/Projects/money-and-mode
cp .env.example .env
# Fill in your credentials (see below)
pip install requests python-dotenv
```

---

## Pinterest API Setup

**Time needed:** ~15 minutes  
**Cost:** Free (Pinterest API is free for standard use)

### Step 1 — Create a Pinterest Developer App

1. Go to **https://developers.pinterest.com/apps/**
2. Log in with your Pinterest account (`sandip2787`)
3. Click **Create App**
4. Fill in:
   - App name: `money-and-mode automation`
   - Description: `Posting pins for money-and-mode.com blog`
   - Website: `https://money-and-mode.com`
5. Click **Create**

### Step 2 — Generate an Access Token

1. In your app dashboard, click **Generate Token** (or "User Token")
2. Select these scopes:
   - `boards:read` — to list your boards and get board IDs
   - `pins:write` — to create pins
3. Click **Generate Token**
4. Copy the token — it starts with something like `pina_...`

### Step 3 — Add to .env

```
PINTEREST_ACCESS_TOKEN=pina_your_token_here
```

### Step 4 — Test it

```bash
python social-media/scripts/pinterest_growth.py --boards
```

You should see your boards listed with their IDs. If you see your 3 boards:
- AI Tips & Tools
- Money & Financial Freedom
- Life, Growth & Daily Habits

You're ready to go.

### Step 5 — Create all 18 pin variations

```bash
# All articles, all variations (recommended — run once)
python social-media/scripts/pinterest_growth.py --all

# Or one article at a time:
python social-media/scripts/pinterest_growth.py --article 74
python social-media/scripts/pinterest_growth.py --article 76
python social-media/scripts/pinterest_growth.py --article 77
python social-media/scripts/pinterest_growth.py --article 110
python social-media/scripts/pinterest_growth.py --article 112
python social-media/scripts/pinterest_growth.py --article 115
```

**What this does:** Creates 3 pin variations per article (same image, different title/description) across the correct boards. Pinterest treats these as fresh pins and distributes each one separately — this is the single biggest lever for Pinterest reach.

---

## Twitter / X API Setup

**Time needed:** ~10 minutes  
**Cost:** Free tier is enough for FINDING conversations. Posting requires paid plan.

### For conversation finding (free — do this first)

1. Go to **https://developer.twitter.com/en/portal/dashboard**
2. Sign in with your X account (`@justIndia25`)
3. Click **Create Project** → name it `money-and-mode`
4. Create an App inside the project
5. Go to **Keys and Tokens** tab
6. Under **Bearer Token**, click **Generate**
7. Copy the token

Add to `.env`:
```
TWITTER_BEARER_TOKEN=AAAA...your_token_here
```

Test it:
```bash
python social-media/scripts/twitter_growth.py --find --topic ai
```

You'll see the top tweets in the AI niche right now — sorted by engagement. These are your reply targets.

### For posting tweets (optional — requires paid plan)

Twitter's free API tier doesn't allow posting. To post programmatically:
- **Basic plan** ($100/month) — allows up to 1,500 tweets/month
- **Pro plan** ($5,000/month) — not needed for a blog

**Honest advice:** For posting, just do it manually from the X app. It's fast and you can customise each tweet. The real value of `twitter_growth.py` is the **conversation finder** — that's free and that's where the growth actually happens.

If you do get the Basic plan, add all 5 Twitter credentials to `.env` and the `post_tweet()` function will work (recommend using `tweepy` library instead of manual OAuth).

---

## Instagram API Setup (future)

**Note:** Instagram's API only supports Business/Creator accounts connected to a Facebook Page. It's more complex to set up.

**Time needed:** 45–60 minutes  
**Cost:** Free

Steps overview:
1. Convert Instagram account to a Business account (Settings → Account → Switch to Professional)
2. Connect it to a Facebook Page (create one for money-and-mode.com if needed)
3. Create a Facebook Developer App at https://developers.facebook.com/apps/
4. Add Instagram Graph API product
5. Generate a long-lived Page Access Token
6. Get your Instagram Business Account ID

This is worth doing once you're regularly publishing — lets you schedule posts via API. For now, posting manually is faster to set up.

---

## Daily Workflow (Twitter Growth)

The single most effective Twitter growth action:

```bash
# Every morning — find who to reply to today
python social-media/scripts/twitter_growth.py --find

# Check target accounts' latest tweets
python social-media/scripts/twitter_growth.py --targets
```

Then open X, find the tweets shown, and reply within the first hour using Kabir Shah's voice:
- Agree + add a layer from 25yr experience
- Surprising counterpoint (gets more replies back)
- "India-specific angle" hooks work especially well
- End with a question

One sharp reply on a tweet with 10K+ likes can bring 50–200 new followers in a day. This beats posting 10 original tweets into the void.

---

## Article Expansion — Adding New Articles to pinterest_growth.py

When you publish a new article, add it to `ARTICLE_PINS` in `pinterest_growth.py`:

```python
NEW_ARTICLE_ID: {
    "url": "https://money-and-mode.com/your-article-slug/",
    "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-your-image.png",
    "board": "AI Tips & Tools",  # or "Money & Financial Freedom" / "Life, Growth & Daily Habits"
    "variations": [
        {
            "title": "Pin Title Variation 1 (max 100 chars)",
            "description": "Description with keyword and link. money-and-mode.com\n\n#Hashtag1 #Hashtag2",
        },
        {
            "title": "Pin Title Variation 2",
            "description": "Different angle on the same article...",
        },
        {
            "title": "Pin Title Variation 3",
            "description": "Third hook, different audience segment...",
        },
    ],
},
```

Then run:
```bash
python social-media/scripts/pinterest_growth.py --article NEW_ARTICLE_ID
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `.env` | Your actual credentials (never commit) |
| `.env.example` | Template — commit this to git |
| `social-media/queue.json` | Article and post tracking |
| `social-media/scripts/pinterest_growth.py` | Pinterest API multi-variation pin creator |
| `social-media/scripts/twitter_growth.py` | Twitter conversation finder + thread poster |

---

*Last updated: May 24, 2026*
