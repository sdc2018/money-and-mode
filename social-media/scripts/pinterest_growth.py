"""
Pinterest Growth Automation — money-and-mode.com
================================================
Creates multiple pin variations per article to maximise reach.
Pinterest rewards FRESH PINS — same URL, different image/copy = more distribution.

Setup:
  pip install requests python-dotenv
  Add credentials to .env (see .env.example)

Usage:
  python pinterest_growth.py --article 74          # Pin all variations for article 74
  python pinterest_growth.py --all-pending          # Pin everything in queue.json
  python pinterest_growth.py --boards               # List your board IDs
"""

import os
import json
import time
import argparse
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / ".env"
QUEUE_FILE = ROOT / "social-media" / "queue.json"

load_dotenv(ENV_FILE)

PINTEREST_ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
BASE_URL = "https://api.pinterest.com/v5"
HEADERS = {
    "Authorization": f"Bearer {PINTEREST_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

# ── Article database ─────────────────────────────────────────────────────────
# For each article: 3 pin variations (title + description angle)
# Same image, different hook — Pinterest treats these as fresh pins
ARTICLE_PINS = {
    74: {
        "url": "https://money-and-mode.com/how-ai-is-changing-everyday-life/",
        "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-ai-everyday-life.png",
        "board": "AI Tips & Tools",
        "variations": [
            {
                "title": "How AI Is Changing Everyday Life — 8 Ways Already Happening",
                "description": "Most people think AI is coming in the future. It's not. It's already here — in your phone, your maps, your TV, your doctor's office. 8 areas where AI is already at work. No jargon. No hype. Full article at money-and-mode.com\n\n#ArtificialIntelligence #AIEverydayLife #TechForBeginners #AIExplained",
            },
            {
                "title": "You're Already Using AI — You Just Don't Know It Yet",
                "description": "Your Netflix recommendations. Google Maps rerouting you. Your bank's fraud alert. That's all AI — running quietly in the background of your life right now. Here's the full picture. money-and-mode.com\n\n#AIInYourLife #TechSimplified #ArtificialIntelligence #FutureOfTech",
            },
            {
                "title": "AI for Beginners — Where It's Already Running in Your Life",
                "description": "8 areas of daily life where AI is already working for you. Healthcare, finance, entertainment, travel — no jargon, no hype. Just a clear look at what's already happening. Full guide at money-and-mode.com\n\n#AIForBeginners #TechExplained #AIEverydayLife #DigitalLife",
            },
        ],
    },
    76: {
        "url": "https://money-and-mode.com/how-to-use-ai-to-save-2-hours-every-day/",
        "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-ai-save-2-hours.png",
        "board": "AI Tips & Tools",
        "variations": [
            {
                "title": "How to Use AI to Save 2 Hours Every Day — Practical Guide",
                "description": "Two hours back every day — that's what AI gives you if you use it right. Email drafts: 30 min → 5 min. Research: 90 min → 20 min. No tech skills needed. Free tools. Full guide at money-and-mode.com\n\n#SaveTimeWithAI #AIProductivity #ChatGPT #WorkSmarter",
            },
            {
                "title": "AI Productivity Hacks — Get 2 Hours Back Every Day",
                "description": "The bar chart doesn't lie. Before AI vs. after AI across 4 key tasks — the time saved is significant. Emails, research, drafts, scheduling. All faster. All free to start. money-and-mode.com\n\n#AIProductivity #ProductivityHacks #AITools #TimeManagement",
            },
            {
                "title": "ChatGPT for Time Management — A Real Before & After",
                "description": "30 minutes on email. Down to 5 with AI. 90-minute research sessions. Down to 20. This is what AI actually saves you — with real numbers. Full breakdown at money-and-mode.com\n\n#ChatGPT #AIForWork #SaveTime #HowToUseAI",
            },
        ],
    },
    77: {
        "url": "https://money-and-mode.com/will-ai-take-my-job-heres-the-honest-answer-nobody-is-giving-you/",
        "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-will-ai-take-job.png",
        "board": "AI Tips & Tools",
        "variations": [
            {
                "title": "Will AI Take My Job? The Calm, Honest Answer",
                "description": "The jobs most at risk: repetitive, rule-based work. The jobs safest: human judgment, empathy, creativity. No doom, no false comfort — just the honest breakdown. Full article at money-and-mode.com\n\n#WillAITakeMyJob #FutureOfWork #AIAndJobs #CareerAdvice",
            },
            {
                "title": "Jobs AI Will Replace vs. Jobs That Are Safe — The Real List",
                "description": "Data entry, basic customer service, standard reporting — at risk. Judgment, empathy, leadership, creativity — safer. The dividing line is clear. Are you on the right side? money-and-mode.com\n\n#AIJobs #FutureOfWork #JobSecurity #AIImpact",
            },
            {
                "title": "How to Future-Proof Your Career in the Age of AI",
                "description": "The people at greatest risk are those who refuse to adapt. The people who thrive will use AI as a tool, not fear it as a threat. Here's how to be in the second group. money-and-mode.com\n\n#CareerAdvice #AIEra #FutureProof #WorkInAIEra",
            },
        ],
    },
    110: {
        "url": "https://money-and-mode.com/i-sold-my-company-at-31-financial-freedom/",
        "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-sold-company-31.png",
        "board": "Money & Financial Freedom",
        "variations": [
            {
                "title": "I Sold My Company at 31 — What Financial Freedom Actually Felt Like",
                "description": "Financial freedom isn't a number in a bank account. It's a calendar. I sold my company at 31 and learned the hard way what freedom really means. Full honest account at money-and-mode.com\n\n#FinancialFreedom #FIRE #FinancialIndependence #TimeOwnership",
            },
            {
                "title": "Financial Freedom Is a Calendar — Not a Number",
                "description": "The question isn't 'how much money?' It's 'who owns your time today?' I built a company, sold it at 31, and it took a full year to understand the answer. money-and-mode.com\n\n#FinancialFreedom #WealthMindset #FIRE #PersonalFinance",
            },
            {
                "title": "4 Phases From Build → Exit → Build Free → Own Time",
                "description": "Phase 4 is the one that actually matters. Most people never reach it — not because they run out of money, but because they never ask the right question. money-and-mode.com\n\n#FinancialIndependence #ExitStrategy #WealthBuilding #MoneyAndLife",
            },
        ],
    },
    112: {
        "url": "https://money-and-mode.com/selling-your-time-financial-freedom-time-ownership/",
        "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-selling-your-time.png",
        "board": "Money & Financial Freedom",
        "variations": [
            {
                "title": "If You Are Selling Your Time, You Will Never Be Free",
                "description": "When you sell your time, the income stops when you stop. That's not a career — it's a treadmill. The before/after calendar shows it clearly. Full article at money-and-mode.com\n\n#SellingYourTime #FinancialFreedom #PassiveIncome #TimeOwnership",
            },
            {
                "title": "The Calendar That Changes Everything — Two Versions of Your Life",
                "description": "One calendar full of other people's priorities. One calendar you control completely. The path between them is specific — and it's not about earning more. money-and-mode.com\n\n#TimeOwnership #FinancialFreedom #FIRE #MoneyMindset",
            },
            {
                "title": "Why Every Employee and Freelancer Has the Same Hidden Problem",
                "description": "Whether you're employed or freelancing — if you're billing hours, you're on the same treadmill. The only exit is income that doesn't need your presence. money-and-mode.com\n\n#PassiveIncome #FinancialIndependence #WealthBuilding #FIRE",
            },
        ],
    },
    115: {
        "url": "https://money-and-mode.com/family-emotional-connection-heaven-at-home/",
        "image_url": "https://money-and-mode.com/wp-content/uploads/2026/05/pinterest-family-connection.png",
        "board": "Life, Growth & Daily Habits",
        "variations": [
            {
                "title": "The Family That Feels Like Heaven — Why Connection Changes Everything",
                "description": "A family can share a house for 20 years and barely know each other. Or share one real conversation and feel completely connected. The difference is emotional presence — not time. money-and-mode.com\n\n#FamilyConnection #EmotionalConnection #FamilyLife #QualityTime",
            },
            {
                "title": "1 Year of Real Connection > 10 Years Side by Side",
                "description": "The difference between a family that feels like heaven and one that's just coexisting isn't time — it's depth. One real conversation beats a decade of surface-level. money-and-mode.com\n\n#FamilyFirst #DeepRelationships #HealthyFamily #MindfulParenting",
            },
            {
                "title": "Signs Your Family Is Truly Connected (Not Just Coexisting)",
                "description": "Conversations go deeper than logistics. People feel genuinely seen. Conflict gets resolved. You actually look forward to being home. The signs — and how to get there. money-and-mode.com\n\n#FamilyGoals #EmotionalConnection #HealthyFamily #FamilyLife",
            },
        ],
    },
}


# ── API helpers ───────────────────────────────────────────────────────────────

def get_boards():
    """Fetch all boards for the authenticated account."""
    resp = requests.get(f"{BASE_URL}/boards", headers=HEADERS, params={"page_size": 100})
    resp.raise_for_status()
    boards = resp.json().get("items", [])
    return {b["name"]: b["id"] for b in boards}


def create_pin(board_id: str, title: str, description: str, image_url: str, link: str) -> dict:
    """Create a single pin via Pinterest API v5."""
    payload = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "link": link,
        "media_source": {
            "source_type": "image_url",
            "url": image_url,
        },
    }
    resp = requests.post(f"{BASE_URL}/pins", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()


# ── Main logic ────────────────────────────────────────────────────────────────

def pin_article_variations(article_id: int, boards: dict, delay_seconds: int = 10):
    """Create all pin variations for a given article."""
    if article_id not in ARTICLE_PINS:
        print(f"❌ No pin data for article {article_id}")
        return

    data = ARTICLE_PINS[article_id]
    board_name = data["board"]
    board_id = boards.get(board_name)

    if not board_id:
        print(f"❌ Board '{board_name}' not found. Available: {list(boards.keys())}")
        return

    print(f"\n📌 Article {article_id} → Board: {board_name}")
    print(f"   {len(data['variations'])} variations to create\n")

    for i, variation in enumerate(data["variations"], 1):
        print(f"  [{i}/{len(data['variations'])}] Creating: {variation['title'][:60]}...")
        try:
            result = create_pin(
                board_id=board_id,
                title=variation["title"],
                description=variation["description"],
                image_url=data["image_url"],
                link=data["url"],
            )
            pin_id = result.get("id", "unknown")
            print(f"  ✅ Created pin ID: {pin_id}")

            # Delay between pins to avoid rate limits
            if i < len(data["variations"]):
                print(f"  ⏳ Waiting {delay_seconds}s before next pin...")
                time.sleep(delay_seconds)

        except requests.HTTPError as e:
            print(f"  ❌ Failed: {e.response.status_code} — {e.response.text}")

    print(f"\n✅ Done with article {article_id}")


def main():
    parser = argparse.ArgumentParser(description="Pinterest Growth Automation")
    parser.add_argument("--article", type=int, help="Article ID to pin all variations for")
    parser.add_argument("--all", action="store_true", help="Create variations for all articles")
    parser.add_argument("--boards", action="store_true", help="List all boards and their IDs")
    args = parser.parse_args()

    if not PINTEREST_ACCESS_TOKEN:
        print("❌ PINTEREST_ACCESS_TOKEN not set in .env")
        print("   See social-media/scripts/SETUP.md for instructions")
        return

    print("🔑 Fetching your Pinterest boards...")
    boards = get_boards()
    print(f"   Found {len(boards)} boards: {', '.join(boards.keys())}\n")

    if args.boards:
        print("\n📋 Your boards:")
        for name, bid in boards.items():
            print(f"  {name}: {bid}")
        return

    if args.article:
        pin_article_variations(args.article, boards)

    elif args.all:
        for article_id in ARTICLE_PINS:
            pin_article_variations(article_id, boards, delay_seconds=15)
            print("  💤 Sleeping 30s between articles...")
            time.sleep(30)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
