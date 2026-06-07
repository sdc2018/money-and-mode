"""
Seed the dashboard DB from existing project JSON files + STATUS.md.
Run once (or re-run safely — uses INSERT OR IGNORE).
"""
import json, re
from pathlib import Path
from db import get_conn, init_db

BASE   = Path(__file__).parent.parent
QUEUE  = BASE / "social-media" / "queue.json"
PERF   = BASE / "social-media" / "system" / "performance-log.json"


# ─── Articles ─────────────────────────────────────────────────────────────────

ARTICLES = [
    # AI Series — published
    dict(wp_post_id=74,  title="How AI Is Changing Everyday Life",         slug="how-ai-is-changing-everyday-life",          category="AI & Everyday Life",    keyword="how AI is changing everyday life",     series="ai-everyday",       status="published", wp_url="https://money-and-mode.com/how-ai-is-changing-everyday-life/",          publish_date="2026-05-26"),
    dict(wp_post_id=76,  title="How to Use AI to Save 2 Hours Every Day",  slug="how-to-use-ai-to-save-2-hours-every-day",   category="AI & Everyday Life",    keyword="how to use AI to save time",           series="ai-everyday",       status="published", wp_url="https://money-and-mode.com/how-to-use-ai-to-save-2-hours-every-day/",   publish_date="2026-05-30"),
    dict(wp_post_id=77,  title="Will AI Take My Job?",                     slug="will-ai-take-my-job",                       category="AI & Everyday Life",    keyword="will AI take my job",                  series="ai-everyday",       status="published", wp_url="https://money-and-mode.com/will-ai-take-my-job/",                        publish_date="2026-06-03"),
    # AI Series — drafts
    dict(wp_post_id=93,  title="What Is ChatGPT?",                         slug="what-is-chatgpt",                           category="AI & Everyday Life",    keyword="what is ChatGPT explained simply",     series="ai-everyday",       status="draft",     publish_date="2026-06-06"),
    dict(wp_post_id=94,  title="10 Free AI Tools for Everyday Use",        slug="10-free-ai-tools",                          category="AI & Everyday Life",    keyword="best free AI tools for everyday use",  series="ai-everyday",       status="draft",     publish_date="2026-06-10"),
    dict(wp_post_id=95,  title="How to Talk to AI: A Beginner's Guide",    slug="how-to-talk-to-ai",                         category="AI & Everyday Life",    keyword="how to use ChatGPT for beginners",     series="ai-everyday",       status="draft",     publish_date="2026-06-13"),
    dict(wp_post_id=96,  title="AI for Parents",                           slug="ai-for-parents",                            category="AI & Everyday Life",    keyword="AI for kids education",                series="ai-everyday",       status="draft",     publish_date="2026-06-17"),
    dict(wp_post_id=97,  title="How AI Is Changing Healthcare",            slug="how-ai-is-changing-healthcare",             category="AI & Everyday Life",    keyword="how AI is changing healthcare",        series="ai-everyday",       status="draft",     publish_date="2026-06-20"),
    # Financial Freedom — published
    dict(wp_post_id=110, title="I Sold My Company at 31",                  slug="i-sold-my-company-at-31-financial-freedom", category="Financial Freedom",     keyword="financial freedom story",              series="financial-freedom", status="published", wp_url="https://money-and-mode.com/i-sold-my-company-at-31-financial-freedom/",  publish_date="2026-05-28"),
    dict(wp_post_id=112, title="If You Are Selling Your Time",             slug="selling-your-time-financial-freedom",       category="Financial Freedom",     keyword="selling your time financial freedom",  series="financial-freedom", status="published", wp_url="https://money-and-mode.com/selling-your-time-financial-freedom-time-ownership/", publish_date="2026-06-01"),
    # Financial Freedom — drafts
    dict(wp_post_id=111, title="The Only Number That Determines Financial Freedom", slug="savings-rate-financial-freedom",  category="Financial Freedom",     keyword="savings rate financial freedom",       series="financial-freedom", status="draft",     publish_date=None),
    dict(wp_post_id=113, title="Stop Selling Your Time. Build Leverage.",  slug="build-leverage-financial-freedom",          category="Financial Freedom",     keyword="build leverage financial independence", series="financial-freedom", status="draft",     publish_date=None),
    dict(wp_post_id=114, title="The 4% Rule Explained",                    slug="4-percent-rule-explained",                  category="Financial Freedom",     keyword="4 percent rule explained",             series="financial-freedom", status="draft",     publish_date=None),
    # Financial Freedom — written locally, needs WP upload
    dict(wp_post_id=None, title="Why Passive Income Is Mostly a Lie",     slug="passive-income-truth",                      category="Financial Freedom",     keyword="passive income truth",                 series="financial-freedom", status="written",   publish_date=None),
    dict(wp_post_id=None, title="The Psychology of Money",                 slug="money-psychology",                          category="Financial Freedom",     keyword="psychology of money",                  series="financial-freedom", status="written",   publish_date=None),
    dict(wp_post_id=None, title="Index Funds — The Boring Investment",     slug="index-funds-beginners",                     category="Financial Freedom",     keyword="index funds beginners guide",          series="financial-freedom", status="written",   publish_date=None),
    # Life & Motivation
    dict(wp_post_id=115, title="The Family That Feels Like Heaven",        slug="family-emotional-connection-heaven",        category="Life & Motivation",     keyword="family emotional connection",          series="life",              status="published", wp_url="https://money-and-mode.com/family-emotional-connection-heaven-at-home/",  publish_date="2026-06-05"),
    dict(wp_post_id=118, title="Connection Starts at Home",                slug="connection-starts-at-home",                 category="Life & Motivation",     keyword="family connection home",               series="life",              status="draft",     publish_date=None),
]

