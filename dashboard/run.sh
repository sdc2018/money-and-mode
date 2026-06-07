#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# money-and-mode Dashboard — one-click start
# Run: bash dashboard/run.sh
# Opens: http://localhost:8765
# ─────────────────────────────────────────────────────────────────

cd "$(dirname "$0")"

echo ""
echo "🌿 money-and-mode Dashboard"
echo "───────────────────────────"

# Install deps if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "📦 Installing dependencies..."
  pip3 install -r requirements.txt --quiet
fi

# Init DB + seed data if first run
if [ ! -f "data/dashboard.db" ]; then
  echo "🌱 First run — seeding database..."
  python3 seed.py
fi

echo "🚀 Starting server at http://localhost:8765"
echo "   Press Ctrl+C to stop"
echo ""

# Open browser after 1 second
(sleep 1 && open "http://localhost:8765") &

python3 app.py
