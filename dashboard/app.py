"""
money-and-mode Dashboard — FastAPI backend
Run: python app.py
Opens: http://localhost:8765
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from pathlib import Path
import json
import subprocess
import uvicorn

from db import get_conn, init_db

app = FastAPI(title="money-and-mode Dashboard", version="1.0")

STATIC       = Path(__file__).parent / "static"
BASE         = Path(__file__).parent.parent
DIGESTS_DIR  = BASE / "social-media" / "digests"
SOURCES_FILE = BASE / "marketing" / "sources.json"
CURATOR_PY   = BASE / "social-media" / "scripts" / "content_curator.py"


# ══════════════════════════════════════════════════════════════════════════════
#  Pydantic models (request bodies)
# ══════════════════════════════════════════════════════════════════════════════

class TodoCreate(BaseModel):
    title: str
    category: Optional[str] = "general"
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None
    notes: Optional[str] = None

class TodoUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    title: Optional[str] = None

class PostStatusUpdate(BaseModel):
    status: str   # pending | posted | skipped
    posted_date: Optional[str] = None

class MetricUpdate(BaseModel):
    likes: Optional[int] = None
    comments: Optional[int] = None
    saves: Optional[int] = None
    shares: Optional[int] = None
    reach: Optional[int] = None
    impressions: Optional[int] = None
    link_clicks: Optional[int] = None

class TrafficEntry(BaseModel):
    month: str
    total_visitors: int
    real_humans_est: Optional[int] = None
    top_source: Optional[str] = None
    new_articles: Optional[int] = None
    notes: Optional[str] = None

class KeywordCreate(BaseModel):
    keyword: str
    article_id: Optional[int] = None
    target_url: Optional[str] = None
    monthly_searches_est: Optional[int] = None
    competition: Optional[str] = "unknown"
    notes: Optional[str] = None

class RankEntry(BaseModel):
    rank: Optional[int] = None   # None = not ranking
    notes: Optional[str] = None

class ArticleCreate(BaseModel):
    title: str
    keyword: Optional[str] = None
    series: Optional[str] = "ai-everyday"
    category: Optional[str] = "AI & Everyday Life"
    status: Optional[str] = "planned"
    publish_date: Optional[str] = None
    wp_post_id: Optional[int] = None
    wp_url: Optional[str] = None
    slug: Optional[str] = None
    notes: Optional[str] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    publish_date: Optional[str] = None
    keyword: Optional[str] = None
    wp_url: Optional[str] = None
    notes: Optional[str] = None

class DigestItemEdit(BaseModel):
    url: str
    kabirs_take: Optional[str] = None
    status: Optional[str] = "include"   # include | skip

class SourceUpdate(BaseModel):
    active: Optional[bool] = None
    authority: Optional[int] = None
    notes: Optional[str] = None

class SourceCreate(BaseModel):
    name: str
    rss: str
    topic: str           # ai_technology | financial_freedom | life_motivation
    source_type: str = "blog"    # blog | news | youtube | official | analysis
    authority: int = 3
    notes: Optional[str] = None

class SettingsUpdate(BaseModel):
    settings: dict   # {key: value, ...}


# ══════════════════════════════════════════════════════════════════════════════
#  Overview
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/overview")
def get_overview():
    today = date.today().isoformat()
    with get_conn() as conn:
        # Article stats
        art_stats = {r["status"]: r["cnt"] for r in conn.execute(
            "SELECT status, COUNT(*) cnt FROM articles GROUP BY status"
        ).fetchall()}

        # Social post stats
        post_stats = {r["status"]: r["cnt"] for r in conn.execute(
            "SELECT status, COUNT(*) cnt FROM social_posts GROUP BY status"
        ).fetchall()}

        # Overdue drafts (publish_date < today and status != published)
        overdue = conn.execute("""
            SELECT COUNT(*) cnt FROM articles
            WHERE publish_date < ? AND status IN ('draft','written') AND publish_date IS NOT NULL
        """, (today,)).fetchone()["cnt"]

        # Pending todos by priority
        todos_pending = conn.execute(
            "SELECT COUNT(*) cnt FROM todos WHERE status='pending'"
        ).fetchone()["cnt"]
        todos_high = conn.execute(
            "SELECT COUNT(*) cnt FROM todos WHERE status='pending' AND priority='high'"
        ).fetchone()["cnt"]

        # Posts due this week (articles with publish_date in next 7 days)
        due_soon = conn.execute("""
            SELECT title, publish_date, status FROM articles
            WHERE publish_date BETWEEN ? AND date(?, '+7 days')
              AND status IN ('draft','written','planned')
            ORDER BY publish_date
        """, (today, today)).fetchall()

        # Latest traffic
        traffic = conn.execute(
            "SELECT * FROM traffic ORDER BY month DESC LIMIT 1"
        ).fetchone()

        # Recent posts (last 7 days)
        recent_posts = conn.execute("""
            SELECT sp.platform, a.title, sp.posted_date
            FROM social_posts sp
            JOIN articles a ON a.id = sp.article_id
            WHERE sp.status='posted' AND sp.posted_date >= date('now', '-7 days')
            ORDER BY sp.posted_date DESC
        """).fetchall()

    real_humans = traffic["real_humans_est"] if traffic else 0
    target = 5000
    pct = round((real_humans / target) * 100, 1) if real_humans else 0

    return {
        "today": today,
        "articles": {
            "published":  art_stats.get("published", 0),
            "draft":      art_stats.get("draft", 0),
            "written":    art_stats.get("written", 0),
            "planned":    art_stats.get("planned", 0),
            "overdue":    overdue,
        },
        "social": {
            "posted":     post_stats.get("posted", 0),
            "pending":    post_stats.get("pending", 0),
            "total":      sum(post_stats.values()),
        },
        "todos": {
            "pending":    todos_pending,
            "high":       todos_high,
        },
        "adsense_progress": {
            "current":    real_humans,
            "target":     target,
            "percent":    pct,
        },
        "due_soon":     [dict(r) for r in due_soon],
        "recent_posts": [dict(r) for r in recent_posts],
    }


# ══════════════════════════════════════════════════════════════════════════════
#  Articles
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/articles")
def get_articles(status: Optional[str] = None, series: Optional[str] = None):
    with get_conn() as conn:
        q = "SELECT * FROM articles WHERE 1=1"
        params = []
        if status:
            q += " AND status=?"; params.append(status)
        if series:
            q += " AND series=?"; params.append(series)
        q += " ORDER BY CASE status WHEN 'published' THEN 1 WHEN 'draft' THEN 2 WHEN 'written' THEN 3 ELSE 4 END, publish_date"
        return [dict(r) for r in conn.execute(q, params).fetchall()]


@app.get("/api/articles/pipeline")
def get_pipeline():
    """Kanban data — articles grouped by status."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM articles ORDER BY publish_date NULLS LAST"
        ).fetchall()
    groups = {"planned": [], "written": [], "draft": [], "published": []}
    for r in rows:
        d = dict(r)
        groups.setdefault(d["status"], []).append(d)
    return groups


