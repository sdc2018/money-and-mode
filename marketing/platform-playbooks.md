# Platform Playbooks — All Active Channels
## money-and-mode.com | Fun in the Life

Every article published triggers posts across all 4 platforms.
One article = 4 posts + 3 Pinterest pins + 1 tweet thread.

---

## The Master Workflow (Per Article)

```
PUBLISH ARTICLE
      ↓
Pinterest  →  3 pin variations (pinterest_growth.py)
Instagram  →  1 post (diagram + save-worthy caption)
X/Twitter  →  1 tweet + optional 3-tweet thread
Facebook   →  1 post (story format + link)
      ↓
TRACK in performance-log.json
```

---

## PLATFORM 1: Pinterest (@sandip2787)
**Role: Traffic engine. Pins live for years, not hours.**

### Why Pinterest Matters More Than You Think
Pinterest has 500M+ monthly users actively searching for content.
Unlike Instagram (followers see posts), Pinterest works like Google — anyone searching "AI tools for beginners" can find your pin even if they've never heard of you.
One well-optimised pin = traffic for 2–3 years.

### Current Setup
- ✅ Account: @sandip2787
- ✅ 3 boards: "AI Tips & Tools" / "Money & Financial Freedom" / "Life, Growth & Daily Habits"
- ✅ Script: pinterest_growth.py (posts 3 variations per article)

### Playbook Per Article
1. Run `python social-media/scripts/pinterest_growth.py --article [ID]`
2. This creates 3 pins with different titles/descriptions on the right board
3. Done — no manual work needed once API token is set up

### Monthly Pinterest Actions
- Create 3 new pin variations for any article older than 30 days (re-pins drive fresh traffic)
- Check Pinterest Analytics: which boards/pins drive most clicks → write more on those topics
- Follow 10 accounts in your niche (AI/finance/life) — Pinterest reciprocates reach

### Pin Optimisation Rules
- Title: keyword first, max 100 chars ("5 Free AI Tools That Save 2 Hours Every Day")
- Description: 2–3 sentences with keyword + "money-and-mode.com" + 5 hashtags
- Image: tall format (2:3 ratio) — already using portrait diagrams ✅
- Board: match article topic exactly — wrong board = less reach

### Hashtags for Pinterest (use 5 per pin)
AI content: #AITools #ChatGPT #AIForBeginners #ArtificialIntelligence #TechTips
Finance: #FinancialFreedom #FIRE #PersonalFinance #MoneyTips #FinancialIndependence
Life: #PersonalGrowth #FamilyLife #MindfulLiving #LifeTips #SelfImprovement

---

## PLATFORM 2: X / Twitter (@justIndia25)
**Role: Conversation + authority building. India tech/finance audience.**

### Why X Works for This Blog
Twitter/X has a large India tech audience — exactly our readers.
The play isn't broadcasting. It's being IN the conversation.
Reply to big accounts → their followers see you → profile clicks → blog traffic.

### Current Setup
- ✅ Account: @justIndia25
- ✅ Script: twitter_growth.py (finds conversations to join)
- ⚠️ Posting via API needs paid plan — manual posting is fine

### Playbook Per Article
**Tweet format (for article launch):**
```
[Hook — 1 punchy sentence]

[3 key points from the article as bullet lines]

[Link to article]

#Hashtag1 #Hashtag2 #Hashtag3
```

**Example:**
```
Most people think AI is coming in the future.

It arrived years ago — quietly, in everything you already use:

• Netflix recs → AI
• Bank fraud alerts → AI
• Google Maps rerouting → AI
• Face unlock → AI

8 places AI is already in your life 👇
money-and-mode.com/how-ai-is-changing-everyday-life/

#AI #ArtificialIntelligence #TechForEveryone
```

### Thread Format (for deeper articles)
Use for Financial Freedom articles — these get bookmarked and shared.
```
Tweet 1: Hook + "🧵 thread"
Tweet 2: Point 1
Tweet 3: Point 2
Tweet 4: Point 3
Tweet 5: Key insight
Tweet 6: "Full article here: [link] — save this thread if it helped"
```

### The Conversation Strategy (Highest Leverage)
Run `python twitter_growth.py --find` every morning.
Find tweets with 500+ likes in AI/finance/India niche.
Reply within the first hour with: genuine insight + experience angle + optional question.

**Reply formula:**
```
[Agree or add nuance — don't just say "great point"]
[Add something from your 25 years in software/AI]
[Optional: "I wrote about this exact thing — [title] if you want to go deeper"]
```

One reply on a viral tweet = 50–500 new profile visits in a day.

### X Hashtags Per Topic
AI: #AI #ChatGPT #ArtificialIntelligence #AITools #TechIndia
Finance: #FinancialFreedom #FIRE #PersonalFinance #MoneyTips #IndiaFinance  
Life: #PersonalGrowth #MindsetShift #Productivity

### Monthly X Actions
- 1 article tweet per published post
- 1 thread per Financial Freedom article (higher engagement)
- Daily: check twitter_growth.py output, reply to 2–3 conversations
- Follow back relevant accounts in AI/finance niche

---

## PLATFORM 3: Facebook (Page to be created)
**Role: India's biggest platform. Massive reach for 35+ audience.**

### Why Facebook Is Critical for This Blog
Facebook has 360M+ users in India — largest user base of any platform.
The 35–55 age group (our primary reader) is MORE active on Facebook than Instagram.
Facebook groups are gold — millions of people in "Personal Finance India", "AI Tools India" groups.

