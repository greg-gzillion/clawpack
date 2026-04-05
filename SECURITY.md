\# Security Policy



\## Supported Versions



| Version | Supported |

|---------|-----------|

| 3.x     | ✅ Current |

| 2.x     | ⚠️ Limited |

| < 2.0   | ❌ End of life |



\## Reporting a Vulnerability



We take security seriously. If you discover a security vulnerability within Clawpack, please follow these steps:



\### Private Reporting (Preferred)

1\. \*\*Do NOT\*\* create a public GitHub issue

2\. Email: \*\*security@clawpack.dev\*\* (or use GitHub's private vulnerability reporting when enabled)

3\. Include as much information as possible:

&#x20;  - Affected versions

&#x20;  - Steps to reproduce

&#x20;  - Potential impact

&#x20;  - Suggested fix (if any)



\### What to Expect

\- \*\*Initial Response\*\*: Within 48 hours

\- \*\*Status Update\*\*: Every 5-7 days until resolved

\- \*\*Fix Timeline\*\*: 

&#x20; - Critical: 7 days

&#x20; - High: 14 days

&#x20; - Medium/Low: Next release



\### Disclosure Policy

\- We will coordinate disclosure with reporters

\- Public disclosure after fix is released

\- Credit given to reporters (unless anonymity requested)



\## Security Best Practices for Clawpack Users



\### API Keys

```bash

\# NEVER hardcode API keys in agent files

\# Use environment variables instead

export OPENROUTER\_API\_KEY="your-key-here"



\# Or use a .env file (excluded from git)

echo "OPENROUTER\_API\_KEY=your-key-here" > .env





\# Security Policy



\## Supported Versions



| Version | Supported |

|---------|-----------|

| 3.x     | ✅ Current |

| 2.x     | ⚠️ Limited |

| < 2.0   | ❌ End of life |



\## Reporting a Vulnerability



We take security seriously. If you discover a security vulnerability within Clawpack, please follow these steps:



\### Private Reporting (Preferred)

1\. \*\*Do NOT\*\* create a public GitHub issue

2\. Email: \*\*security@clawpack.dev\*\* (or use GitHub's private vulnerability reporting when enabled)

3\. Include as much information as possible:

&#x20;  - Affected versions

&#x20;  - Steps to reproduce

&#x20;  - Potential impact

&#x20;  - Suggested fix (if any)



\### What to Expect

\- \*\*Initial Response\*\*: Within 48 hours

\- \*\*Status Update\*\*: Every 5-7 days until resolved

\- \*\*Fix Timeline\*\*: 

&#x20; - Critical: 7 days

&#x20; - High: 14 days

&#x20; - Medium/Low: Next release



\### Disclosure Policy

\- We will coordinate disclosure with reporters

\- Public disclosure after fix is released

\- Credit given to reporters (unless anonymity requested)



\## Security Best Practices for Clawpack Users



\### API Keys

```bash

\# NEVER hardcode API keys in agent files

\# Use environment variables instead

export OPENROUTER\_API\_KEY="your-key-here"



\# Or use a .env file (excluded from git)

echo "OPENROUTER\_API\_KEY=your-key-here" > .env

Database Security

bash

\# Shared memory database location

\~/.claw\_memory/shared\_memory.db



\# Ensure proper permissions

chmod 600 \~/.claw\_memory/shared\_memory.db

Running Agents

Never run as root/admin



Use dedicated user account for automation



Review API calls before executing



Known Security Considerations

API Dependencies

Clawpack uses OpenRouter.ai for AI queries



All API calls are over HTTPS



No user data is stored permanently



Local Database

SQLite database stores cached responses



No encryption by default (add your own if needed)



Backup files should be encrypted



Code Execution

Agents only execute Python code



No arbitrary command execution



All file operations are contained to \~/.claw\_memory/



Reporting Format

markdown

\*\*Vulnerability Title\*\*: \[Brief description]



\*\*Affected Versions\*\*: \[e.g., 3.0.0]



\*\*Description\*\*: 

\[Detailed explanation]



\*\*Steps to Reproduce\*\*:

1\. ...

2\. ...



\*\*Potential Impact\*\*:

\[What could an attacker do?]



\*\*Suggested Fix\*\*:

\[If you have one]



\*\*Additional Context\*\*:

\[Logs, screenshots, etc.]

Responsible Disclosure

We follow coordinated vulnerability disclosure principles. Reporters who follow these guidelines will receive:



Public acknowledgment



Potential bounty (for critical findings)



Our gratitude 🙏



Contact

Security Team: security@clawpack.dev



PGP Key: \[Available upon request]



Emergency: \[GitHub private vulnerability reporting]



Last Updated: April 2026





\### 2. \*\*ENABLE PRIVATE VULNERABILITY REPORTING\*\*



Go to your repository Settings → Security → Vulnerability reporting:

\- Click "Enable" under "Private vulnerability reporting"



\### 3. \*\*SET UP DEPENDABOT ALERTS\*\*



Create a Dependabot configuration:



```powershell

\# Create .github/dependabot.yml

New-Item -Path ".github" -ItemType Directory -Force

notepad .github/dependabot.yml

Copy this content:



yaml

version: 2

updates:

&#x20; # Python dependencies

&#x20; - package-ecosystem: "pip"

&#x20;   directory: "/"

&#x20;   schedule:

&#x20;     interval: "weekly"

&#x20;     day: "monday"

&#x20;   open-pull-requests-limit: 10

&#x20;   labels:

&#x20;     - "dependencies"

&#x20;     - "security"

&#x20;   commit-message:

&#x20;     prefix: "deps"

&#x20;     include: "scope"

&#x20;   reviewers:

&#x20;     - "greg-gzillion"



&#x20; # GitHub Actions

&#x20; - package-ecosystem: "github-actions"

&#x20;   directory: "/"

&#x20;   schedule:

&#x20;     interval: "weekly"

&#x20;   labels:

&#x20;     - "dependencies"

&#x20;     - "ci-cd"

4\. CONFIGURE CODE SCANNING

Create a CodeQL workflow:



powershell

\# Create .github/workflows/codeql.yml

New-Item -Path ".github/workflows" -ItemType Directory -Force

notepad .github/workflows/codeql.yml

Copy this content:



yaml

name: "CodeQL Security Scan"



on:

&#x20; push:

&#x20;   branches: \[ "main" ]

&#x20; pull\_request:

&#x20;   branches: \[ "main" ]

&#x20; schedule:

&#x20;   - cron: '0 0 \* \* 0'  # Weekly on Sunday



jobs:

&#x20; analyze:

&#x20;   name: Analyze

&#x20;   runs-on: ubuntu-latest

&#x20;   permissions:

&#x20;     security-events: write

&#x20;     actions: read

&#x20;     contents: read



&#x20;   strategy:

&#x20;     fail-fast: false

&#x20;     matrix:

&#x20;       language: \[ 'python' ]



&#x20;   steps:

&#x20;   - name: Checkout repository

&#x20;     uses: actions/checkout@v4



&#x20;   - name: Initialize CodeQL

&#x20;     uses: github/codeql-action/init@v3

&#x20;     with:

&#x20;       languages: ${{ matrix.language }}



&#x20;   - name: Autobuild

&#x20;     uses: github/codeql-action/autobuild@v3



&#x20;   - name: Perform CodeQL Analysis

&#x20;     uses: github/codeql-action/analyze@v3

&#x20;     with:

&#x20;       category: "/language:${{matrix.language}}"

5\. SCAN FOR EXISTING SECRETS

powershell

\# Check if any API keys are accidentally committed

git log --all --grep="sk-or-v1" --oneline

git grep -n "sk-or-v1"

6\. CREATE .ENV EXAMPLE

powershell

\# Create .env.example

notepad .env.example

bash

\# Clawpack Environment Variables

\# Copy this to .env and add your actual keys



\# OpenRouter API Key (required)

\# Get from: https://openrouter.ai/keys

OPENROUTER\_API\_KEY=sk-or-v1-your-key-here



\# Database Path (optional)

CLAW\_MEMORY\_PATH=\~/.claw\_memory



\# Logging Level (optional)

LOG\_LEVEL=INFO



\# API Timeout (seconds)

API\_TIMEOUT=60

7\. UPDATE .GITIGNORE

powershell

\# Add to .gitignore

notepad .gitignore

Add these lines:



gitignore

\# Environment variables

.env

.env.local

.env.\*.local



\# Secrets

\*\_key.py

\*\_secret.py

\*\*/secrets.py



\# Security files

\*.pem

\*.key

\*.crt

