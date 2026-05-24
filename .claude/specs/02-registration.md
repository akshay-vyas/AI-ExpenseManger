# Spec: Registration

## Overview
Implement the user registration and login flows for Spendly. This step wires up the existing `register.html` and `login.html` forms with real POST handlers, stores new users in the database with hashed passwords, and establishes a Flask cookie session on successful auth. It also implements logout and a minimal post-login landing page so users have somewhere to land after authenticating.

## Depends on
Step 01 — Database Setup (users table and `get_db()` must exist).

## Routes
- `POST /register` — validate form input, insert user, set session, redirect to `/dashboard` — public
- `POST /login` — verify credentials, set session, redirect to `/dashboard` — public
- `GET /logout` — clear session, redirect to `/` — logged-in
- `GET /dashboard` — simple logged-in landing page (stub for now) — logged-in

## Database changes
No database changes. The `users` table already has all required columns (`id`, `name`, `email`, `password_hash`, `created_at`).

## Templates
- **Create:** `templates/dashboard.html` — minimal post-login page showing "Welcome, <name>"
- **Modify:** none — `register.html` and `login.html` already have correct form actions and `{% if error %}` blocks

## Files to change
- `app.py` — add `secret_key`; convert `/register` and `/login` to POST handlers; implement `/logout`; add `/dashboard` route

## Files to create
- `templates/dashboard.html`

## New dependencies
No new dependencies. `werkzeug.security` (`check_password_hash`, `generate_password_hash`) is already in the dependency tree.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`; verified with `check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any `session` write
- On duplicate email at registration, re-render `register.html` with `error="An account with that email already exists."`
- On bad credentials at login, re-render `login.html` with `error="Invalid email or password."` (same message for both cases — no user enumeration)
- Session stores only `user_id` (integer) — nothing else
- `/dashboard` and `/logout` must redirect to `/login` if no session exists

## Definition of done
- [ ] `POST /register` with valid data creates a new user row and redirects to `/dashboard`
- [ ] `POST /register` with a duplicate email re-renders the form with an error message
- [ ] `POST /register` with missing fields returns a 400 or re-renders with an error (HTML5 `required` attributes handle client-side; server must also reject)
- [ ] `POST /login` with correct credentials starts a session and redirects to `/dashboard`
- [ ] `POST /login` with wrong password re-renders the form with an error message
- [ ] `POST /login` with unknown email re-renders the form with the same generic error message
- [ ] `/dashboard` shows the logged-in user's name
- [ ] `/dashboard` redirects to `/login` when accessed without a session
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] Refreshing `/dashboard` after logout redirects to `/login`
- [ ] Passwords are never stored in plain text (verify `password_hash` column in DB)
