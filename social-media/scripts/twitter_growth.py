"""
Twitter/X Growth Automation — money-and-mode.com
=================================================
Finds high-value conversations to join — the #1 growth lever on Twitter.

A sharp reply on a tweet with 50K likes → 50-200 new followers.
Posting into the void → nothing.

This script finds the RIGHT conversations and drafts replies in Kabir Shah's voice.

Setup:
  pip install requests python-dotenv
  Add TWITTER_BEARER_TOKEN to .env

Usage:
  python twitter_growth.py --find              # Find conversations to join now
  python twitter_growth.py --find --topic ai   # Filter by topic
  python twitter_growth.py --post-threads      # Post all pending threads from queue.json
"""

import os
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
QUEUE_FILE = ROOT / "social-media" / "queue.json"

load_dotenv(ENV_FILE)

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

SEARCH_BASE = "https://api.twitter.com/2/tweets/search/recent"
POST_BASE = "https://api.twitter.com/2/tweets"

BEARER_HEADERS = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}

# ── Target accounts to monitor (high-follower, relevant niche) ────────────────
# When these accounts tweet, reply within the first hour for max visibility
TARGET_ACCOUNTS = [
    "naval",           # Naval Ravikant — philosophy, wealth
    "SahilBloom",      # Sahil Bloom — finance, growth
    "morganhousel",    # Morgan Housel — money, investing
    "JamesClear",      # James Clear — habits
    "GaryVee",         # Gary Vaynerchuk — entrepreneurship
    "elonmusk",        # Elon Musk — AI, tech
    "sama",            # Sam Altman — AI
    "paulg",           # Paul Graham — startups
    "balajis",         # Balaji — tech, India
    "shreyas",         # Shreyas Doshi — product, startups
]

# ── Search queries by topic ───────────────────────────────────────────────────
SEARCH_QUERIES = {
    "ai": [
        "AI everyday life -is:retweet lang:en min_faves:100",
        "artificial intelligence simple explanation -is:retweet lang:en min_faves:50",
        "AI tools productivity -is:retweet lang:en min_faves:100",
        "ChatGPT save time -is:retweet lang:en min_faves:50",
    ],
    "finance": [
        "financial freedom time -is:retweet lang:en min_faves:100",
        "passive income truth -is:retweet lang:en min_faves:50",
        "selling your time employment -is:retweet lang:en min_faves:100",
        "FIRE movement -is:retweet lang:en min_faves:100",
        "financial independence India -is:retweet lang:en min_faves:20",
    ],
    "life": [
        "family connection meaning -is:retweet lang:en min_faves:100",
        "work life balance truth -is:retweet lang:en min_faves:100",
        "morning routine habits -is:retweet lang:en min_faves:50",
    ],
    "entrepreneurship": [
        "sold my company -is:retweet lang:en min_faves:50",
        "startup exit founder -is:retweet lang:en min_faves:100",
        "entrepreneur India tech -is:retweet lang:en min_faves:20",
    ],
}

# ── Reply templates (fill with specific insight) ──────────────────────────────
# Kabir Shah voice: wise, direct, from experience — never salesy
REPLY_TEMPLATES = {
    "ai_everyday": [
        "This is what I keep telling people — AI isn't coming, it's already here. Your Netflix queue, Google Maps rerouting, your bank's fraud alert. All AI. Most people just haven't noticed yet.",
        "25 years in tech and this is the most common misconception I see. People think AI is future tense. It's present tense — and has been for years.",
        "The gap between 'AI is coming' and 'AI is here' is the single most important thing for people to close. Once they do, everything changes.",
    ],
    "financial_freedom": [
        "Financial freedom isn't a number. It's a calendar. The question isn't 'how much?' — it's 'who owns your time today?'",
        "I sold my company at 31. Within a week I was looking for what to do next. The money landed — but freedom took another year to understand.",
        "The trap isn't employment. It's selling your time. Employees do it. Freelancers do it too. The exit is income that doesn't need your presence.",
    ],
    "general_wisdom": [
        "The biggest shifts happen quietly. Not with a bang, but with a slight change in what you're optimising for.",
        "25+ years in the software business: the people who adapt consistently beat the people who resist consistently. Every time.",
        "Worth noting for India specifically — we're at the perfect inflection point. Early enough to build, late enough to learn from others' mistakes.",
    ],
}


# ── API helpers ────────────────────────────────────────────────────────────────

