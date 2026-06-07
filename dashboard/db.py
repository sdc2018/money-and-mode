"""
Database layer — SQLite via raw SQL.
All tables live in dashboard/data/dashboard.db
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "dashboard.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with get_conn() as conn:
        conn.executescript("""
        -- ─── Articles ───────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS articles (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            wp_post_id   INTEGER,
            title        TEXT NOT NULL,
            slug         TEXT,
            category     TEXT,
            keyword      TEXT,
            series       TEXT,            -- 'ai-everyday' | 'financial-freedom' | 'life'
            status       TEXT DEFAULT 'planned',
                                          -- planned | written | draft | published
            wp_url       TEXT,
            publish_date TEXT,            -- ISO YYYY-MM-DD
            notes        TEXT,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        -- ─── Social Posts ────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS social_posts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id   INTEGER REFERENCES articles(id),
            platform     TEXT NOT NULL,   -- instagram | twitter | facebook | pinterest
            caption      TEXT,
            image_url    TEXT,
            status       TEXT DEFAULT 'pending',
                                          -- pending | posted | skipped
            posted_date  TEXT,
            notes        TEXT,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        -- ─── Performance Metrics ─────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS metrics (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            social_post_id  INTEGER REFERENCES social_posts(id),
            platform        TEXT,
            likes           INTEGER,
            comments        INTEGER,
            saves           INTEGER,
            shares          INTEGER,
            reach           INTEGER,
            impressions     INTEGER,
            link_clicks     INTEGER,
            recorded_date   TEXT DEFAULT (date('now'))
        );

        -- ─── Todos ───────────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS todos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            title        TEXT NOT NULL,
            category     TEXT DEFAULT 'general',
                                          -- content | social | seo | technical | general
            priority     TEXT DEFAULT 'medium',
                                          -- high | medium | low
            status       TEXT DEFAULT 'pending',
                                          -- pending | in_progress | done
            due_date     TEXT,
            notes        TEXT,
            created_at   TEXT DEFAULT (datetime('now')),
            completed_at TEXT
        );

        -- ─── Monthly Traffic ─────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS traffic (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            month            TEXT UNIQUE,  -- YYYY-MM
            total_visitors   INTEGER,
            real_humans_est  INTEGER,
            top_source       TEXT,
            new_articles     INTEGER,
            adsense_revenue  REAL DEFAULT 0,
            notes            TEXT
        );

        -- ─── Weekly Digest Items ─────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS digest_items (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            week            TEXT,          -- YYYY-WNN
            topic           TEXT,          -- ai_technology | financial_freedom | life_motivation
            title           TEXT,
            url             TEXT,
            source          TEXT,
            kabirs_take     TEXT,
            content_type    TEXT DEFAULT 'article',   -- article | video
            status          TEXT DEFAULT 'curated',   -- curated | published | skipped
            published_date  TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        );

        -- ─── Indexes ─────────────────────────────────────────────────────────────
        -- ─── Keywords ────────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS keywords (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword              TEXT NOT NULL,
            article_id           INTEGER REFERENCES articles(id),
            target_url           TEXT,
            monthly_searches_est INTEGER,
            competition          TEXT DEFAULT 'unknown',  -- low | medium | high | unknown
            notes                TEXT,
            created_at           TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS keyword_rankings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_id    INTEGER REFERENCES keywords(id),
            rank          INTEGER,          -- Google position (null = not ranking yet)
            recorded_date TEXT DEFAULT (date('now')),
            notes         TEXT
        );

        -- ─── Indexes ─────────────────────────────────────────────────────────────
        CREATE INDEX IF NOT EXISTS idx_articles_status      ON articles(status);
        CREATE INDEX IF NOT EXISTS idx_social_posts_status  ON social_posts(status);
        CREATE INDEX IF NOT EXISTS idx_todos_status         ON todos(status);
        CREATE INDEX IF NOT EXISTS idx_traffic_month        ON traffic(month);
        CREATE INDEX IF NOT EXISTS idx_kw_rankings_kw       ON keyword_rankings(keyword_id);
        """)
    print(f"✅ Database ready: {DB_PATH}")
