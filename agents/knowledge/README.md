\# Dependabot configuration for Clawpack

\# Documentation: https://docs.github.com/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file



version: 2

updates:

&#x20; # Python dependencies (pip)

&#x20; - package-ecosystem: "pip"

&#x20;   directory: "/"  # Location of requirements.txt

&#x20;   schedule:

&#x20;     interval: "weekly"

&#x20;     day: "monday"

&#x20;     time: "09:00"

&#x20;     timezone: "America/New\_York"

&#x20;   open-pull-requests-limit: 10

&#x20;   labels:

&#x20;     - "dependencies"

&#x20;     - "python"

&#x20;     - "security"

&#x20;   commit-message:

&#x20;     prefix: "deps"

&#x20;     prefix-development: "deps-dev"

&#x20;     include: "scope"

&#x20;   reviewers:

&#x20;     - "greg-gzillion"  # Your GitHub username

&#x20;   assignees:

&#x20;     - "greg-gzillion"

&#x20;   groups:

&#x20;     # Group security updates together

&#x20;     security-updates:

&#x20;       applies-to: "security-updates"

&#x20;       patterns:

&#x20;         - "\*"

&#x20;       update-types:

&#x20;         - "patch"

&#x20;         - "minor"

&#x20;     # Group production dependencies

&#x20;     production-dependencies:

&#x20;       patterns:

&#x20;         - "requests"

&#x20;         - "sqlite3\*"

&#x20;     # Group development dependencies

&#x20;     development-dependencies:

&#x20;       patterns:

&#x20;         - "pytest\*"

&#x20;         - "black\*"

&#x20;         - "flake8\*"

&#x20;   ignore:

&#x20;     # Ignore major version updates for critical packages (review manually)

&#x20;     - dependency-name: "requests"

&#x20;       update-types: \["version-update:semver-major"]

&#x20;     - dependency-name: "sqlite3"

&#x20;       update-types: \["version-update:semver-major"]



&#x20; # GitHub Actions dependencies

&#x20; - package-ecosystem: "github-actions"

&#x20;   directory: "/"

&#x20;   schedule:

&#x20;     interval: "weekly"

&#x20;     day: "monday"

&#x20;   open-pull-requests-limit: 5

&#x20;   labels:

&#x20;     - "dependencies"

&#x20;     - "github-actions"

&#x20;     - "ci-cd"

&#x20;   commit-message:

&#x20;     prefix: "ci"

&#x20;     include: "scope"

&#x20;   reviewers:

&#x20;     - "greg-gzillion"

&#x20;   groups:

&#x20;     actions-minor-patch:

&#x20;       patterns:

&#x20;         - "\*"

&#x20;       update-types:

&#x20;         - "patch"

&#x20;         - "minor"



&#x20; # Python (for local development environment)

&#x20; - package-ecosystem: "pip"

&#x20;   directory: "/agents/"

&#x20;   schedule:

&#x20;     interval: "weekly"

&#x20;   labels:

&#x20;     - "dependencies"

&#x20;     - "agents"

&#x20;   ignore:

&#x20;     - dependency-name: "\*"

&#x20;       update-types: \["version-update:semver-major"]