def search_tweets(query: str, max_results: int = 10) -> list:
    """Search recent tweets matching a query."""
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "public_metrics,author_id,created_at,text",
        "expansions": "author_id",
        "user.fields": "username,public_metrics,name",
    }
    resp = requests.get(SEARCH_BASE, headers=BEARER_HEADERS, params=params)
    if resp.status_code == 429:
        print("  ⚠️  Rate limit hit. Twitter free tier allows 1 search/15min.")
        return []
    resp.raise_for_status()
    data = resp.json()

    tweets = data.get("data", [])
    users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}

    results = []
    for t in tweets:
        author = users.get(t["author_id"], {})
        results.append({
            "id": t["id"],
            "text": t["text"],
            "author": author.get("username", "unknown"),
            "author_followers": author.get("public_metrics", {}).get("followers_count", 0),
            "likes": t.get("public_metrics", {}).get("like_count", 0),
            "retweets": t.get("public_metrics", {}).get("retweet_count", 0),
            "created_at": t.get("created_at", ""),
            "url": f"https://twitter.com/{author.get('username')}/status/{t['id']}",
        })

    # Sort by engagement
    results.sort(key=lambda x: x["likes"] + x["retweets"] * 3, reverse=True)
    return results


def post_tweet(text: str, reply_to_id: str = None) -> dict:
    """Post a tweet (requires OAuth 1.0a — needs additional auth setup)."""
    # Note: Posting requires OAuth 1.0a with user credentials
    # This is read-only for now unless full OAuth is configured
    import hmac
    import hashlib
    import base64
    import time
    import uuid
    from urllib.parse import quote

    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("❌ Full OAuth credentials needed to post. See SETUP.md")
        return {}

    payload = {"text": text}
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

    # OAuth 1.0a signature (simplified — use tweepy in production)
    print(f"📤 Would post: {text[:80]}...")
    print("   (Full OAuth posting — use tweepy library for production)")
    return {"status": "draft"}


def load_pending_threads() -> list:
    """Load pending Twitter threads from queue.json."""
    with open(QUEUE_FILE) as f:
        queue = json.load(f)
    return [t for t in queue.get("threads_pending", []) if t.get("status") == "pending"]


def display_engagement_opportunities(tweets: list, topic: str):
    """Display tweets worth replying to, with suggested reply angles."""
    if not tweets:
        print("  No tweets found matching this criteria.")
        return

    print(f"\n{'='*70}")
    print(f"  🎯 Top opportunities in: {topic.upper()}")
    print(f"{'='*70}\n")

    for i, t in enumerate(tweets[:5], 1):
        print(f"  [{i}] @{t['author']} ({t['author_followers']:,} followers)")
        print(f"      ❤️  {t['likes']:,}  🔁 {t['retweets']:,}")
        print(f"      📝 {t['text'][:120]}{'...' if len(t['text']) > 120 else ''}")
        print(f"      🔗 {t['url']}")
        print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Twitter Growth Automation")
    parser.add_argument("--find", action="store_true", help="Find conversations to join")
    parser.add_argument("--topic", choices=list(SEARCH_QUERIES.keys()), help="Filter by topic")
    parser.add_argument("--post-threads", action="store_true", help="Show pending threads from queue.json")
    parser.add_argument("--targets", action="store_true", help="Show tweets from target accounts")
    args = parser.parse_args()

    if not TWITTER_BEARER_TOKEN:
        print("❌ TWITTER_BEARER_TOKEN not set in .env")
        print("   See social-media/scripts/SETUP.md for instructions")
        return

    if args.post_threads:
        print("\n📋 Pending Twitter Threads:\n")
        threads = load_pending_threads()
        if not threads:
            print("  No pending threads found in queue.json")
            return
        for thread in threads:
            print(f"  Thread: {thread['id']} (Article {thread['article_id']})")
            for i, tweet in enumerate(thread["tweets"], 1):
                print(f"    Tweet {i}: {tweet[:80]}...")
            print()
        return

    if args.find:
        topics = [args.topic] if args.topic else list(SEARCH_QUERIES.keys())

        print("\n🔍 Finding high-value conversations to join...\n")
        print("📌 STRATEGY: Reply to tweets with 100+ likes in your first hour.")
        print("   One great reply on a viral tweet can bring 50-200 followers.\n")

        for topic in topics:
            queries = SEARCH_QUERIES[topic]
            # Use first query per topic (free tier rate limits)
            print(f"\n🏷️  Topic: {topic}")
            try:
                tweets = search_tweets(queries[0], max_results=10)
                display_engagement_opportunities(tweets, topic)
            except Exception as e:
                print(f"  Error: {e}")

        print("\n💡 REPLY ANGLES (Kabir Shah voice):")
        print("   • Agree + add a layer from your 25yr experience")
        print("   • Share a surprising counterpoint (gets more replies)")
        print("   • '25 years in tech/India specific angle' hooks work well")
        print("   • End with a question to invite conversation")
        print("\n🎯 ACCOUNTS TO MONITOR DAILY:")
        for acc in TARGET_ACCOUNTS[:5]:
            print(f"   @{acc} — reply within 1hr of their tweets")

    if args.targets:
        print("\n👥 Target accounts to monitor:")
        for acc in TARGET_ACCOUNTS:
            print(f"  https://twitter.com/{acc}")
        print("\n⚡ Tip: Add these to a Twitter List for fast morning monitoring.")

    if not any([args.find, args.post_threads, args.targets]):
        parser.print_help()


if __name__ == "__main__":
    main()
