"""Seed the dashboard DB from existing project data. Safe to re-run."""
import json
from pathlib import Path
from db import get_conn, init_db

BASE  = Path(__file__).parent.parent
QUEUE = BASE / "social-media" / "queue.json"

ARTICLES = [
    dict(wp_post_id=74,  title="How AI Is Changing Everyday Life",               slug="how-ai-is-changing-everyday-life",          category="AI & Everyday Life",  keyword="how AI is changing everyday life",       series="ai-everyday",       status="published", wp_url="https://money-and-mode.com/how-ai-is-changing-everyday-life/",         publish_date="2026-05-26"),
    dict(wp_post_id=76,  title="How to Use AI to Save 2 Hours Every Day",        slug="how-to-use-ai-to-save-2-hours-every-day",   category="AI & Everyday Life",  keyword="how to use AI to save time",             series="ai-everyday",       status="published", wp_url="https://money-and-mode.com/how-to-use-ai-to-save-2-hours-every-day/",  publish_date="2026-05-30"),
    dict(wp_post_id=77,  title="Will AI Take My Job?",                           slug="will-ai-take-my-job",                       category="AI & Everyday Life",  keyword="will AI take my job",                    series="ai-everyday",       status="published", wp_url="https://money-and-mode.com/will-ai-take-my-job/",                       publish_date="2026-06-03"),
    dict(wp_post_id=93,  title="What Is ChatGPT?",                               slug="what-is-chatgpt",                           category="AI & Everyday Life",  keyword="what is ChatGPT explained simply",       series="ai-everyday",       status="draft",     publish_date="2026-06-06"),
    dict(wp_post_id=94,  title="10 Free AI Tools for Everyday Use",              slug="10-free-ai-tools",                          category="AI & Everyday Life",  keyword="best free AI tools for everyday use",    series="ai-everyday",       status="draft",     publish_date="2026-06-10"),
    dict(wp_post_id=95,  title="How to Talk to AI: A Beginner's Guide",          slug="how-to-talk-to-ai",                         category="AI & Everyday Life",  keyword="how to use ChatGPT for beginners",       series="ai-everyday",       status="draft",     publish_date="2026-06-13"),
    dict(wp_post_id=96,  title="AI for Parents",                                 slug="ai-for-parents",                            category="AI & Everyday Life",  keyword="AI for kids education",                  series="ai-everyday",       status="draft",     publish_date="2026-06-17"),
    dict(wp_post_id=97,  title="How AI Is Changing Healthcare",                  slug="how-ai-is-changing-healthcare",             category="AI & Everyday Life",  keyword="how AI is changing healthcare",          series="ai-everyday",       status="draft",     publish_date="2026-06-20"),
    dict(wp_post_id=110, title="I Sold My Company at 31",                        slug="i-sold-my-company-at-31-financial-freedom", category="Financial Freedom",   keyword="financial freedom story",                series="financial-freedom", status="published", wp_url="https://money-and-mode.com/i-sold-my-company-at-31-financial-freedom/", publish_date="2026-05-28"),
    dict(wp_post_id=112, title="If You Are Selling Your Time",                   slug="selling-your-time-financial-freedom",       category="Financial Freedom",   keyword="selling your time financial freedom",    series="financial-freedom", status="published", wp_url="https://money-and-mode.com/selling-your-time-financial-freedom-time-ownership/", publish_date="2026-06-01"),
    dict(wp_post_id=111, title="The Only Number That Determines Financial Freedom", slug="savings-rate-financial-freedom",         category="Financial Freedom",   keyword="savings rate financial freedom",         series="financial-freedom", status="draft"),
    dict(wp_post_id=113, title="Stop Selling Your Time. Build Leverage.",        slug="build-leverage-financial-freedom",          category="Financial Freedom",   keyword="build leverage financial independence",  series="financial-freedom", status="draft"),
    dict(wp_post_id=114, title="The 4% Rule Explained",                          slug="4-percent-rule-explained",                  category="Financial Freedom",   keyword="4 percent rule explained",               series="financial-freedom", status="draft"),
    dict(wp_post_id=None,title="Why Passive Income Is Mostly a Lie",             slug="passive-income-truth",                      category="Financial Freedom",   keyword="passive income truth",                   series="financial-freedom", status="written"),
    dict(wp_post_id=None,title="The Psychology of Money",                        slug="money-psychology",                          category="Financial Freedom",   keyword="psychology of money",                    series="financial-freedom", status="written"),
    dict(wp_post_id=None,title="Index Funds — The Boring Investment",            slug="index-funds-beginners",                     category="Financial Freedom",   keyword="index funds beginners guide",            series="financial-freedom", status="written"),
    dict(wp_post_id=115, title="The Family That Feels Like Heaven",              slug="family-emotional-connection-heaven",        category="Life & Motivation",   keyword="family emotional connection",            series="life",              status="published", wp_url="https://money-and-mode.com/family-emotional-connection-heaven-at-home/", publish_date="2026-06-05"),
    dict(wp_post_id=118, title="Connection Starts at Home",                      slug="connection-starts-at-home",                 category="Life & Motivation",   keyword="family connection home",                 series="life",              status="draft"),
]

