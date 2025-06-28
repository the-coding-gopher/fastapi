# FastAPI Development Scripts

This directory contains various scripts for development, documentation building, translation management, and project maintenance.

## Overview

These scripts automate common development tasks for the FastAPI project, including documentation generation, translation workflows, contributor management, and code quality checks.

## Key Scripts

### `docs.py`
Comprehensive documentation build system for multi-language documentation.

**Key Features:**
- Build documentation for multiple languages
- Generate README from main documentation
- Manage translation workflows
- Serve documentation locally with live reload
- Verify documentation consistency

**Common Commands:**
```bash
# Build all language documentation
python scripts/docs.py build-all

# Serve documentation locally
python scripts/docs.py live en

# Generate README from docs
python scripts/docs.py generate-readme

# Verify documentation consistency
python scripts/docs.py verify-docs
```

### `contributors.py`
Automated contributor and translator tracking system.

**Features:**
- Fetches contributor data from GitHub API
- Tracks pull request authors and reviewers
- Generates contributor statistics
- Updates contributor data files automatically
- Creates automated PRs for contributor updates

**Usage:**
Requires GitHub token and repository configuration. Typically run in CI/CD pipelines.

### `translate.py`
AI-powered translation system for documentation.

**Features:**
- Translates documentation using AI (GPT-4)
- Maintains translation consistency
- Handles technical terms appropriately
- Preserves code snippets and formatting
- Updates existing translations

**Usage:**
```bash
# Translate a specific file
python scripts/translate.py --lang es --path docs/en/docs/tutorial/index.md

# Translate all missing files for a language
python scripts/translate.py --lang es
```

### Shell Scripts

#### `format.sh`
Code formatting using Ruff formatter.

#### `lint.sh`
Code linting and style checking.

#### `test.sh`
Run the test suite.

#### `test-cov-html.sh`
Run tests with HTML coverage report.

### Other Utilities

#### `people.py`
Manages FastAPI people and community data.

#### `sponsors.py`
Handles sponsor information and display.

#### `topic_repos.py`
Manages topic-related repository information.

#### `label_approved.py`
Automated labeling for approved pull requests.

#### `deploy_docs_status.py`
Manages documentation deployment status.

#### `notify_translations.py`
Notification system for translation updates.

#### `mkdocs_hooks.py`
Custom hooks for MkDocs documentation building.

#### `playwright/`
End-to-end testing utilities using Playwright.

## Prerequisites

Most scripts require:
- Python 3.8+
- Required dependencies (install with `pip install -r requirements-docs.txt`)
- For some scripts: GitHub token, OpenAI API key, or other credentials

## Development Workflow

1. **Documentation Changes**: Use `docs.py live` for local development
2. **Code Changes**: Run `lint.sh` and `test.sh` before committing
3. **Translation Updates**: Use `translate.py` for new translations
4. **Release Preparation**: Run `docs.py verify-docs` to ensure consistency

## CI/CD Integration

Many of these scripts are integrated into GitHub Actions workflows for:
- Automated testing and linting
- Documentation building and deployment
- Translation management
- Contributor tracking
- Release automation

## Learn More

For specific script usage and configuration options, run:
```bash
python scripts/{script_name}.py --help
```

Or refer to the individual script files for detailed documentation and examples.
