# money-and-mode.com — Project Status

**Site:** https://money-and-mode.com  
**Site Name:** Fun in the Life  
**Tagline:** From Daily Growth to Wealth: A Life Well Lived  
**Last Updated:** May 21, 2026 (Session 4 — Diagrams live on all 3 articles; MonsterInsights OAuth done; Pinterest @sandip2787 created)  

---

## Phase Overview

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 | Site audit, content foundation, SEO setup | 🟡 In Progress |
| Phase 2 | Content engine (AI + Financial Freedom series) | 🔵 Planning |
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
| 4–10 | See content calendar | Various | 📝 Planned |

### Financial Freedom Series
| # | Title | Status |
|---|-------|--------|
| 1–8 | Pending Sandip's initial thoughts | ⏳ Awaiting input |

**All article files:** `/articles/`  
**Content calendar + 10 ideas:** `/articles/10-article-ideas-content-calendar.md`

### Diagrams & Images (Session 4)

| File | WordPress ID | Used In | Description |
|------|-------------|---------|-------------|
| `assets/images/ai-in-your-life.svg` | 80 (PNG) | Post 74 | Wheel diagram — 8 ways AI is in daily life |
| `assets/images/time-savings-chart.svg` | 81 (PNG) | Post 76 | Bar chart — time saved before/after AI (4 tasks) |
| `assets/images/ai-job-risk.svg` | 82 (PNG) | Post 77 | Two-column — disrupted roles vs thriving roles |

All diagrams are custom SVG (800px wide, Georgia serif font, brand colours), uploaded as PNG to WordPress and embedded in article content with captions.

---

## 12-Week Publishing Calendar

**Schedule:** Tuesday + Friday | 2 articles/week | 24 total articles

| Week | Dates | Articles |
|------|-------|---------|
| 1 | May 26, 30 | AI Everyday Life ✅ + AI Save Time ✅ |
| 2 | Jun 3, 6 | Will AI Take My Job ✅ + What is ChatGPT |
| 3 | Jun 10, 13 | 10 Free AI Tools + How to Talk to AI |
| 4 | Jun 17, 20 | AI for Parents + AI & Healthcare |
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

| Platform | Handle | Status |
|----------|--------|--------|
| Pinterest | @sandip2787 (sdc67@yahoo.com) | ✅ Created |
| Instagram | To be created | ⚪ Phase 3 |
| Facebook Page | To be created | ⚪ Phase 3 |
| Twitter/X | To be created | ⚪ Phase 3 |
| YouTube | To be created | ⚪ Phase 3 |

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

## Security Status

✅ **Wordfence active** — brute force protection running on /wp-login.php  
✅ **WordPress version tag hidden** — removed via functions.php, verified on live site  
✅ **GA4 tracking live** — G-LR3QLHFKBH tag firing on all pages

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
- [ ] Write next batch of articles (ChatGPT explained, Free AI tools, Talk to AI)
- [ ] Get Sandip's financial freedom initial thoughts → write series
- [x] Pinterest account created — @sandip2787 (sdc67@yahoo.com) — Phase 3 begins
- [ ] Apply for Google AdSense when traffic hits 5,000/month

---

*Auto-generated and maintained by Claude | money-and-mode project*
