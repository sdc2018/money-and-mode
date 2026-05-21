# CLAUDE.md — money-and-mode.com Project Instructions

This file gives Claude full context to work on the money-and-mode.com blog project without needing re-explanation every session.

---

## About This Project

**Site:** https://money-and-mode.com  
**Site name:** Fun in the Life  
**Owner:** Sandip (sandipc@gmail.com | sandipc on GitHub as sdc2018)  
**Purpose:** Lifestyle blog covering AI in everyday life, financial freedom, motivation, and personal growth  
**Audience:** Regular people — laymen, not tech-savvy. Write simply, warmly, and wisely.  
**Hosting:** IONOS WordPress (WaaS) — contract expires Jan 2027  
**GitHub:** https://github.com/sdc2018/money-and-mode  

---

## About Sandip (Author Voice)

Sandip is a 50+ software entrepreneur based in India. He runs Cymetrix, a data/AI consulting company. He has:
- 25+ years in the software and technology business
- Deep technical knowledge but writes for non-technical people
- A philosophical, reflective, wisdom-first voice — draws from real life experience
- 11 years of personal journal entries with genuine life insights
- Sons: Mihir (SF, YC-funded startup) and Arnav
- Heavy daily user of Claude AI — understands AI from the inside

**His writing voice is:** warm, honest, conversational, wise. No corporate speak. No jargon. Like a wise friend explaining something over chai.

**Key life philosophy (from his journals):**
- "Take life as it comes. Just not resist anything."
- "Life is full of battle of mind and emotions nothing else."
- Values: family, peace, health over success and money
- Gratitude, letting go, consistency over intensity

When writing articles, weave in this perspective. Articles should feel like they come from someone who has lived, not just read about a topic.

---

## Content Strategy

### Active Series

**1. AI & Everyday Life** (primary series — 24 articles planned)
- Target: people who've heard of AI but haven't used it
- Tone: reassuring, practical, no jargon
- Keywords: see `/articles/10-article-ideas-content-calendar.md`

**2. Financial Freedom** (upcoming — awaiting Sandip's thoughts)
- Will cover: saving, investing, building passive income, mindset
- Audience: Indian middle class + global aspirational readers

**3. Life & Motivation** (existing site content)
- Morning routines, habits, mindset, personal growth

### Publishing Schedule
- 2 articles per week: Tuesday + Friday
- Target length: 800–1,500 words
- SEO plugin: AIOSEO (already installed)

---

## Article Writing Rules

Every article must have:
1. **Target keyword in title** (first 60 chars)
2. **Target keyword in first paragraph**
3. **Meta description** (max 155 chars) — write one for every article
4. **At least one H2 with keyword or variation**
5. **2–3 internal links** to other articles on the site
6. **Featured image alt text** with keyword
7. **Closing question** to invite comments
8. **No jargon** — if using a tech term, explain it immediately
9. **Short paragraphs** — max 3–4 sentences
10. **Personal angle** — always include one real-life example or personal perspective

### Article file format
Save articles in `/articles/` as `article-N-slug.md` with this header:
```
# Article Title
**Target keyword:** ...
**Secondary keywords:** ...
**Meta description:** ...
**Word count:** ~X
**Category:** ...
```

---

## Folder Structure

```
/money-and-mode/
├── CLAUDE.md                    ← You are here
├── STATUS.md                    ← Live project status — update after every session
├── articles/                    ← All written articles (AI series, financial freedom, etc.)
│   └── 10-article-ideas-content-calendar.md
├── financial-freedom/           ← Financial freedom series drafts
├── social-media/               ← Social media content (Phase 3)
├── ads/                        ← Ad setup notes (Phase 4)
└── assets/                     ← Images, logos, brand assets
```

---

## SEO Setup

**Plugin:** AIOSEO v4.9.7.2  
**Current score:** 65% (target: 90%+)  

**Fixes still needed:**
- Add meta descriptions to all existing pages
- Hide WordPress version (AIOSEO → Search Appearance)
- Submit sitemap to Google Search Console
- Connect Google Analytics GA4

**Keyword research tool:** Use search volume estimates. Target low-competition keywords first (under 5,000 searches/month with "low" difficulty). Build authority before chasing high-competition terms.

---

## Analytics

**IONOS Analytics:** https://analytics.ionos.com/  
**Google Analytics:** Not yet set up (add GA4)  
**Google Search Console:** Not yet confirmed connected  

**Current traffic (May 2026):**
- 2,344 visitors/month (-9.1% — declining, needs new content)
- Most traffic is bots (GPTBot, Amazonbot, crawlers)
- /wp-login.php getting 2,879 bot hits = brute force attacks
- Real human traffic is very low — new content will fix this

**Traffic goal:** 5,000 real human visitors/month → apply for Google AdSense

---

## Monetisation Roadmap

| Phase | Action | Trigger |
|-------|--------|---------|
| Now | Publish consistent content | Always |
| Phase 4 | Apply for Google AdSense | 5,000 visitors/month + 20 articles |
| Phase 4 | Test Ezoic (lower threshold) | 1,000 visitors/month |
| Phase 4 | Affiliate links (Amazon, tools) | Any time after 10 articles |
| Future | Newsletter / email list | After AdSense running |

**Ad Inserter plugin** is already installed — just needs ad codes.

---

## Social Media (Phase 3 — Not Started)

Platforms to create: Pinterest, Instagram, Facebook Page, Twitter/X, YouTube  
Pinterest is highest priority for lifestyle blog traffic.  
All handles to be created by Sandip — Claude will manage content posting after setup.

---

## GitHub

**Repo:** https://github.com/sdc2018/money-and-mode  
**Branch:** main  
**Commit convention:** `content: add article on [topic]` / `fix: [what was fixed]` / `docs: update STATUS.md`

Always update STATUS.md after any significant session and commit.

---

## Security Issues (Fix Soon)

1. **/wp-login.php brute force** — install Wordfence or add IP-based login restriction
2. **WordPress version exposed** — fix via AIOSEO
3. **No security headers** — add via Wordfence or .htaccess

---

## How to Start Any Session

1. Read `STATUS.md` for current state
2. Check open actions at bottom of STATUS.md
3. Ask Sandip: "What do you want to work on today?"
4. After session: update STATUS.md with what was done

---

## Things Claude Should Never Do

- Don't write in corporate/academic tone — always conversational
- Don't use jargon without explaining it
- Don't write generic AI content — always add Sandip's personal perspective
- Don't create content that sounds like it's written by a robot
- Don't publish to WordPress without Sandip confirming

---

*Last updated: May 21, 2026*