# ══════════════════════════════════════════════════════════════════════════════
#  Social Posts
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/posts")
def get_posts(platform: Optional[str] = None, status: Optional[str] = None):
    with get_conn() as conn:
        q = """
            SELECT sp.*, a.title article_title, a.wp_url, a.series
            FROM social_posts sp
            LEFT JOIN articles a ON a.id = sp.article_id
            WHERE 1=1
        """
        params = []
        if platform:
            q += " AND sp.platform=?"; params.append(platform)
        if status:
            q += " AND sp.status=?"; params.append(status)
        q += " ORDER BY sp.created_at DESC"
        return [dict(r) for r in conn.execute(q, params).fetchall()]


@app.get("/api/posts/matrix")
def get_posts_matrix():
    """For each article, show status across all 4 platforms."""
    with get_conn() as conn:
        articles = conn.execute(
            "SELECT id, title, wp_url, series, status art_status FROM articles ORDER BY id"
        ).fetchall()
        posts = conn.execute(
            "SELECT article_id, platform, status, posted_date FROM social_posts"
        ).fetchall()

    post_map = {}
    for p in posts:
        post_map.setdefault(p["article_id"], {})[p["platform"]] = {
            "status": p["status"], "posted_date": p["posted_date"]
        }

    result = []
    for a in articles:
        plats = post_map.get(a["id"], {})
        result.append({
            "article_id":   a["id"],
            "title":        a["title"],
            "art_status":   a["art_status"],
            "wp_url":       a["wp_url"],
            "series":       a["series"],
            "instagram":    plats.get("instagram",  {"status": "none"}),
            "twitter":      plats.get("twitter",    {"status": "none"}),
            "facebook":     plats.get("facebook",   {"status": "none"}),
            "pinterest":    plats.get("pinterest",  {"status": "none"}),
        })
    return result