# ─── Todos (from STATUS.md open actions) ───────────────────────────────────────

TODOS = [
    dict(title="Edit Instagram post-74 — add missing caption (⋯ → Edit → paste)", category="social",   priority="high",   status="pending"),
    dict(title="Publish WP draft 93 — What is ChatGPT (due Jun 6, overdue)",        category="content",  priority="high",   status="pending"),
    dict(title="Create blog email: blog@money-and-mode.com via IONOS",              category="technical",priority="high",   status="pending"),
    dict(title="Create Facebook Page: Fun in the Life",                             category="social",   priority="high",   status="pending"),
    dict(title="Post batch-1 X/Twitter threads (6 articles)",                      category="social",   priority="high",   status="pending"),
    dict(title="Post batch-1 Facebook posts (6 articles)",                         category="social",   priority="high",   status="pending"),
    dict(title="Get Pinterest API access token → run pinterest_growth.py --all",   category="technical",priority="medium", status="pending"),
    dict(title="Get Twitter Bearer Token → run twitter_growth.py --find",          category="technical",priority="medium", status="pending"),
    dict(title="Install feedparser → run content_curator.py --fetch --draft",      category="technical",priority="medium", status="pending"),
    dict(title="Fill performance metrics for Jun 7 Instagram posts (7 days later)",category="social",   priority="medium", status="pending", due_date="2026-06-14"),
    dict(title="Rewrite Privacy Policy page (currently default WP boilerplate)",   category="seo",      priority="medium", status="pending"),
    dict(title="Set up email list capture + lead magnet (MailerLite)",             category="content",  priority="medium", status="pending"),
    dict(title="Publish WP draft 94 — 10 Free AI Tools (due Jun 10)",             category="content",  priority="medium", status="pending", due_date="2026-06-10"),
    dict(title="Upload FF-06/07/08 SVG→PNG to WordPress + create draft posts",     category="content",  priority="low",    status="pending"),
    dict(title="Apply for Ezoic once traffic hits 1,000 real humans/month",        category="general",  priority="low",    status="pending"),
]

