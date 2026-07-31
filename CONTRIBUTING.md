# Contributing to ASHA

Thank you for your interest in contributing!

> **Project stage:** Developer preview (v0.4.2). We welcome bug reports, documentation fixes, and focused PRs.

## What we need most right now

| Priority | How you can help |
|----------|------------------|
| **Feedback** | Run `streamlit run examples/showcase/streamlit_app.py` and open an issue |

| **Bug reports** | Repro steps, Python version, optional `[extras]` used |
| **Docs & examples** | Clarify setup, add real-world snippets |
| **Tests** | PII edge cases, adapter smoke tests, AshaFit scenarios |
| **Large features** | Discuss in an issue before a big PR |

We are **not** looking for drive-by refactors or scope creep in preview - keep PRs focused.

## Quick Links

- **Full contributing guide**: [docs/contributing.md](docs/contributing.md)
- **Support policy**: [SUPPORT.md](SUPPORT.md)
- **Security reports**: [SECURITY.md](SECURITY.md) - do not open public issues for vulnerabilities
- **Code of conduct**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Discussions**: https://github.com/AjayRajan05/ASHA/discussions
- **Slack**: https://join.slack.com/t/asha-community/shared_invite/zt-45h11ellh-yY~YG4BL8W~TvxsMXSgPzw

## Getting Started

```bash
git clone https://github.com/AjayRajan05/ASHA.git
cd ASHA
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Requirements

- Python **3.10+**
- Follow existing code style (Black, flake8)
- Add tests for new behavior in `tests/`
- Keep changes focused - one concern per PR

## Pull Request Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] New features include unit tests
- [ ] Documentation updated if API changes
- [ ] CHANGELOG.md updated for user-facing changes
- [ ] No secrets or API keys committed (use `.env.example` only)
- [ ] `python scripts/check_public_surface.py` passes
- [ ] No `training/`, `models/`, `data/`, or `*.joblib` added to this public repo

## Private artifacts (maintainers)

Hardened detector weights and training data live in a **private** store, not this repository.
See [maintainers/PRIVATE_ARTIFACTS.md](maintainers/PRIVATE_ARTIFACTS.md) and
[maintainers/SECRET_ROTATION.md](maintainers/SECRET_ROTATION.md).

## Development Focus Areas

We especially welcome contributions in:

- PII detection accuracy and false-positive reduction
- Security bypass test cases
- Provider adapter compatibility
- Documentation and examples
- Benchmark reproducibility

See [docs/contributing.md](docs/contributing.md) for architecture overview, release process, and detailed guidelines.
