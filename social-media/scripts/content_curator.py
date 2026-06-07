#!/usr/bin/env python3
"""
Content Curator for money-and-mode.com
Fetches RSS feeds from sources.json, scores articles by relevance,
and generates weekly digest drafts for Sandip to review and publish.

Usage:
  python content_curator.py --fetch        # Fetch all feeds, score, save top picks
  python content_curator.py --draft        # Generate WordPress post draft from this week's picks
  python content_curator.py --show         # Print this week's top picks to terminal
  python content_curator.py --fetch --draft  # Do both in one step
"""

import feedparser
import json
import os
import sys
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import time

# ─── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent.parent
SOURCES     = BASE_DIR / "marketing" / "sources.json"
DIGESTS_DIR = BASE_DIR / "social-media" / "digests"
SEEN_FILE   = DIGESTS_DIR / "seen_urls.json"
DIGESTS_DIR.mkdir(parents=True, exist_ok=True)

# ─── Config ────────────────────────────────────────────────────────────────────
MAX_AGE_DAYS   = 7       # Only include articles from last 7 days
TOP_PER_TOPIC  = 3       # How many articles per topic in the digest
MIN_SCORE      = 1.0     # Minimum relevance score to include


# ─── Scoring ───────────────────────────────────────────────────────────────────
def score_article(entry, keywords, authority):
    """Score an article by keyword relevance × authority × recency."""
    text = (
        (entry.get("title") or "") + " " +
        (entry.get("summary") or "") + " " +
        " ".join(t.get("term", "") for t in entry.get("tags", []))
    ).lower()

    # Keyword match score
    keyword_hits = sum(1 for kw in keywords if kw.lower() in text)
    if keyword_hits == 0:
        return 0.0

    # Recency score (1.0 = today, 0.1 = 7 days ago)
    recency = 1.0
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if published:
        try:
            age_days = (datetime.now() - datetime(*published[:6])).days
            recency = max(0.1, 1.0 - (age_days / MAX_AGE_DAYS))
        except Exception:
            recency = 0.5

    return round(keyword_hits * authority * recency, 2)


def is_recent(entry, max_days=MAX_AGE_DAYS):
    """Return True if the article was published within max_days."""
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True  # Can't tell — include it
    try:
        age = (datetime.now() - datetime(*published[:6])).days
        return age <= max_days
    except Exception:
        return True


def get_url(entry):
    return entry.get("link") or entry.get("id") or ""


def get_published(entry):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if published:
        try:
            return datetime(*published[:6]).strftime("%Y-%m-%d")
        except Exception:
            pass
    return datetime.now().strftime("%Y-%m-%d")


# ─── Load / Save seen URLs ──────────────────────────────────────────────────────
def load_seen():
    if SEEN_FILE.exists():
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f, indent=2)


# ─── Fetch all feeds ────────────────────────────────────────────────────────────
def fetch_all(sources_data, seen_urls):
    results = {}  # topic -> list of scored articles

    for topic, topic_data in sources_data["topics"].items():
        keywords  = topic_data["keywords"]
        articles  = []

        all_sources = topic_data.get("sources", []) + topic_data.get("youtube_channels", [])

        for source in all_sources:
            rss_url   = source.get("rss")
            authority = source.get("authority", 3)
            name      = source.get("name", rss_url)

            if not rss_url:
                continue

            print(f"  Fetching: {name} ...", end=" ", flush=True)
            try:
                feed = feedparser.parse(rss_url)
                count = 0
                for entry in feed.entries[:20]:  # Check top 20 entries
                    url = get_url(entry)
                    if not url or url in seen_urls:
                        continue
                    if not is_recent(entry):
                        continue
                    score = score_article(entry, keywords, authority)
                    if score >= MIN_SCORE:
                        articles.append({
                            "title":     entry.get("title", "").strip(),
                            "url":       url,
                            "source":    name,
                            "summary":   re.sub(r"<[^>]+>", "", entry.get("summary", ""))[:300].strip(),
                            "published": get_published(entry),
                            "score":     score,
                            "topic":     topic,
                            "type":      "youtube" if "youtube.com" in rss_url else "article"
                        })
                        count += 1
                print(f"{count} relevant articles")
                time.sleep(0.5)  # Be polite to servers
            except Exception as e:
                print(f"ERROR: {e}")

        # Sort by score descending
        articles.sort(key=lambda x: x["score"], reverse=True)
        results[topic] = articles

    return results