@app.put("/api/posts/{post_id}/status")
def update_post_status(post_id: int, body: PostStatusUpdate):
    with get_conn() as conn:
        posted = body.posted_date or (date.today().isoformat() if body.status == "posted" else None)
        conn.execute(
            "UPDATE social_posts SET status=?, posted_date=? WHERE id=?",
            (body.status, posted, post_id)
        )
        conn.commit()
    return {"ok": True}


@app.put("/api/posts/{post_id}/metrics")
def update_metrics(post_id: int, m: MetricUpdate):
    with get_conn() as conn:
        exists = conn.execute(
            "SELECT id FROM metrics WHERE social_post_id=?", (post_id,)
        ).fetchone()
        sp = conn.execute(
            "SELECT platform FROM social_posts WHERE id=?", (post_id,)
        ).fetchone()
        if not sp:
            raise HTTPException(404, "Post not found")
        if exists:
            conn.execute("""
                UPDATE metrics SET likes=COALESCE(?,likes), comments=COALESCE(?,comments),
                  saves=COALESCE(?,saves), shares=COALESCE(?,shares), reach=COALESCE(?,reach),
                  impressions=COALESCE(?,impressions), link_clicks=COALESCE(?,link_clicks),
                  recorded_date=date('now') WHERE social_post_id=?
            """, (m.likes, m.comments, m.saves, m.shares, m.reach, m.impressions, m.link_clicks, post_id))
        else:
            conn.execute("""
                INSERT INTO metrics (social_post_id, platform, likes, comments, saves, shares, reach, impressions, link_clicks)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (post_id, sp["platform"], m.likes, m.comments, m.saves, m.shares, m.reach, m.impressions, m.link_clicks))
        conn.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Todos
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/todos")
def get_todos(status: Optional[str] = None, category: Optional[str] = None):
    with get_conn() as conn:
        q = "SELECT * FROM todos WHERE 1=1"
        params = []
        if status:
            q += " AND status=?"; params.append(status)
        if category:
            q += " AND category=?"; params.append(category)
        q += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, created_at"
        return [dict(r) for r in conn.execute(q, params).fetchall()]


@app.post("/api/todos")
def create_todo(todo: TodoCreate):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO todos (title, category, priority, due_date, notes)
            VALUES (?,?,?,?,?)
        """, (todo.title, todo.category, todo.priority, todo.due_date, todo.notes))
        conn.commit()
        return {"id": cur.lastrowid, **todo.dict()}


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, body: TodoUpdate):
    with get_conn() as conn:
        if body.status == "done":
            conn.execute(
                "UPDATE todos SET status='done', completed_at=datetime('now') WHERE id=?",
                (todo_id,)
            )
        else:
            updates, params = [], []
            if body.status:  updates.append("status=?");   params.append(body.status)
            if body.priority: updates.append("priority=?"); params.append(body.priority)
            if body.title:   updates.append("title=?");    params.append(body.title)
            if updates:
                conn.execute(f"UPDATE todos SET {', '.join(updates)} WHERE id=?", params + [todo_id])
        conn.commit()
    return {"ok": True}


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        conn.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Traffic & AdSense
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/traffic")
def get_traffic():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM traffic ORDER BY month DESC LIMIT 12"
        ).fetchall()]


