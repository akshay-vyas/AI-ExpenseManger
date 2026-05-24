# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (activate venv first)
pip install -r requirements.txt

# Run the development server (http://localhost:5008)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_foo.py
```

## Architecture

**Spendly** is a Flask expense-tracking web app backed by SQLite. The stack is intentionally minimal: no ORM, no JS framework — raw SQL, Jinja2 templates, and vanilla JS.

### Key files

- `app.py` — Flask application and all route definitions. Currently has live routes for `/`, `/register`, `/login`, `/terms`, `/privacy` plus stub routes for `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.
- `database/db.py` — Database layer. Must expose three functions: `get_db()` (returns a SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables), and `seed_db()` (inserts sample data).
- `templates/base.html` — Master layout. All other templates extend it via `{% extends "base.html" %}` and fill `{% block title %}`, `{% block content %}`, and optionally `{% block head %}` / `{% block scripts %}`.
- `static/css/style.css` — Single global stylesheet (DM Sans + DM Serif Display fonts from Google Fonts).
- `static/js/main.js` — Vanilla JavaScript entry point, loaded on every page.

### Request flow

Browser → Flask route in `app.py` → optional DB call via `database/db.py` → `render_template(...)` → Jinja2 template extending `base.html`.

### Auth pattern (to be implemented)

Sessions will use Flask's built-in `session` dict (cookie-based). `app.secret_key` must be set before session writes work. Password hashing belongs in `database/db.py` or a thin helper — Werkzeug's `generate_password_hash` / `check_password_hash` is already available in the dependency tree.

### Database conventions

- SQLite file lives at a path returned/managed by `get_db()`.
- All connections should set `conn.row_factory = sqlite3.Row` so columns are accessible by name.
- Enable foreign keys per-connection: `conn.execute("PRAGMA foreign_keys = ON")`.
