# Releasing

Guidance for **maintainers** when publishing versions (Git tags, PyPI, etc.).

## Versioning

- Use **Semantic Versioning** (`MAJOR.MINOR.PATCH`) for published Python packages when you ship to PyPI.
- The **web app** and **API** in this monorepo may share the same tag or be versioned separately; document whichever approach you choose in the release notes.

## Checklist

1. Ensure **`main`** (or the release branch) passes **CI**.
2. Update **[CHANGELOG.md](CHANGELOG.md)** — move items from `[Unreleased]` into a dated section with the new version.
3. **Tag** the repository:

   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

4. **PyPI** (if applicable): build and upload from `backend/` per your packaging workflow (`python -m build`, `twine upload`, or CI).
5. **GitHub Release**: create a release from the tag and paste the changelog section for that version.

## Optional: CODEOWNERS

To auto-request reviews, add `.github/CODEOWNERS` (see [.github/CODEOWNERS.example](.github/CODEOWNERS.example)). GitHub requires real `@username` or `@org/team` entries.