@app.post("/api/traffic")
def add_traffic(entry: TrafficEntry):
    with get_conn() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO traffic
              (month, total_visitors, real_humans_est, top_source, new_articles, notes)
            VALUES (?,?,?,?,?,?)
        """, (entry.month, entry.total_visitors, entry.real_humans_est,
              entry.top_source, entry.new_articles, entry.notes))
        conn.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Performance (metrics summary)
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/performance")
def get_performance():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT sp.id post_id, a.title, a.series, sp.platform, sp.posted_date,
                   m.likes, m.comments, m.saves, m.shares, m.reach, m.link_clicks
            FROM social_posts sp
            JOIN articles a      ON a.id  = sp.article_id
            LEFT JOIN metrics m  ON m.social_post_id = sp.id
            WHERE sp.status = 'posted'
            ORDER BY sp.posted_date DESC
        """).fetchall()
        top_saves = conn.execute("""
            SELECT a.title, SUM(COALESCE(m.saves,0)) total_saves,
                   SUM(COALESCE(m.reach,0)) total_reach,
                   SUM(COALESCE(m.comments,0)) total_comments
            FROM metrics m
            JOIN social_posts sp ON sp.id = m.social_post_id
            JOIN articles a      ON a.id  = sp.article_id
            WHERE m.saves IS NOT NULL
            GROUP BY a.id ORDER BY total_saves DESC LIMIT 5
        """).fetchall()
        platform_stats = conn.execute("""
            SELECT sp.platform,
                   COUNT(*)                          total_posts,
                   SUM(COALESCE(m.saves,0))          total_saves,
                   SUM(COALESCE(m.comments,0))       total_comments,
                   SUM(COALESCE(m.reach,0))          total_reach,
                   AVG(CASE WHEN m.reach>0 THEN CAST(m.saves AS FLOAT)/m.reach*100 END) avg_save_rate
            FROM social_posts sp
            LEFT JOIN metrics m ON m.social_post_id = sp.id
            WHERE sp.status='posted'
            GROUP BY sp.platform
        """).fetchall()
        has_data = conn.execute("SELECT COUNT(*) cnt FROM metrics").fetchone()["cnt"] > 0
    return {
        "posts":          [dict(r) for r in rows],
        "top_saves":      [dict(r) for r in top_saves],
        "platform_stats": [dict(r) for r in platform_stats],
        "has_data":       has_data,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  Content Calendar
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/calendar/{year}/{month}")
def get_calendar(year: int, month: int):
    import calendar
    month_str = f"{year}-{month:02d}"
    days_in_month = calendar.monthrange(year, month)[1]
    with get_conn() as conn:
        articles = conn.execute("""
            SELECT id, title, slug, status, publish_date, series, wp_url
            FROM articles
            WHERE publish_date LIKE ?
            ORDER BY publish_date
        """, (f"{month_str}%",)).fetchall()

    day_map = {}
    for a in articles:
        d = a["publish_date"][-2:]   # last 2 chars = day
        day_map.setdefault(d, []).append(dict(a))

    return {
        "year": year, "month": month, "days_in_month": days_in_month,
        "first_weekday": calendar.monthrange(year, month)[0],   # 0=Mon
        "articles_by_day": day_map,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  Keywords
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/keywords")
def get_keywords():
    with get_conn() as conn:
        kws = conn.execute("""
            SELECT k.*,
                   a.title article_title, a.wp_url,
                   (SELECT rank FROM keyword_rankings WHERE keyword_id=k.id
                    ORDER BY recorded_date DESC LIMIT 1) current_rank,
                   (SELECT rank FROM keyword_rankings WHERE keyword_id=k.id
                    ORDER BY recorded_date DESC LIMIT 1 OFFSET 1) prev_rank,
                   (SELECT recorded_date FROM keyword_rankings WHERE keyword_id=k.id
                    ORDER BY recorded_date DESC LIMIT 1) last_checked
            FROM keywords k
            LEFT JOIN articles a ON a.id = k.article_id
            ORDER BY k.created_at DESC
        """).fetchall()
    return [dict(r) for r in kws]

@app.post("/api/keywords")
def create_keyword(kw: KeywordCreate):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO keywords (keyword, article_id, target_url, monthly_searches_est, competition, notes)
            VALUES (?,?,?,?,?,?)
        """, (kw.keyword, kw.article_id, kw.target_url, kw.monthly_searches_est, kw.competition, kw.notes))
        conn.commit()
        return {"id": cur.lastrowid, **kw.dict()}

@app.post("/api/keywords/{kw_id}/rank")
def add_rank(kw_id: int, entry: RankEntry):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO keyword_rankings (keyword_id, rank, notes) VALUES (?,?,?)",
            (kw_id, entry.rank, entry.notes)
        )
        conn.commit()
    return {"ok": True}

@app.delete("/api/keywords/{kw_id}")
def delete_keyword(kw_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM keyword_rankings WHERE keyword_id=?", (kw_id,))
        conn.execute("DELETE FROM keywords WHERE id=?", (kw_id,))
        conn.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Articles — CRUD (create, update, delete)
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/api/articles")
def create_article(a: ArticleCreate):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO articles (title, keyword, series, category, status,
                                  publish_date, wp_post_id, wp_url, slug, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (a.title, a.keyword, a.series, a.category, a.status,
              a.publish_date, a.wp_post_id, a.wp_url, a.slug, a.notes))
        conn.commit()
        return {"id": cur.lastrowid, **a.dict()}


@app.put("/api/articles/{article_id}")
def update_article(article_id: int, a: ArticleUpdate):
    updates, params = [], []
    if a.title:        updates.append("title=?");        params.append(a.title)
    if a.status:       updates.append("status=?");       params.append(a.status)
    if a.publish_date: updates.append("publish_date=?"); params.append(a.publish_date)
    if a.keyword:      updates.append("keyword=?");      params.append(a.keyword)
    if a.wp_url:       updates.append("wp_url=?");       params.append(a.wp_url)
    if a.notes:        updates.append("notes=?");        params.append(a.notes)
    if not updates:
        return {"ok": True}
    with get_conn() as conn:
        conn.execute(f"UPDATE articles SET {', '.join(updates)} WHERE id=?", params + [article_id])
        conn.commit()
    return {"ok": True}


@app.delete("/api/articles/{article_id}")
def delete_article(article_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM articles WHERE id=?", (article_id,))
        conn.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Settings
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/api/settings")
def get_settings():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT key, value, label, category FROM settings ORDER BY category, key"
        ).fetchall()
    # Return as dict for easy lookup, plus ordered list for display
    result = {}
    for r in rows:
        result[r["key"]] = {"value": r["value"], "label": r["label"], "category": r["category"]}
    return result


@app.put("/api/settings")
def update_settings(body: SettingsUpdate):
    with get_conn() as conn:
        for key, value in body.settings.items():
            conn.execute("""
                UPDATE settings SET value=?, updated_at=datetime('now') WHERE key=?
            """, (str(value), key))
        conn.commit()
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Digest — read curator output, edit Kabir's take, generate WP HTML
# ══════════════════════════════════════════════════════════════════════════════

def _load_digest_edits(conn, week):
    rows = conn.execute(
        "SELECT url, kabirs_take, status FROM digest_edits WHERE week=?", (week,)
    ).fetchall()
    return {r["url"]: {"kabirs_take": r["kabirs_take"], "status": r["status"]} for r in rows}


@app.get("/api/digest/weeks")
def get_digest_weeks():
    """List all available digest JSON files."""
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(DIGESTS_DIR.glob("digest-*.json"), reverse=True)
    weeks = []
    for f in files:
        try:
            data = json.loads(f.read_text())
            weeks.append({"week": data.get("week", f.stem.replace("digest-","")),
                          "label": data.get("label", f.stem),
                          "file":  f.name})
        except Exception:
            pass
    return weeks


@app.get("/api/digest/{week}")
def get_digest(week: str):
    """Return digest items for a week, merged with any saved edits."""
    digest_file = DIGESTS_DIR / f"digest-{week}.json"
    if not digest_file.exists():
        raise HTTPException(404, f"No digest found for week {week}")
    data = json.loads(digest_file.read_text())
    results = data.get("results", {})

    with get_conn() as conn:
        edits = _load_digest_edits(conn, week)

    topic_labels = {
        "ai_technology":    "AI & Technology",
        "financial_freedom": "Financial Freedom",
        "life_motivation":  "Life & Motivation",
    }

    items = []
    for topic, articles in results.items():
        for a in articles[:3]:  # top 3 per topic
            url = a.get("url", "")
            edit = edits.get(url, {})
            items.append({
                "topic":       topic,
                "topic_label": topic_labels.get(topic, topic),
                "title":       a.get("title", ""),
                "url":         url,
                "source":      a.get("source", ""),
                "summary":     a.get("summary", ""),
                "score":       a.get("score", 0),
                "published":   a.get("published", ""),
                "kabirs_take": edit.get("kabirs_take", ""),
                "status":      edit.get("status", "include"),
            })

    return {"week": week, "label": data.get("label",""), "items": items}


@app.put("/api/digest/{week}/item")
def save_digest_item(week: str, body: DigestItemEdit):
    """Save Kabir's take + include/skip for one item."""
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO digest_edits (week, url, kabirs_take, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(week, url) DO UPDATE SET
                kabirs_take=excluded.kabirs_take,
                status=excluded.status,
                updated_at=datetime('now')
        """, (week, body.url, body.kabirs_take, body.status))
        conn.commit()
    return {"ok": True}


@app.post("/api/digest/{week}/generate")
def generate_digest_html(week: str):
    """Generate WordPress-ready HTML from the included items."""
    digest_file = DIGESTS_DIR / f"digest-{week}.json"
    if not digest_file.exists():
        raise HTTPException(404, "Digest not found")

    data = json.loads(digest_file.read_text())
    results = data.get("results", {})

    with get_conn() as conn:
        edits = _load_digest_edits(conn, week)

    topic_labels = {
        "ai_technology":    "AI & Technology",
        "financial_freedom": "Financial Freedom",
        "life_motivation":  "Life & Motivation",
    }

    html_parts = [
        f"<!-- Weekly Digest — {data.get('label',week)} -->",
        f"<p>Every week I read across AI, money, and life — so you don't have to. "
        f"Here are the pieces that made me think this week.</p>",
        "",
    ]

    for topic, articles in results.items():
        topic_html = [f"<h2>{topic_labels.get(topic, topic)}</h2>", ""]
        has_items = False
        for a in articles[:3]:
            url  = a.get("url","")
            edit = edits.get(url, {})
            if edit.get("status") == "skip":
                continue
            has_items = True
            take = edit.get("kabirs_take","").strip()
            topic_html.append(f'<h3><a href="{url}" target="_blank" rel="noopener">{a.get("title","")}</a></h3>')
            topic_html.append(f'<p><em>Source: {a.get("source","")}</em></p>')
            if a.get("summary"):
                topic_html.append(f'<p>{a.get("summary","")}…</p>')
            if take:
                topic_html.append(f'<blockquote><strong>Kabir&rsquo;s take:</strong> {take}</blockquote>')
            topic_html.append(f'<p><a href="{url}" target="_blank" rel="noopener">Read the full article →</a></p>')
            topic_html.append("")
        if has_items:
            html_parts.extend(topic_html)

    html_parts += [
        "<hr>",
        "<h2>Why I Curate This</h2>",
        "<p>The internet has too much content. Most of it isn't worth your time. "
        "Every week I read across AI, money, and life so you don't have to. "
        "These are the pieces that made me think, taught me something, or changed how I see something.</p>",
        "<p>If something here was useful, share it with one person who'd benefit.</p>",
        "<p><em>→ Want this in your inbox every week? Subscribe below.</em></p>",
        "",
        "<p><strong>Tags:</strong> weekly-digest, AI, financial-freedom, personal-growth, curated</p>",
    ]

    html = "\n".join(html_parts)

    # Save to digests folder as well
    out_file = DIGESTS_DIR / f"wp-html-{week}.html"
    out_file.write_text(html)

    return {"html": html, "saved_to": str(out_file)}


@app.post("/api/digest/fetch")
def fetch_digest():
    """Trigger content_curator.py --fetch as subprocess."""
    if not CURATOR_PY.exists():
        raise HTTPException(404, f"content_curator.py not found at {CURATOR_PY}")
    try:
        result = subprocess.run(
            ["python3", str(CURATOR_PY), "--fetch"],
            capture_output=True, text=True, timeout=120,
            cwd=str(CURATOR_PY.parent)
        )
        return {
            "ok":     result.returncode == 0,
            "stdout": result.stdout[-3000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "Fetch timed out after 120s"}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}


# ══════════════════════════════════════════════════════════════════════════════
#  Sources — read/write marketing/sources.json
# ══════════════════════════════════════════════════════════════════════════════

def _load_sources():
    if not SOURCES_FILE.exists():
        return {}
    return json.loads(SOURCES_FILE.read_text())


def _save_sources(data):
    SOURCES_FILE.write_text(json.dumps(data, indent=2))


def _flatten_sources(data):
    """Return a flat list of all sources with topic + kind fields."""
    flat = []
    for topic, topic_data in data.get("topics", {}).items():
        for s in topic_data.get("sources", []):
            flat.append({**s, "topic": topic, "kind": "blog",
                         "active": s.get("active", True)})
        for s in topic_data.get("youtube_channels", []):
            flat.append({**s, "topic": topic, "kind": "youtube",
                         "active": s.get("active", True)})
    return flat


@app.get("/api/sources")
def get_sources():
    data = _load_sources()
    flat = _flatten_sources(data)
    return flat


@app.put("/api/sources/{name:path}")
def update_source(name: str, body: SourceUpdate):
    data = _load_sources()
    updated = False
    for topic, topic_data in data.get("topics", {}).items():
        for lst_key in ("sources", "youtube_channels"):
            for s in topic_data.get(lst_key, []):
                if s.get("name") == name:
                    if body.active is not None:
                        s["active"] = body.active
                    if body.authority is not None:
                        s["authority"] = body.authority
                    if body.notes is not None:
                        s["notes"] = body.notes
                    updated = True
    if not updated:
        raise HTTPException(404, f"Source '{name}' not found")
    _save_sources(data)
    return {"ok": True}


@app.post("/api/sources")
def add_source(body: SourceCreate):
    data = _load_sources()
    topic_data = data.setdefault("topics", {}).setdefault(body.topic, {
        "keywords": [], "sources": [], "youtube_channels": []
    })
    lst_key = "youtube_channels" if body.source_type == "youtube" else "sources"
    # Check for duplicate
    for s in topic_data.get(lst_key, []):
        if s.get("name") == body.name:
            raise HTTPException(409, f"Source '{body.name}' already exists")
    new_source = {
        "name":      body.name,
        "rss":       body.rss,
        "authority": body.authority,
        "type":      body.source_type,
        "notes":     body.notes or "",
        "active":    True,
    }
    topic_data.setdefault(lst_key, []).append(new_source)
    _save_sources(data)
    return {"ok": True, **new_source, "topic": body.topic}


@app.delete("/api/sources/{name:path}")
def delete_source(name: str):
    data = _load_sources()
    deleted = False
    for topic, topic_data in data.get("topics", {}).items():
        for lst_key in ("sources", "youtube_channels"):
            before = len(topic_data.get(lst_key, []))
            topic_data[lst_key] = [s for s in topic_data.get(lst_key, []) if s.get("name") != name]
            if len(topic_data.get(lst_key, [])) < before:
                deleted = True
    if not deleted:
        raise HTTPException(404, f"Source '{name}' not found")
    _save_sources(data)
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════════════
#  Serve frontend
# ══════════════════════════════════════════════════════════════════════════════

app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse(str(STATIC / "index.html"))


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    init_db()
    print("\n🌿 money-and-mode Dashboard")
    print("   http://localhost:8765\n")
    uvicorn.run("app:app", host="127.0.0.1", port=8765, reload=True)
