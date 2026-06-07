"""
Database layer — SQLite via raw SQL.
All tables live in dashboard/data/dashboard.db

Migration system: db_version table tracks applied migrations.
Add new ALTER TABLE changes to MIGRATIONS dict with the next version number.
New tables always go in the executescript block (CREATE TABLE IF NOT EXISTS).
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "dashboard.db"

CURRENT_VERSION = 2

# Only ALTER TABLE / data-fix migrations go here.
# New tables are created in init_db() with IF NOT EXISTS.
MIGRATIONS = {
    1: "ALTER TABLE traffic ADD COLUMN affiliate_revenue REAL DEFAULT 0;",
    2: "ALTER TABLE social_posts ADD COLUMN scheduled_date TEXT;",
}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _get_version(conn):
    try:
        row = conn.execute("SELECT version FROM db_version LIMIT 1").fetchone()
        return row[0] if row else 0
    except Exception:
        return 0


def _set_version(conn, version):
    conn.execute("INSERT OR REPLACE INTO db_version (id, version) VALUES (1, ?)", (version,))


def run_migrations(conn):
    current = _get_version(conn)
    if current >= CURRENT_VERSION:
        return
    for v in sorted(MIGRATIONS):
        if v > current:
            try:
                conn.execute(MIGRATIONS[v])
                print(f"  ✓ Migration {v} applied")
            except Exception as e:
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"  ~ Migration {v} skipped (already applied)")
                else:
                    print(f"  ✗ Migration {v} failed: {e}")
    _set_version(conn, CURRENT_VERSION)
    conn.commit()


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with get_conn() as conn:
        conn.executescript("""
        -- ─── Version tracking ─────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS db_version (
            id      INTEGER PRIMARY KEY DEFAULT 1,
            version INTEGER DEFAULT 0
        );

        -- ─── Articles ─────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS articles (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            wp_post_id   INTEGER,
            title        TEXT NOT NULL,
            slug         TEXT,
            category     TEXT,
            keyword      TEXT,
            series       TEXT,
            status       TEXT DEFAULT 'planned',
            wp_url       TEXT,
            publish_date TEXT,
            notes        TEXT,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        -- ─── Social Posts ─────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS social_posts (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id     INTEGER REFERENCES articles(id),
            platform       TEXT NOT NULL,
            caption        TEXT,
            image_url      TEXT,
            status         TEXT DEFAULT 'pending',
            posted_date    TEXT,
            scheduled_date TEXT,
            notes          TEXT,
            created_at     TEXT DEFAULT (datetime('now'))
        );

        -- ─── Performance Metrics ──────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS metrics (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            social_post_id INTEGER REFERENCES social_posts(id),
            platform       TEXT,
            likes          INTEGER,
            comments       INTEGER,
            saves          INTEGER,
            shares         INTEGER,
            reach          INTEGER,
            impressions    INTEGER,
            link_clicks    INTEGER,
            recorded_date  TEXT DEFAULT (date('now'))
        );

        -- ─── Todos ────────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS todos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            title        TEXT NOT NULL,
            category     TEXT DEFAULT 'general',
            priority     TEXT DEFAULT 'medium',
            status       TEXT DEFAULT 'pending',
            due_date     TEXT,
            notes        TEXT,
            created_at   TEXT DEFAULT (datetime('now')),
            completed_at TEXT
        );

        -- ─── Monthly Traffic ──────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS traffic (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            month             TEXT UNIQUE,
            total_visitors    INTEGER,
            real_humans_est   INTEGER,
            top_source        TEXT,
            new_articles      INTEGER,
            adsense_revenue   REAL DEFAULT 0,
            affiliate_revenue REAL DEFAULT 0,
            notes             TEXT
        );

        -- ─── Digest Edits ─────────────────────────────────────────────────────
        -- Stores Kabir's take + include/skip per item per week.
        -- Survives re-fetches because it keys on (week, url).
        CREATE TABLE IF NOT EXISTS digest_edits (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            week        TEXT NOT NULL,
            url         TEXT NOT NULL,
            kabirs_take TEXT,
            status      TEXT DEFAULT 'include',
            updated_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(week, url)
        );

        -- ─── Settings ─────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS settings (
            key        TEXT PRIMARY KEY,
            value      TEXT,
            label      TEXT,
            category   TEXT DEFAULT 'general',
            updated_at TEXT DEFAULT (datetime('now'))
        );

        -- ─── Keywords ─────────────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS keywords (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword              TEXT NOT NULL,
            article_id           INTEGER REFERENCES articles(id),
            target_url           TEXT,
            monthly_searches_est INTEGER,
            competition          TEXT DEFAULT 'unknown',
            notes                TEXT,
            created_at           TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS keyword_rankings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_id    INTEGER REFERENCES keywords(id),
            rank          INTEGER,
            recorded_date TEXT DEFAULT (date('now')),
            notes         TEXT
        );

        -- ─── Indexes ──────────────────────────────────────────────────────────
        CREATE INDEX IF NOT EXISTS idx_articles_status     ON articles(status);
        CREATE INDEX IF NOT EXISTS idx_social_posts_status ON social_posts(status);
        CREATE INDEX IF NOT EXISTS idx_todos_status        ON todos(status);
        CREATE INDEX IF NOT EXISTS idx_traffic_month       ON traffic(month);
        CREATE INDEX IF NOT EXISTS idx_kw_rankings_kw      ON keyword_rankings(keyword_id);
        CREATE INDEX IF NOT EXISTS idx_digest_edits        ON digest_edits(week, url);
        """)
        run_migrations(conn)
    print(f"✅ Database ready: {DB_PATH}")
