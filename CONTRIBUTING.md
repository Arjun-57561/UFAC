# Contributing Guidelines

Welcome to the project! We're glad you're here. Please read the following guidelines before contributing.

---

## 👥 Core Contributors

| GitHub Handle | Name |
|---|---|
| [@Arjun-57561](https://github.com/Arjun-57561) | Arjun Reddy |
| [@Neil-Cardoz](https://github.com/Neil-Cardoz) | Neil Cardoz |
| [@Amitkumarracha](https://github.com/Amitkumarracha) | Amit Kumar Racha |

---

## 🚀 Getting Started

1. **Fork** the repository to your own GitHub account.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/UFAC.git
   cd UFAC
   ```
3. **Add the upstream remote:**
   ```bash
   git remote add upstream https://github.com/<org>/<repo-name>.git
   ```
4. **Install dependencies** as described in the `README.md`.

---

## 🌿 Branching Strategy

- `main` — stable, production-ready code. Direct pushes are **not** allowed.
- `dev` — active development branch. All feature branches should be based off this.
- Feature branches should follow the naming convention:
  ```
  feature/<short-description>
  fix/<short-description>
  chore/<short-description>
  ```

---

## 🔄 Workflow

1. Sync your fork with upstream before starting any work:
   ```bash
   git fetch upstream
   git checkout dev
   git merge upstream/dev
   ```
2. Create a new branch from `dev`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes with clear, atomic commits.
4. Push your branch and open a **Pull Request** against `dev`.

---

## ✅ Pull Request Guidelines

- Provide a clear **title** and **description** of what the PR does.
- Link any related issues using `Closes #<issue-number>`.
- Ensure your branch is up to date with `dev` before requesting review.
- At least **one approval** from a core contributor is required before merging.
- Squash commits where appropriate to keep history clean.

---

## 💬 Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
<type>(optional scope): <short summary>

Examples:
feat(auth): add login with Google
fix(api): handle null response from endpoint
chore: update dependencies
docs: update README with setup steps
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 🐛 Reporting Issues

- Search existing issues before opening a new one.
- Use the provided issue templates where available.
- Include steps to reproduce, expected vs actual behavior, and environment details.

---

## 🤝 Code of Conduct

Be respectful, inclusive, and constructive. We're all here to build something great together.

---

## 🧪 Testing Guidelines

All contributions **must** include appropriate tests. We maintain a high standard of test coverage to keep the codebase reliable.

### Running Tests

```bash
# Run the full test suite
npm test

# Run tests in watch mode
npm run test:watch

# Generate a coverage report
npm run test:coverage
```

### What to Test

- **Unit tests** — cover individual functions and components in isolation.
- **Integration tests** — verify that multiple parts of the system work together correctly.
- **Edge cases** — always test boundary conditions, null/undefined inputs, and error states.

### Guidelines

- Place test files alongside the source file they test, using the `.test.ts` / `.test.js` / `.spec.ts` suffix.
- Each PR should maintain or improve the existing coverage percentage — do not submit PRs that reduce coverage.
- Mock external dependencies (APIs, databases) in unit tests — never rely on live services in the test suite.
- Write descriptive test names that explain **what** is being tested and **what** the expected outcome is:
  ```
  ✅ "should return 404 when user is not found"
  ❌ "test user endpoint"
  ```

---

## 🔒 Security Policy

We take security seriously. Please follow these guidelines to help keep the project and its users safe.

### Supported Versions

Only the latest stable release on `main` receives security patches. Please ensure you are on the latest version before reporting a vulnerability.

### Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please report them responsibly by emailing the core contributors directly or using GitHub's private [Security Advisory](https://docs.github.com/en/code-security/security-advisories) feature:

1. Go to the repository's **Security** tab.
2. Click **"Report a vulnerability"**.
3. Fill in the details — include steps to reproduce, potential impact, and any suggested fixes if you have them.

We aim to acknowledge reports within **48 hours** and provide a fix or mitigation plan within **7 days** for critical issues.

### Security Best Practices for Contributors

- **Never commit secrets** — no API keys, tokens, passwords, or credentials in code or config files. Use environment variables and a `.env.example` template instead.
- Keep dependencies up to date and run `npm audit` (or equivalent) before submitting a PR.
- Avoid using `eval()`, unsafe `innerHTML` assignments, or other patterns that can introduce XSS or injection vulnerabilities.
- Follow the principle of least privilege — request only the permissions your code actually needs.

---

## 📬 Questions?

Reach out to any of the core contributors via GitHub, or open a Discussion in the repository.
