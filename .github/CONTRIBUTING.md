# Contribution and release rules

Use a feature branch (`codex/*` or `feature/*`) and open a Pull Request into
`main`. Direct pushes to `main` are disabled in the GitHub repository settings.

Commit messages follow Conventional Commits:

- `fix:` creates a patch release.
- `feat:` creates a minor release.
- `feat!:` or a `BREAKING CHANGE:` footer creates a major release.
- Documentation, tests, chores, and refactors do not create a release by themselves.

The release workflow creates the version tag and GitHub Release after CI passes.
Production deployment still requires approval through the `production` GitHub
Environment.