TODOS = [
    dict(title="Edit Instagram post-74 — add missing caption (⋯ → Edit → paste)",   category="social",    priority="high",   due_date=None),
    dict(title="Publish WP draft 93 — What is ChatGPT (due Jun 6, overdue)",         category="content",   priority="high",   due_date="2026-06-06"),
    dict(title="Create blog email: blog@money-and-mode.com via IONOS",               category="technical", priority="high",   due_date=None),
    dict(title="Create Facebook Page: Fun in the Life",                              category="social",    priority="high",   due_date=None),
    dict(title="Post batch-1 X/Twitter posts (6 articles)",                          category="social",    priority="high",   due_date=None),
    dict(title="Post batch-1 Facebook posts (6 articles)",                           category="social",    priority="high",   due_date=None),
    dict(title="Get Pinterest API token → run pinterest_growth.py --all",            category="technical", priority="medium", due_date=None),
    dict(title="Get Twitter Bearer Token → run twitter_growth.py",                  category="technical", priority="medium", due_date=None),
    dict(title="pip install feedparser → run content_curator.py --fetch --draft",   category="technical", priority="medium", due_date=None),
    dict(title="Fill Instagram metrics in performance-log.json (7 days after post)", category="social",    priority="medium", due_date="2026-06-14"),
    dict(title="Rewrite Privacy Policy page (default WP boilerplate)",               category="seo",       priority="medium", due_date=None),
    dict(title="Set up email list + lead magnet (MailerLite)",                       category="content",   priority="medium", due_date=None),
    dict(title="Publish WP draft 94 — 10 Free AI Tools",                            category="content",   priority="medium", due_date="2026-06-10"),
    dict(title="Upload FF-06/07/08 SVGs to WordPress + create draft posts",          category="content",   priority="low",    due_date=None),
    dict(title="Apply for Ezoic once traffic hits 1,000 real humans/month",          category="general",   priority="low",    due_date=None),
]

TRAFFIC = [
    dict(month="2026-05", total_visitors=2344, real_humans_est=200, top_source="Direct/bots", new_articles=5, notes="Starting point"),
]

SETTINGS = [
    # (key, value, label, category)
    ("blog_url",          "https://money-and-mode.com", "Blog URL",               "general"),
    ("site_name",         "Fun in the Life",             "Site Name",              "general"),
    ("author_name",       "Kabir Shah",                  "Author / Pen Name",      "general"),
    ("adsense_target",    "5000",                        "AdSense Visitor Target", "traffic"),
    ("ezoic_target",      "1000",                        "Ezoic Visitor Target",   "traffic"),
    ("pub_days",          "Tuesday,Friday",              "Publish Days",           "content"),
    ("ig_handle",         "fun_in_life71",               "Instagram Handle",       "social"),
    ("twitter_handle",    "@justIndia25",                "Twitter / X Handle",     "social"),
    ("pinterest_handle",  "sandip2787",                  "Pinterest Handle",       "social"),
    ("wp_api_url",        "https://money-and-mode.com/wp-json/wp/v2", "WordPress API URL", "wordpress"),
    ("blog_email",        "funInTheLife2@gmail.com",                  "Blog Email (Gmail)", "general"),
]

