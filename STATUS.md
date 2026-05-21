# money-and-mode.com — Project Status

**Site:** https://money-and-mode.com  
**Site Name:** Fun in the Life  
**Tagline:** From Daily Growth to Wealth: A Life Well Lived  
**Last Updated:** May 21, 2026 (Session 1 — Full housekeeping done)  

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
| Meta descriptions | ❌ Missing on most pages |
| WordPress version hidden | ❌ Exposed in HTML |
| Security headers | ❌ Missing (X-Frame-Options, CSP, XSS) |
| Google Search Console | ❌ Not confirmed connected |
| Google Analytics | ❌ Not confirmed — using IONOS analytics only |
| Sitemap submitted | ❌ Needs verification |

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
| 1 | How AI Is Changing Everyday Life | how AI is changing everyday life | ✅ Written |
| 2 | How to Use AI to Save 2 Hours Every Day | how to use AI to save time | ✅ Written |
| 3 | Will AI Take My Job? | will AI take my job | ✅ Written |
| 4–10 | See content calendar | Various | 📝 Planned |

### Financial Freedom Series
| # | Title | Status |
|---|-------|--------|
| 1–8 | Pending Sandip's initial thoughts | ⏳ Awaiting input |

**All article files:** `/articles/`  
**Content calendar + 10 ideas:** `/articles/10-article-ideas-content-calendar.md`

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
| Pinterest | To be created | ⚪ Phase 3 |
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
| MonsterInsights (GA) | ✅ Activated | Needs GA4 tracking ID connected |
| IONOS Single Sign-On | ✅ Activated | Fixes IONOS dashboard login |
| Wordfence Security | ✅ Active | Firewall learning mode until May 28 |
| All plugins | ✅ Up to date | No updates needed |
| All themes | ✅ Up to date | No updates needed |
| Wordfence free license | ⚠️ Manual step | WP Admin → Wordfence → Help → Resume Installation → enter sandipc@gmail.com |
| Hide WordPress version | ⚠️ Manual step | AIOSEO → General Settings → Advanced → uncheck "Output Generator Tag" |
| Google Analytics GA4 | ⚠️ Manual step | MonsterInsights active — needs GA4 Measurement ID |
| Google Search Console | ⚠️ Not done | Submit sitemap after GA connected |

---

## Security Status

✅ **Wordfence active** — brute force protection running on /wp-login.php  
⚠️ **WordPress 7.0 version tag visible** — fix manually via AIOSEO → General Settings → Advanced

---

## GitHub Repository

**Repo:** https://github.com/sdc2018/money-and-mode  
**Status:** ✅ Live  
**Branch:** main  

---

## Open Actions

- [ ] Publish 3 written articles to WordPress (ready in /articles/)
- [ ] Complete Wordfence license (enter sandipc@gmail.com on wordfence.com)
- [ ] Hide WP version: AIOSEO → General Settings → Advanced → uncheck generator tag
- [ ] Connect MonsterInsights to GA4 Measurement ID
- [ ] Submit sitemap to Google Search Console
- [ ] Add meta descriptions to existing pages via AIOSEO
- [ ] Write next batch of articles (ChatGPT explained, Free AI tools, Talk to AI)
- [ ] Get Sandip's financial freedom initial thoughts → write series
- [ ] Create Phase 3 social media handles (Pinterest first)
- [ ] Apply for Google AdSense when traffic hits 5,000/month

---

*Auto-generated and maintained by Claude | money-and-mode project*
