# Security policy

## Supported versions

Security fixes land on the default branch (`main`). Deploy from recent commits.

## Reporting a vulnerability

Do **not** file a public issue for undisclosed security bugs.

Use **GitHub private security advisories** (repository **Security** tab) if enabled, or contact maintainers through a private channel listed on the organization or repo profile.

Include:

- Description and impact  
- Steps to reproduce (if possible)  
- Affected areas (e.g. `backend/` API, `frontend/` app)

## Deployment hardening

- Use a strong `SECRET_KEY` (see [`backend/.env.example`](backend/.env.example)); never ship default secrets.
- Restrict PostgreSQL and Redis to trusted networks; use TLS where appropriate.
- Keep dependencies updated (`pip`, `npm`).