KEYWORDS = [
    dict(keyword="how AI is changing everyday life",    article_title="How AI Is Changing Everyday Life",           monthly_searches_est=1900, competition="low"),
    dict(keyword="how to use AI to save time",           article_title="How to Use AI to Save 2 Hours Every Day",    monthly_searches_est=2400, competition="low"),
    dict(keyword="will AI take my job",                  article_title="Will AI Take My Job?",                       monthly_searches_est=4400, competition="medium"),
    dict(keyword="what is ChatGPT explained simply",     article_title="What Is ChatGPT?",                           monthly_searches_est=3600, competition="medium"),
    dict(keyword="best free AI tools for everyday use",  article_title="10 Free AI Tools for Everyday Use",          monthly_searches_est=2900, competition="low"),
    dict(keyword="financial freedom India",              article_title="I Sold My Company at 31",                    monthly_searches_est=1600, competition="low"),
    dict(keyword="passive income India",                 article_title="Why Passive Income Is Mostly a Lie",         monthly_searches_est=3500, competition="medium"),
    dict(keyword="index funds India beginners",          article_title="Index Funds — The Boring Investment",        monthly_searches_est=2100, competition="low"),
    dict(keyword="FIRE movement India",                  article_title="The Only Number That Determines Financial Freedom", monthly_searches_est=880, competition="low"),
    dict(keyword="family emotional connection",          article_title="The Family That Feels Like Heaven",          monthly_searches_est=720,  competition="low"),
]


def load_queue_posts(wp_to_db):
    posts = []
    if not QUEUE.exists():
        return posts
    with open(QUEUE) as f:
        data = json.load(f)
    for entry in data.get("pending", []):
        art_db_id = wp_to_db.get(entry.get("article_id"))
        platform  = entry.get("platform", "")
        caption   = (entry.get("caption") or entry.get("pin_title") or "")[:500]
        status    = entry.get("status", "pending")
        posts.append(dict(article_id=art_db_id, platform=platform, caption=caption,
                          status=status, posted_date=entry.get("posted_date"),
                          notes=entry.get("id", "")))
    return posts


def seed():
    init_db()
    with get_conn() as conn:
        # Articles
        print("Seeding articles...")
        wp_to_db = {}; title_to_id = {}
        for a in ARTICLES:
            conn.execute("""
                INSERT OR IGNORE INTO articles
                  (wp_post_id,title,slug,category,keyword,series,status,wp_url,publish_date)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (a.get("wp_post_id"), a["title"], a.get("slug"), a.get("category"),
                  a.get("keyword"), a.get("series"), a.get("status","planned"),
                  a.get("wp_url"), a.get("publish_date")))
            row = conn.execute("SELECT id FROM articles WHERE title=?", (a["title"],)).fetchone()
            if row:
                title_to_id[a["title"]] = row["id"]
                if a.get("wp_post_id"):
                    wp_to_db[a["wp_post_id"]] = row["id"]

        # Social posts
        print("Seeding social posts...")
        for p in load_queue_posts(wp_to_db):
            conn.execute("""
                INSERT OR IGNORE INTO social_posts (article_id,platform,caption,status,posted_date,notes)
                VALUES (?,?,?,?,?,?)
            """, (p["article_id"], p["platform"], p["caption"],
                  p["status"], p["posted_date"], p["notes"]))
        for db_id in wp_to_db.values():
            for plat in ("twitter", "facebook"):
                if not conn.execute("SELECT id FROM social_posts WHERE article_id=? AND platform=?",
                                    (db_id, plat)).fetchone():
                    conn.execute("INSERT INTO social_posts (article_id,platform,status) VALUES (?,?,'pending')",
                                 (db_id, plat))

        # Todos
        print("Seeding todos...")
        for t in TODOS:
            conn.execute("INSERT OR IGNORE INTO todos (title,category,priority,status,due_date) VALUES (?,?,?,'pending',?)",
                (t["title"], t.get("category","general"), t.get("priority","medium"), t.get("due_date")))

        # Traffic
        print("Seeding traffic...")
        for tr in TRAFFIC:
            conn.execute("INSERT OR IGNORE INTO traffic (month,total_visitors,real_humans_est,top_source,new_articles,notes) VALUES (?,?,?,?,?,?)",
                (tr["month"], tr["total_visitors"], tr["real_humans_est"],
                 tr["top_source"], tr["new_articles"], tr.get("notes","")))

        # Keywords
        print("Seeding keywords...")
        for kw in KEYWORDS:
            aid = title_to_id.get(kw["article_title"])
            conn.execute("INSERT OR IGNORE INTO keywords (keyword,article_id,monthly_searches_est,competition) VALUES (?,?,?,?)",
                (kw["keyword"], aid, kw["monthly_searches_est"], kw["competition"]))

        # Settings
        print("Seeding settings...")
        for key, value, label, category in SETTINGS:
            conn.execute("""
                INSERT OR IGNORE INTO settings (key, value, label, category)
                VALUES (?, ?, ?, ?)
            """, (key, value, label, category))

        conn.commit()
    print("✅ Seed complete.")


if __name__ == "__main__":
    seed()
