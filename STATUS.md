# money-and-mode.com — Project Status

**Site:** https://money-and-mode.com  
**Site Name:** Fun in the Life  
**Tagline:** From Daily Growth to Wealth: A Life Well Lived  
**Last Updated:** June 7, 2026 (Session 10 cont. — Dashboard Sessions 1+2 COMPLETE: Phase 2 done earlier; now Infra (DB migrations, Settings screen, Article quick-add) + Phase 3 (Digest Editor, Sources Manager) all built. Dashboard now has 11 tabs. All 11 API endpoints tested 200 OK. http://localhost:8765)  
**Pen Name:** Kabir Shah (technology entrepreneur, 25 years in software/AI, India) — used for all author attribution  

---

## Phase Overview

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 | Site audit, content foundation, SEO setup | 🟡 In Progress |
| Phase 2 | Content engine (AI + Financial Freedom series) | 🟡 In Progress |
| Phase 3 | Social media handles + distribution | ⚪ Not Started |
| Phase 4 | Monetisation (Google Ads / ad framework) | ⚪ Not Started |

---

## Hosting & Infrastructure

| Item | Detail |
|------|--------|
| Host | IONOS Inc. (Philadelphia, PA) |
| IP | 74.208.236.24 |
| Registrar | IONOS SE |
| Domain created | Jan 14, 2025 |
| Domain expires | Jan 14, 2027 |
| Contract status | ⚠️ Cancellation filed — valid until Jan 2027. Decide before then. |
| WordPress version | 6.9 (latest) |
| Theme | Extendable v2.1.4 |
| PHP | 8.1.34 / Apache |
| IONOS Customer ID | 309669888 |
| Account email | sandipc@gmail.com |

---

## Site Analytics (as of May 21, 2026)

**Source:** analytics.ionos.com (last ~30 days)

| Metric | Value | Change |
|--------|-------|--------|
| Total Visitors | 2,344 | -9.1% |
| Page impressions/session | 2.16 | +22.1% |

### Top Pages by Impressions
| Page | Impressions | Change | Note |
|------|------------|--------|------|
| /wp-login.php | 2,879 | +43.2% | ⚠️ Mostly bot/brute-force traffic |
| /index.php | 982 | -28.6% | |
| / (homepage) | 605 | -6.5% | |

### Bot Traffic Breakdown (by impressions)
| Bot | Share | Change |
|-----|-------|--------|
| GPTBot (OpenAI) | 18.14% | +300% |
| Amazonbot | 17.18% | -22.6% |
| Barkrowler | 12.65% | +32.5% |
| AhrefsBot | 10.26% | -25.9% |
| Googlebot Desktop | 9.07% | +2.7% |
| MJ12bot | 5.97% | — |
| SERankingBot | 5.73% | 0% |
| Googlebot Mobile | 4.06% | -26.1% |
| Pinterestbot | 2.63% | -26.7% |

**Key insight:** Majority of impressions are bots, not real humans. The /wp-login.php page getting 2,879 hits is a brute-force attack signal — real visitors don't hit that page repeatedly.

---

## SEO Status

| Item | Status |
|------|--------|
| AIOSEO plugin | ✅ Installed (v4.9.7.2) |
| Overall optimization score | 65% |
| Meta descriptions | ✅ Set on all 3 published articles (Posts 74, 76, 77) |
| WordPress version hidden | ✅ Done | `remove_action('wp_head','wp_generator')` added to Extendable functions.php |
| Security headers | ❌ Missing (X-Frame-Options, CSP, XSS) |
| Google Search Console | ✅ Verified & connected | Property: https://money-and-mode.com/ |
| Google Analytics | ✅ Active | G-LR3QLHFKBH tag live on site; MonsterInsights connected to same ID |
| Sitemap submitted | ✅ Done | sitemap.xml submitted to Google Search Console |

### Immediate SEO fixes (30–60 min total)
1. Add meta descriptions via AIOSEO for all existing pages
2. In AIOSEO → Search Appearance → hide WordPress generator tag
3. Restrict /wp-json/ REST API or limit exposed info
4. Block /wp-login.php from non-admin IPs (or install Wordfence)
5. Connect Google Search Console + submit sitemap

---

## Active Plugins
- AIOSEO v4.9.7.2 (SEO)
- Broken Link Checker
- Ad Inserter (ready for ads - Phase 4)
- OMApp (email marketing)

---

## Content — Articles Written

### AI & Everyday Life Series
| # | Title | Keyword | Status |
|---|-------|---------|--------|
| 1 | How AI Is Changing Everyday Life | how AI is changing everyday life | ✅ Published (Post ID 74) |
| 2 | How to Use AI to Save 2 Hours Every Day | how to use AI to save time | ✅ Published (Post ID 76) |
| 3 | Will AI Take My Job? | will AI take my job | ✅ Published (Post ID 77) |
| 4 | What Is ChatGPT? | what is ChatGPT explained simply | 📋 Draft (Post ID 93) — publish Jun 6 |
| 5 | 10 Free AI Tools | best free AI tools for everyday use | 📋 Draft (Post ID 94) — publish Jun 10 |
| 6 | How to Talk to AI | how to use ChatGPT for beginners | 📋 Draft (Post ID 95) — publish Jun 13 |
| 7 | AI for Parents | AI for kids education | 📋 Draft (Post ID 96) — publish Jun 17 |
| 8 | AI & Healthcare | how AI is changing healthcare | 📋 Draft (Post ID 97) — publish Jun 20 |
| 9–24 | See content calendar | Various | 📝 Planned |

### Financial Freedom Series (Kabir Shah voice — US audience — FIRE at 31)
| # | Title | WP ID | Image ID | Status |
|---|-------|-------|----------|--------|
| 1 | I Sold My Company at 31. Here's What Financial Freedom Actually Felt Like. | 110 | 105 | ✅ Published |
| 2 | The Only Number That Determines Your Financial Freedom (Savings Rate) | 111 | 106 | 📋 Draft |
| 3 | If You Are Selling Your Time, You Will Never Be Free | 112 | 107 | ✅ Published |
| 4 | Stop Selling Your Time. Build Leverage Instead. | 113 | 108 | 📋 Draft |
| 5 | The 4% Rule Explained: What the Trinity Study Actually Said | 114 | 109 | 📋 Draft |
| 6 | Why "Passive Income" Is Mostly a Lie | — | — | 📝 Written + SVG created (ff-06-passive-income-truth) — needs WP upload |
| 7 | The Psychology of Money — Why Smart People Stay Broke | — | — | 📝 Written + SVG created (ff-07-money-psychology) — needs WP upload |
| 8 | Index Funds — The Boring Investment That Beats Almost Everyone | — | — | 📝 Written + SVG created (ff-08-index-funds) — needs WP upload |

**Series diagrams:** `/assets/images/ff-01-*.svg` through `ff-08-*.svg` — ff-01 to ff-05 uploaded as 2× PNGs (IDs 105–109); ff-06/07/08 SVGs created locally, pending upload

**All article files:** `/articles/`  
**Content calendar + 10 ideas:** `/articles/10-article-ideas-content-calendar.md`

### Diagrams & Images

| File | WordPress ID | Used In | Description |
|------|-------------|---------|-------------|
| `assets/images/ai-in-your-life.svg` | 80 (PNG) | Post 74 | Wheel diagram — 8 ways AI is in daily life |
| `assets/images/time-savings-chart.svg` | 81 (PNG) | Post 76 | Bar chart — time saved before/after AI (4 tasks) |
| `assets/images/ai-job-risk.svg` | 82 (PNG) | Post 77 | Two-column — disrupted roles vs thriving roles |
| `assets/images/what-is-chatgpt.svg` | 88 (PNG) | Post 93 | 3-step flow: you type → AI thinks → you get answer |
| `assets/images/10-free-ai-tools.svg` | 89 (PNG) | Post 94 | Grid of 10 AI tools with use cases |
| `assets/images/how-to-talk-to-ai.svg` | 90 (PNG) | Post 95 | Before/after: vague ask vs. clear ask (4 examples) |
| `assets/images/ai-for-parents.svg` | 91 (PNG) | Post 96 | 5 ways AI helps children learn better |
| `assets/images/ai-healthcare.svg` | 92 (PNG) | Post 97 | 5 ways AI is changing healthcare |
| `assets/images/ff-01-three-phases.svg` | 105 (PNG) | Post 110 | 4-phase journey: Build → Exit → Build Free → Own Time |
| `assets/images/ff-02-savings-rate.svg` | 106 (PNG) | Post 111 | Savings rate table (5%→75%) with years to freedom |
| `assets/images/ff-03-calendar-contrast.svg` | 107 (PNG) | Post 112 | Before/after calendar: packed meetings vs owned time |
| `assets/images/ff-04-three-income-modes.svg` | 108 (PNG) | Post 113 | Employee / Freelancer / Entrepreneur income modes |
| `assets/images/ff-05-freedom-number.svg` | 109 (PNG) | Post 114 | Freedom number table + 25x formula + rate benchmarks |
| `assets/images/ff-06-passive-income-truth.svg` | — (pending upload) | — | Passive income myth vs reality — 3 that work vs 5 that aren't |
| `assets/images/ff-07-money-psychology.svg` | — (pending upload) | — | 5 money psychology bugs table with fixes |
| `assets/images/ff-08-index-funds.svg` | — (pending upload) | — | Index fund vs active fund side-by-side comparison |
| `assets/images/lm-connection-starts-at-home.svg` | 117 (PNG) | Post 118 | Hub diagram — Home → Self/Spouse/Children/Community/Society |

All diagrams are custom SVG (800px wide, Georgia serif font, brand colours), uploaded as PNG to WordPress and embedded in article content.

---

## 12-Week Publishing Calendar

**Schedule:** Tuesday + Friday | 2 articles/week | 24 total articles

| Week | Dates | Articles |
|------|-------|---------|
| 1 | May 26, 30 | AI Everyday Life ✅ + AI Save Time ✅ |
| 2 | Jun 3, 6 | Will AI Take My Job ✅ + What is ChatGPT 📋 |
| 3 | Jun 10, 13 | 10 Free AI Tools 📋 + How to Talk to AI 📋 |
| 4 | Jun 17, 20 | AI for Parents 📋 + AI & Healthcare 📋 |
| 5–12 | Jun 24–Aug 15 | See full calendar in content-calendar.md |

---

## Monetisation Plan (Phase 4)

- **Ad Inserter plugin** already installed — ready for ad code
- **Google AdSense:** Apply once site has 20+ quality articles and consistent traffic
- **Requirement for AdSense approval:** Original content, privacy policy page, about page, contact page, no thin content
- **Alternative networks:** Ezoic (lower traffic threshold), Media.net, Monumetric
- **Recommended threshold:** Apply to AdSense when monthly visitors reach 5,000+

---

## Social Media (Phase 3)

**Blog email:** funInTheLife2@gmail.com — use for all blog accounts, API sign-ups, social registrations

| Platform | Handle | Status |
|----------|--------|--------|
| Pinterest | @sandip2787 (funInTheLife2@gmail.com) | ✅ Live — profile, 3 boards, articles pinned |
| Instagram | @fun_in_life71 | ✅ Live — https://www.instagram.com/fun_in_life71/ — bio set ✅, profile photo needed |
| Facebook Page | To be created | ⚪ Phase 3 — use funInTheLife2@gmail.com |
| Twitter/X | @justIndia25 | ✅ Live — bio set, articles tweeted |
| YouTube | To be created | ⚪ Phase 3 — use funInTheLife2@gmail.com |

---

## WordPress Housekeeping — Completed May 21, 2026

| Task | Status | Notes |
|------|--------|-------|
| Comments, pingbacks, trackbacks | ✅ Disabled | All turned off globally |
| WordPress core | ✅ Updated | 6.9 → 7.0 |
| Timezone | ✅ Fixed | Asia/Kolkata (IST, UTC+5:30) |
| Public registration | ✅ Disabled | "Anyone can register" = OFF |
| Permalinks | ✅ Confirmed | /%postname%/ — SEO-friendly |
| MonsterInsights (GA) | ✅ Connected | Active Profile: G-LR3QLHFKBH. Reports need OAuth wizard at MonsterInsights.com |
| IONOS Single Sign-On | ✅ Activated | Fixes IONOS dashboard login |
| Wordfence Security | ✅ Active | Firewall learning mode until May 28 |
| All plugins | ✅ Up to date | No updates needed |
| All themes | ✅ Up to date | No updates needed |
| Wordfence free license | ✅ Done by Sandip | License registered at wordfence.com |
| Hide WordPress version | ✅ Done | remove_action added to functions.php — verified live |
| Google Analytics GA4 | ✅ Tag live | G-LR3QLHFKBH on site. MonsterInsights reports need OAuth (manual step) |
| Google Search Console | ✅ Done | Property verified, sitemap.xml submitted |

---

## Author / Identity

| Item | Detail |
|------|--------|
| Pen name | **Kabir Shah** |
| WordPress display name | Kabir Shah (changed from "admin") |
| Author URL | https://money-and-mode.com/author/kabir-shah/ |
| About page | https://money-and-mode.com/about/ — live, full bio as Kabir Shah |
| Author description | Technology entrepreneur, 25 years in software/AI, based in India |
| Twitter | @justIndia25 |

---

## SEO & GEO Status

| Item | Status |
|------|--------|
| Traditional SEO (AIOSEO) | 🟡 65% score — improving |
| llms.txt (AI search) | ✅ Live at https://money-and-mode.com/llms.txt — auto-generated by AIOSEO |
| Google Search Console | ✅ Connected — 13 impressions, avg position 15.6 (Feb–May 2026) |
| Bing Webmaster Tools | ❌ Not yet set up — needed for ChatGPT/Copilot visibility |
| Author schema (E-E-A-T) | ✅ Configured — site set to "Person" (Kabir Shah, ID 1); user bio set; experience topics set |
| FAQ schema on articles | ❌ Not yet added |
| About page | ✅ Live with Kabir Shah bio |
| Privacy Policy page | ⚠️ Exists but has default WP content — needs review |
| Contact page | ✅ Live — custom contact form, sends to admin email, Twitter DM backup |

---

## Security Status

✅ **Wordfence active** — brute force protection running on /wp-login.php  
✅ **WordPress version tag hidden** — removed via functions.php, verified on live site  
✅ **GA4 tracking live** — G-LR3QLHFKBH tag firing on all pages  
✅ **Admin username hidden** — display name changed from "admin" to "Kabir Shah"  

---

## GitHub Repository

**Repo:** https://github.com/sdc2018/money-and-mode  
**Status:** ✅ Live  
**Branch:** main  

---

## Open Actions

- [x] Publish 3 articles — all live under "AI & Everyday Life" category (Post IDs: 74, 76, 77)
- [x] Complete Wordfence license — done by Sandip
- [x] Hide WP version — done via functions.php, verified live
- [x] GA4 tracking live — G-LR3QLHFKBH tag on site, MonsterInsights connected
- [x] MonsterInsights reports OAuth — completed by Sandip (Google login done)
- [x] Submit sitemap to Google Search Console — already verified and submitted
- [x] Add meta descriptions to 3 published articles via AIOSEO — live on all 3 posts
- [x] Add custom diagrams/images to all 3 published articles — live on site
- [x] Write articles 4–8 (ChatGPT, Free AI Tools, Talk to AI, AI for Parents, AI Healthcare) — all done, saved in /articles/
- [x] Create custom diagrams for articles 4–8 — 5 SVGs made, uploaded as PNGs (WP IDs 88–92)
- [x] Publish articles 4–8 as WordPress drafts — Post IDs 93–97, diagrams embedded, AIOSEO meta set
- [ ] Review & publish drafts 93–97 on schedule (Jun 6, 10, 13, 17, 20)
- [x] Write Financial Freedom series (FF-01 to FF-05) — DONE. Published FF-01 & FF-03; drafts FF-02/04/05
- [x] Pinterest account created — @sandip2787 (sdc67@yahoo.com) — Phase 3 begins
- [x] Pinterest profile set up — name "Fun in the Life", bio, website money-and-mode.com all live
- [x] Pinterest profile photo — uploaded by Sandip ✅
- [x] Pinterest boards created — "AI Tips & Tools", "Money & Financial Freedom", "Life, Growth & Daily Habits"
- [x] Pinterest pins created — all 3 articles pinned to AI Tips & Tools board with diagrams
- [ ] Pinterest Rich Pins — enable via schema validation (checking)
- [ ] Apply for Google AdSense when traffic hits 5,000/month
- [x] Create pen name Kabir Shah — WordPress display name + author URL updated
- [x] Write & publish About page as Kabir Shah — live at /about/
- [x] Hide 9 old placeholder posts — set to private, invisible to public & search engines
- [x] llms.txt live — AIOSEO auto-generates at https://money-and-mode.com/llms.txt
- [ ] Set up Bing Webmaster Tools — submit sitemap for ChatGPT/Copilot visibility
- [ ] Configure Author schema in AIOSEO (E-E-A-T)
- [ ] Add FAQ schema to published articles via AIOSEO
- [x] Contact page rebuilt — custom form live at /contact/, sends to admin email privately, Twitter DM backup
- [ ] Review Privacy Policy page content
- [x] Bing Webmaster Tools set up by Sandip ✅
- [x] Create 5 FF series SVG diagrams — done (ff-01 through ff-05)
- [x] Upload FF diagrams as PNGs to WordPress — IDs 105–109
- [x] Publish FF-01 "I Sold My Company at 31" — live at /i-sold-my-company-at-31-financial-freedom/
- [x] Publish FF-03 "If You Are Selling Your Time" — live at /selling-your-time-financial-freedom-time-ownership/
- [ ] Publish FF-02 (Savings Rate draft, ID 111) — schedule for next publishing slot
- [ ] Publish FF-04 (Build Leverage draft, ID 113) — schedule
- [ ] Publish FF-05 (4% Rule draft, ID 114) — schedule
- [x] Write FF-06/07/08 — all 3 articles written locally (passive income, money psychology, index funds)
- [x] Configure Author schema in AIOSEO — site set to Person (Kabir Shah), user bio updated, experience topics saved
- [x] Create diagrams for FF-06/07/08 — 3 SVGs done locally — still need WP upload + draft posts
- [ ] Upload FF-06/07/08 PNGs to WordPress media + create 3 draft posts
- [x] Create "Life & Motivation" WordPress category — ID 15
- [x] Write & publish "Family Heaven" article — live (Post 115)
- [x] Write "Connection Starts at Home" — draft (Post 118, diagram ID 117)
- [x] Add social media icons to homepage — X, Instagram, Pinterest icons live in "FOLLOW THE JOURNEY" section
- [x] Instagram bio set — "AI · Money · Life. Simple ideas for a better everyday. 🌱 money-and-mode.com"
- [ ] Instagram profile photo — add (Sandip to do on mobile, website link also needs mobile app)
- [ ] Instagram first posts — share article diagrams with captions (per new publishing workflow)
- [x] CLAUDE.md updated — full publishing workflow added (write → diagram → WordPress → SEO → social → commit)
- [ ] Add FAQ schema to FF published articles via AIOSEO
- [ ] Review Privacy Policy page content
- [x] Build Pinterest growth automation script — social-media/scripts/pinterest_growth.py — 3 pin variations × 6 articles = 18 pins ready to post via Pinterest API v5
- [x] Build Twitter growth automation script — social-media/scripts/twitter_growth.py — finds high-engagement conversations to reply to; loads target account list + topic search queries
- [x] Create .env.example — credential template for Pinterest, Twitter, Instagram, WordPress API keys
- [x] Create social-media/scripts/SETUP.md — step-by-step instructions for getting each API token
- [x] Update .gitignore — .env protected from git commits
- [ ] **GET PINTEREST ACCESS TOKEN** — https://developers.pinterest.com/apps/ → Create App → Generate Token (scopes: boards:read, pins:write) → add to .env
- [ ] **GET TWITTER BEARER TOKEN** — https://developer.twitter.com/en/portal/dashboard → Create Project → Get Bearer Token → add to .env
- [ ] Run `python pinterest_growth.py --boards` to verify Pinterest API connection
- [ ] Run `python pinterest_growth.py --all` to post all 18 pin variations (run once, big reach boost)
- [ ] Run `python twitter_growth.py --find` daily for reply opportunities (free tier)

### Session 10 Pending (Jun 7, 2026)
- [ ] **Instagram post-115** (Family Connection) — final post from batch 1. Caption in clipboard. Image: ~/Downloads/ig-article-115.png. Post at https://instagram.com (verify handle = fun_in_life71 first)
- [ ] **Edit Instagram post-74** — was posted without caption. Open Instagram → find post → ⋯ → Edit → paste new caption (see batch-2-instagram notes or queue.json for improved caption)
- [ ] **Publish WP draft 93** (What is ChatGPT) — was due Jun 6, still draft. Go to WordPress dashboard → Posts → ID 93 → Publish
- [ ] **Create blog email** — blog@money-and-mode.com via IONOS email panel (see below)
- [ ] **Create Facebook Page** — Sandip to do. Page name: "Fun in the Life" or "Money & Mode". Connect to Instagram for cross-posting.
- [ ] **Post batch-2 Instagram** — 6 deeper posts ready in /social-media/future-posts/batch-2-instagram.md. Schedule Jun 17–Jul 4.
- [ ] **Upload FF-06/07/08 PNGs** to WordPress media + create 3 draft posts

### Blog Email Setup (Do This Once)
**Create:** `blog@money-and-mode.com`
**Where:** Login to IONOS → Email → Create Mailbox → use money-and-mode.com domain
**Why:** All social accounts (Instagram, Pinterest, Facebook, Twitter, YouTube) should use this one email. Currently all linked to personal emails.
**Steps:**
1. Login at ionos.com → "Email" section
2. Create mailbox: blog@money-and-mode.com
3. Set a strong password
4. Use this email when: creating Facebook Page, YouTube channel, any new social account

---

*Auto-generated and maintained by Claude | money-and-mode project*
