"""
money-and-mode Dashboard — FastAPI backend
Run: python app.py
Opens: http://localhost:8765
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from pathlib import Path
import uvicorn

from db import get_conn, init_db

app = FastAPI(title="money-and-mode Dashboard", version="1.0")

STATIC = Path(__file__).parent / "static"


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
            SELECT a.title, a.series, sp.platform, sp.posted_date,
                   m.likes, m.comments, m.saves, m.reach, m.link_clicks
            FROM metrics m
            JOIN social_posts sp ON sp.id = m.social_post_id
            JOIN articles a      ON a.id  = sp.article_id
            ORDER BY sp.posted_date DESC
        """).fetchall()
        # Top performers by saves
        top_saves = conn.execute("""
            SELECT a.title, SUM(m.saves) total_saves, SUM(m.reach) total_reach
            FROM metrics m
            JOIN social_posts sp ON sp.id = m.social_post_id
            JOIN articles a      ON a.id  = sp.article_id
            WHERE m.saves IS NOT NULL
            GROUP BY a.id ORDER BY total_saves DESC LIMIT 5
        """).fetchall()
    return {
        "posts":      [dict(r) for r in rows],
        "top_saves":  [dict(r) for r in top_saves],
    }


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