# ─── Traffic ──────────────────────────────────────────────────────────────────

TRAFFIC = [
    dict(month="2026-05", total_visitors=2344, real_humans_est=200, top_source="Direct/bots", new_articles=5, notes="Starting point — mostly bots"),
]


# ─── Social posts from queue.json ─────────────────────────────────────────────

def load_queue_posts(article_id_map):
    """Read queue.json and return social_posts rows."""
    posts = []
    if not QUEUE.exists():
        return posts
    with open(QUEUE) as f:
        data = json.load(f)
    for entry in data.get("pending", []):
        art_title = entry.get("article_title", "")
        # Find matching article id
        article_db_id = article_id_map.get(entry.get("article_id"))
        platform = entry.get("platform", "")
        caption = entry.get("caption") or entry.get("pin_title") or entry.get("description", "")
        status = entry.get("status", "pending")
        posted_date = entry.get("posted_date")
        posts.append(dict(
            article_id=article_db_id,
            platform=platform,
            caption=caption[:500] if caption else "",
            status=status,
            posted_date=posted_date,
            notes=entry.get("id", ""),
        ))
    return posts


def seed():
    init_db()
    with get_conn() as conn:
        # ── Articles ──────────────────────────────────────────────────────────
        print("Seeding articles...")
        wp_to_db = {}
        for a in ARTICLES:
            cur = conn.execute("""
                INSERT OR IGNORE INTO articles
                  (wp_post_id, title, slug, category, keyword, series, status, wp_url, publish_date)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (a.get("wp_post_id"), a["title"], a.get("slug"), a.get("category"),
                  a.get("keyword"), a.get("series"), a.get("status","planned"),
                  a.get("wp_url"), a.get("publish_date")))
            row = conn.execute("SELECT id FROM articles WHERE title=?", (a["title"],)).fetchone()
            if row and a.get("wp_post_id"):
                wp_to_db[a["wp_post_id"]] = row["id"]

        # ── Social Posts ──────────────────────────────────────────────────────
        print("Seeding social posts from queue.json...")
        posts = load_queue_posts(wp_to_db)
        for p in posts:
            conn.execute("""
                INSERT OR IGNORE INTO social_posts
                  (article_id, platform, caption, status, posted_date, notes)
                VALUES (?,?,?,?,?,?)
            """, (p["article_id"], p["platform"], p["caption"],
                  p["status"], p["posted_date"], p["notes"]))

        # X + Facebook posts as pending for all published articles
        for wp_id, db_id in wp_to_db.items():
            for plat in ("twitter", "facebook"):
                exists = conn.execute(
                    "SELECT id FROM social_posts WHERE article_id=? AND platform=?",
                    (db_id, plat)
                ).fetchone()
                if not exists:
                    conn.execute("""
                        INSERT INTO social_posts (article_id, platform, status)
                        VALUES (?, ?, 'pending')
                    """, (db_id, plat))

        # ── Todos ─────────────────────────────────────────────────────────────
        print("Seeding todos...")
        for t in TODOS:
            conn.execute("""
                INSERT OR IGNORE INTO todos (title, category, priority, status, due_date)
                VALUES (?,?,?,?,?)
            """, (t["title"], t.get("category","general"), t.get("priority","medium"),
                  t.get("status","pending"), t.get("due_date")))

        # ── Traffic ───────────────────────────────────────────────────────────
        print("Seeding traffic data...")
        for tr in TRAFFIC:
            conn.execute("""
                INSERT OR IGNORE INTO traffic (month, total_visitors, real_humans_est, top_source, new_articles, notes)
                VALUES (?,?,?,?,?,?)
            """, (tr["month"], tr["total_visitors"], tr["real_humans_est"],
                  tr["top_source"], tr["new_articles"], tr.get("notes","")))

        conn.commit()
    print("✅ Seed complete.")


if __name__ == "__main__":
    seed()
