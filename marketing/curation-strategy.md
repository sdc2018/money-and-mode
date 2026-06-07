# Content Curation Strategy
## "I read the internet so you don't have to"

---

## The Big Idea

Readers don't have time to follow 20 sources on AI, finance, and life.
Kabir Shah does it for them — curates the best 9 pieces each week with a short, personal take on why each one matters.

Published every Sunday as:
1. **Blog post** — "Weekly Digest: AI, Money & Life" — gets indexed by Google, served ads
2. **Email newsletter** — sent to subscribers (future)
3. **Social posts** — Instagram, X, Facebook all promote it

This is exactly what Morning Brew, The Hustle, and Farnam Street do.
The value is not the links. The value is **Kabir's judgment + commentary**.

---

## Why This Works for Traffic + Ads

**For traffic:**
- Digest posts rank for "best AI articles this week", "financial freedom reads", etc.
- People bookmark the site and return weekly — repeat visitors
- Each digest has 9 outbound links → Google sees it as a resource page → better ranking
- Social posts about the digest drive new followers back to the blog

**For ads:**
- Digest readers are in "learning mode" — highly receptive to relevant ads
- AI digest page → AI tool ads (ChatGPT Plus, Coursera, GitHub Copilot)
- Finance digest → Zerodha, Groww, finance courses
- Life digest → Health apps, book recommendations
- AdSense automatically matches ads to content — digest pages naturally attract premium ads

**Expected RPM (revenue per 1,000 visitors) on digest pages:**
- 2–4× higher than regular blog posts (because visitors are clicking around more)
- A digest page with 500 visitors/month could earn as much as a regular article with 1,500 visitors

---

## The Format (Every Weekly Digest Post)

```
TITLE: "Weekly Digest: [Month Day] — AI, Money & Life"
SLUG: /weekly-digest-[date]/
CATEGORY: Weekly Digest (new WP category)

INTRO (50 words):
"Every week I go through dozens of articles, videos, and posts across AI, money, and life.
These 9 are worth your time. I've added a short note on why I picked each one."

━━━━━━━━━━━━━━━━━━━━━━━━━━
## 🤖 AI & Technology (3 picks)

### 1. [Article Title] — [Source]
> Kabir's take: [2 sentences — why this matters for our non-technical reader. 
  Written in warm, wise voice. What should they do with this information?]

[Brief excerpt or summary — 2-3 sentences]
[Read more →](URL)

---

### 2. [Article/Video Title] — [Source]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━
## 💰 Financial Freedom (3 picks)
...

━━━━━━━━━━━━━━━━━━━━━━━━━━
## 🌱 Life & Personal Growth (3 picks)
...

━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTRO:
"If something here was useful, share it with one person who'd benefit.
Subscribe to get this in your inbox every Sunday."
[EMAIL SUBSCRIBE FORM]
```

---

## "Kabir's Take" — Voice Guide

Every curated piece needs 2 sentences in Kabir's voice.
Not a summary. A perspective.

**Bad (just a summary):**
> "This article explains how AI is being used in healthcare."

**Good (Kabir's voice):**
> "What struck me reading this: AI isn't replacing doctors — it's giving them a second pair of tireless eyes. For anyone worried about AI in medicine, this is reassuring without being naive."

**Formula:**
- Sentence 1: what struck you / what's surprising / what's counterintuitive
- Sentence 2: what the reader should do with this (read it if X, skip if Y)

**Draw from Sandip's actual perspective:**
- 25 years in software — can spot hype vs. substance
- Lives in India — can add "India angle" to global content
- Believes in simplicity, family, financial freedom — filter content through these values

---

## Sources (Monitored Automatically)

See `marketing/sources.json` for full list. Summary:

**AI/Technology (9 sources):**
MIT Technology Review, The Verge, VentureBeat, TechCrunch, OpenAI Blog, Google AI Blog, Harvard Business Review, Wired, BBC Technology
+ YouTube: AI Explained, Two Minute Papers, Fireship

**Financial Freedom (8 sources):**
Mr. Money Mustache, JL Collins, Financial Samurai, CNBC Make It, Economic Times, Moneycontrol, NerdWallet, Investopedia
+ YouTube: Graham Stephan, Andrei Jikh, Warikoo, Akshat Shrivastava

**Life & Motivation (6 sources):**
James Clear, Mark Manson, Psychology Today, Harvard Business Review, Tim Ferriss, Zen Habits
+ YouTube: Matt D'Avella, Thomas Frank

**Total monitored:** 23 blogs + 9 YouTube channels = 32 sources checked weekly

---

## The Automation

### Every Sunday (scheduled task runs automatically at 7am)
1. `content_curator.py --fetch` — fetches all 32 sources, scores articles by relevance
2. Outputs: `social-media/digests/digest-[week].json` — ranked picks per topic
3. `content_curator.py --draft` — generates the WordPress post draft + social posts

### Sandip reviews (15 minutes Sunday morning)
1. Open `social-media/digests/draft-[week].md`
2. Read through 9 picks — remove any you don't like, add one you found yourself
3. Fill in "Kabir's take" for each (2 sentences per pick — the most important step)
4. Copy to WordPress → publish
5. Copy social posts from `social-media/digests/social-[week].json` → post on IG/X/Facebook

### Result
One Sunday morning ritual → 52 digest posts/year → compounding traffic + ad revenue

---

## Legal & Attribution

**Content curation is 100% legal when done correctly:**
- ✅ Link to original always (we do this)
- ✅ Quote briefly (2-3 sentences max from source)
- ✅ Add original commentary (the "Kabir's take" section)
- ✅ Never copy full articles
- ✅ Credit source and author clearly

This is how Flipboard, SmartBrief, The Browser, and every major newsletter curates content.
The 30-40% original commentary (Kabir's takes + intro + outro) makes this original work.

---

## Growth Path for the Digest

| Stage | Subscribers | Format | Revenue |
|-------|------------|--------|---------|
| Now | 0 | Blog post only | Ad revenue on page |
| Month 3 | 100 email subscribers | Blog + email | Ad revenue |
| Month 6 | 500 subscribers | Blog + email | Ad revenue + newsletter ads |
| Month 12 | 2,000 subscribers | Blog + email + paid tier | Sponsorship possible |
| Month 18 | 5,000 subscribers | Full media product | Dedicated sponsors $500+/issue |

---

## Adding New Sources

To add a new RSS feed to monitor:
1. Open `marketing/sources.json`
2. Add entry under the right topic with: name, rss URL, authority (1-5), type, notes
3. Run `python content_curator.py --fetch` to test it
4. Done — it will be checked every Sunday automatically

---

*The digest is the highest-leverage content type on the site:
one piece of content → traffic + email growth + ads + authority + social posts*