### Setup Steps (One-time, ~30 minutes)
1. Go to facebook.com/pages/create
2. Page name: **Fun in the Life**
3. Category: **Blog** or **Personal Blog**
4. Username: @funintheli71 (match Instagram handle)
5. Description: "AI · Money · Life. Simple ideas for a better everyday. By Kabir Shah."
6. Website: money-and-mode.com
7. Profile photo: same as Instagram
8. Cover photo: blog banner
9. **Connect to Instagram** (Settings → Instagram → Connect) → enables cross-posting

### Playbook Per Article
**Facebook post format (different from Instagram — longer text works here):**
```
[1-sentence hook]

[3–4 paragraph story or insight from the article]
(Facebook rewards longer posts — 150–300 words work well)

[Key takeaway as a numbered list]

[Link to article]

[Question to drive comments]

[3–5 hashtags — Facebook uses fewer than Instagram]
```

**Example (for AI Everyday Life article):**
```
You've been using AI for years. You just didn't know it was called that.

When Netflix suggested a show that turned out perfect — that was AI.
When Google Maps quietly rerouted you around an accident — AI.
When your bank sent a fraud alert before you noticed anything wrong — AI.

None of these happened by accident. They happened because companies quietly added machine learning to tools you were already using.

I put together a breakdown of 8 everyday places AI is already working for you — written for people who aren't tech-savvy. No jargon. Just plain explanations.

The one that surprises most people: your doctor's diagnosis is increasingly assisted by AI. And honestly? That might be a good thing.

Full article: money-and-mode.com/how-ai-is-changing-everyday-life/

Which one surprised you most? 👇

#AI #Technology #EverydayLife
```

### Facebook Groups Strategy (Big Traffic Opportunity)
Join these groups and share value — not spam:

| Group type | What to search on Facebook | When to post |
|-----------|--------------------------|-------------|
| AI India groups | "Artificial Intelligence India", "AI Tools India" | When publishing AI articles |
| Personal Finance India | "Personal Finance India", "FIRE India" | When publishing finance articles |
| Entrepreneurs India | "Entrepreneurs India", "Startup India" | Financial freedom articles |
| Working professionals | "Tech professionals India" | AI productivity articles |

**Group posting rule:** Add value in 5 comments before posting your own link. Build presence first.

### Facebook Ads (Future — Month 6+)
Once organic reach is established:
- Boost top-performing posts: ₹200–500/day
- Target: India, 30–55, interests: AI/technology, personal finance, self-improvement
- Goal: website traffic → AdSense revenue increase

### Monthly Facebook Actions
- Share every new article (2/week)
- 3 group posts per week (in relevant groups)
- Reply to every comment within 24 hours
- Check Facebook Insights: which post got most link clicks? Write more on that topic.

---

## FULL CROSS-PLATFORM CALENDAR (Per Week)

| Day | Platform | Action |
|-----|----------|--------|
| Tuesday | WordPress | Publish article |
| Tuesday | Pinterest | Run pinterest_growth.py --article [ID] |
| Tuesday | Instagram | Post diagram + save-worthy caption |
| Tuesday | X/Twitter | Article tweet (hook + 3 points + link) |
| Tuesday | Facebook | Article post (story format, longer) |
| Wednesday | X/Twitter | Morning: twitter_growth.py --find → reply to 2 conversations |
| Wednesday | Facebook | Share in 1 relevant group |
| Thursday | Quora | Write 1 answer linking to Tuesday's article |
| Friday | WordPress | Publish second article |
| Friday | Pinterest | Run pinterest_growth.py --article [ID] |
| Friday | Instagram | Post diagram + caption |
| Friday | X/Twitter | Article tweet or thread |
| Friday | Facebook | Article post |
| Saturday | X/Twitter | Morning: twitter_growth.py → reply to 2 conversations |
| Saturday | Facebook | Share in 1 relevant group |
| Sunday | Quora | Write 1 answer (for Friday article) |

**Total per week:** 2 articles, 6 social posts (2 IG + 2 X + 2 FB), 6 Pinterest pins, 2 Quora answers.

---

## Captions — Platform Differences

Same article, different angles for each platform:

| Platform | Tone | Length | Format | CTA |
|----------|------|--------|--------|-----|
| Instagram | Visual, punchy | 150–300 words | Lists, before/after | "Save this 💾" |
| X/Twitter | Sharp, opinionated | 280 chars (or thread) | Hook + points + link | "RT if useful" |
| Facebook | Conversational, warm | 200–400 words | Story → insight → list | "Share with someone" |
| Pinterest | Keyword-rich, helpful | 100–150 words | Keyword + benefits | "Full article at money-and-mode.com" |

---

## Performance Tracking — All Platforms

Add to performance-log.json after each post (7 days later):

| Platform | Metrics to track |
|----------|-----------------|
| Instagram | Saves, comments, reach, likes |
| X/Twitter | Impressions, link clicks, retweets, replies |
| Facebook | Reach, link clicks, comments, shares |
| Pinterest | Impressions, clicks, saves (outbound clicks = gold) |

**Monthly review:** Claude reads all metrics → finds which platform sends most blog traffic → doubles down on that channel next month.

---

*All captions for the week ahead are pre-written in the monthly plan. Claude generates them. Sandip posts them.*
*Last updated: June 2026*