# ─── Generate digest markdown ───────────────────────────────────────────────────
def generate_digest(results, week_label):
    """Generate a WordPress-ready markdown draft of the weekly digest."""

    topic_display = {
        "ai_technology":    ("🤖 AI & Technology", "ai-technology"),
        "financial_freedom": ("💰 Financial Freedom", "financial-freedom"),
        "life_motivation":   ("🌱 Life & Personal Growth", "life-motivation"),
    }

    total_picks = sum(len(v[:TOP_PER_TOPIC]) for v in results.values())

    lines = []
    lines.append(f"# Weekly Digest — {week_label}")
    lines.append(f"**What's worth your time this week: AI, Money & Life.**")
    lines.append(f"*Curated by Kabir Shah — {total_picks} picks across 3 topics. Saving you hours of scrolling.*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Every week I go through dozens of articles, videos, and posts across AI, personal finance, and everyday life.")
    lines.append("These are the ones worth your time. I add a short note on why I picked each one.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for topic, (display_name, slug) in topic_display.items():
        picks = results.get(topic, [])[:TOP_PER_TOPIC]
        if not picks:
            continue

        lines.append(f"## {display_name}")
        lines.append("")

        for i, article in enumerate(picks, 1):
            content_type = "📹 Video" if article["type"] == "youtube" else "📄 Article"
            lines.append(f"### {i}. [{article['title']}]({article['url']})")
            lines.append(f"**Source:** {article['source']} | {content_type} | {article['published']}")
            lines.append("")

            # Placeholder for Kabir's take — Claude fills this in during the monthly task
            lines.append(f"> **Kabir's take:** *[Add 2-sentence commentary here — why does this matter for our readers?]*")
            lines.append("")

            if article["summary"]:
                lines.append(f"{article['summary'][:200]}...")
                lines.append("")

            lines.append(f"[Read / Watch →]({article['url']})")
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("## Why I Curate This")
    lines.append("")
    lines.append("The internet has too much content. Most of it isn't worth your time.")
    lines.append("Every week I read across AI, money, and life so you don't have to.")
    lines.append("These are the pieces that made me think, taught me something, or changed how I see something.")
    lines.append("")
    lines.append("If something here was useful, share it with one person who'd benefit.")
    lines.append("")
    lines.append("*→ Want this in your inbox every week? Subscribe below.*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Tags:** weekly-digest, AI, financial-freedom, personal-growth, curated")

    return "\n".join(lines)


def generate_social_posts(results, week_label):
    """Generate social media posts promoting the digest."""
    picks_flat = []
    for topic, articles in results.items():
        picks_flat.extend(articles[:1])  # Top pick per topic

    ig_caption = f"""This week in AI, Money & Life — the 3 things worth your time 🗞️

"""
    for p in picks_flat[:3]:
        ig_caption += f"→ {p['title'][:60]}{'...' if len(p['title']) > 60 else ''}\n   ({p['source']})\n\n"

    ig_caption += "Full digest with links at money-and-mode.com → Link in bio\n\n"
    ig_caption += "💾 Save this post — your weekly reading list is ready.\n\n"
    ig_caption += "#WeeklyDigest #AI #FinancialFreedom #PersonalGrowth #ContentCuration"

    tweet = f"This week's reading list — AI, money & life:\n\n"
    for p in picks_flat[:3]:
        tweet += f"📌 {p['title'][:50]}\n"
    tweet += f"\nFull digest → money-and-mode.com\n#AI #FinancialFreedom #WeeklyReads"

    fb_post = f"""Every week I go through dozens of articles so you don't have to.

Here's what's worth your time this week:

"""
    for p in picks_flat:
        fb_post += f"✅ {p['title']}\n   → {p['url']}\n\n"

    fb_post += "Full digest with commentary: money-and-mode.com\n\n"
    fb_post += "What's the most interesting thing you read this week? Drop it below 👇\n\n"
    fb_post += "#WeeklyDigest #AI #PersonalFinance #PersonalGrowth"

    return {
        "instagram": ig_caption,
        "twitter":   tweet,
        "facebook":  fb_post
    }


# ─── Main ───────────────────────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    do_fetch = "--fetch" in args
    do_draft = "--draft" in args
    do_show  = "--show"  in args or (not args)

    week_label = datetime.now().strftime("Week of %B %d, %Y")
    week_slug  = datetime.now().strftime("%Y-W%V")
    digest_file = DIGESTS_DIR / f"digest-{week_slug}.json"
    draft_file  = DIGESTS_DIR / f"draft-{week_slug}.md"

    # ── FETCH ──────────────────────────────────────────────────────────────────
    if do_fetch:
        print(f"\n📡 Fetching RSS feeds — {week_label}")
        print("=" * 60)

        if not SOURCES.exists():
            print(f"ERROR: {SOURCES} not found")
            sys.exit(1)

        with open(SOURCES) as f:
            sources_data = json.load(f)

        seen_urls = load_seen()
        print(f"Already seen: {len(seen_urls)} URLs\n")

        results = fetch_all(sources_data, seen_urls)

        # Mark fetched URLs as seen
        for topic_articles in results.values():
            for a in topic_articles:
                seen_urls.add(a["url"])
        save_seen(seen_urls)

        # Summary
        print(f"\n✅ Fetch complete:")
        total = 0
        for topic, articles in results.items():
            top = articles[:TOP_PER_TOPIC]
            print(f"  {topic}: {len(articles)} found, top {len(top)} selected")
            total += len(top)
        print(f"  Total digest picks: {total}")

        # Save results
        with open(digest_file, "w") as f:
            json.dump({"week": week_slug, "label": week_label, "results": results}, f, indent=2)
        print(f"\n💾 Saved to: {digest_file}")

    # ── DRAFT ──────────────────────────────────────────────────────────────────
    if do_draft:
        if not digest_file.exists():
            print("No digest data found. Run --fetch first.")
            sys.exit(1)

        with open(digest_file) as f:
            data = json.load(f)

        results = data["results"]

        # Generate WordPress draft
        draft = generate_digest(results, week_label)
        with open(draft_file, "w") as f:
            f.write(draft)
        print(f"\n📝 WordPress draft saved: {draft_file}")

        # Generate social posts
        social = generate_social_posts(results, week_label)
        social_file = DIGESTS_DIR / f"social-{week_slug}.json"
        with open(social_file, "w") as f:
            json.dump(social, f, indent=2)
        print(f"📱 Social posts saved: {social_file}")

    # ── SHOW ───────────────────────────────────────────────────────────────────
    if do_show or (not do_fetch and not do_draft):
        if not digest_file.exists():
            print("No digest found for this week. Run: python content_curator.py --fetch")
            sys.exit(0)

        with open(digest_file) as f:
            data = json.load(f)

        print(f"\n📰 {data['label']} — Top Picks")
        print("=" * 60)
        for topic, articles in data["results"].items():
            print(f"\n{topic.upper()}")
            for a in articles[:TOP_PER_TOPIC]:
                print(f"  [{a['score']:.1f}] {a['title'][:70]}")
                print(f"       {a['source']} | {a['published']}")
                print(f"       {a['url'][:80]}")

    print("\nDone ✅")


if __name__ == "__main__":
    main()
