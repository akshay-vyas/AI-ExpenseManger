# Spec: Login and Logout

## Overview
Step 02 implemented the login, logout, and session flows directly inside each route handler. This step refactors those guards into a reusable `@login_required` decorator and a `before_request` hook that loads the current user into Flask's `g` object on every request. This eliminates the repeated `if "user_id" not in session: redirect(...)` pattern, gives templates a clean `g.user` variable, and makes every future protected route a one-liner. It also adds a `?next=` redirect so users land back on the page they were trying to reach after logging in.

## Depends on
Step 01 — Database Setup, Step 02 — Registration (session and login routes must exist).

## Routes
No new routes. All existing routes remain; `/dashboard` is updated to use `@login_required`.

## Database changes
No database changes.

## Templates
- **Create:** none
- **Modify:**
  - `templates/base.html` — replace `session.get('user_id')` nav check with `g.user`
  - `templates/dashboard.html` — use `g.user` instead of the passed-in `user` template variable (optional cleanup)

## Files to change
- `app.py` — add `before_request` hook, `login_required` decorator, update `/dashboard` and `/login` to handle `?next=`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `login_required` must be implemented as a decorator using `functools.wraps`
- `before_request` loads the user row into `g.user` (or sets `g.user = None`) — never raises exceptions
- The `?next=` value must be validated to be a relative path (starts with `/`) before redirecting — never redirect to an external URL
- `g` is imported from `flask`; `functools` from the standard library

## Definition of done
- [ ] Visiting `/dashboard` without a session redirects to `/login?next=/dashboard`
- [ ] After logging in, the user is redirected to the original `next` URL instead of always going to `/dashboard`
- [ ] `g.user` is available in all templates (verify by printing `{{ g.user['name'] }}` in any template)
- [ ] Nav bar uses `g.user` (not `session.get(...)`) to decide which links to show
- [ ] Any future route decorated with `@login_required` automatically redirects unauthenticated users to login
- [ ] A `?next=` value pointing to an external URL (e.g. `http://evil.com`) is ignored — user lands on `/dashboard` instead
- [ ] Removing `session["user_id"]` manually in the browser causes all protected pages to redirect to login
