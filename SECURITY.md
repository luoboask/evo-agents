# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of evo-agents seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email or create a draft security advisory on GitHub.

### Reporting Process

1. **Report:** Send an email with details about the vulnerability
2. **Response:** We will acknowledge receipt within 48 hours
3. **Assessment:** We will investigate and respond with our assessment
4. **Resolution:** We will work on a fix and notify you

### What to Include

* Type of issue (e.g., buffer overflow, SQL injection, etc.)
* Full paths of source file(s) related to the issue
* Location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

### Preferred Languages

We prefer all communications to be in English or Chinese.

## Security Best Practices

### For Users

1. **Keep OpenClaw Updated** - Always use the latest version of OpenClaw
2. **Review Scripts** - Review scripts before running them
3. **Secure Your Workspace** - Keep your workspace directory private
4. **Don't Commit Secrets** - Use `.gitignore` to exclude sensitive files
5. **Use Private Repos** - If storing sensitive data, use private Git repos

### For Contributors

1. **No Secrets in Code** - Never commit API keys, passwords, or tokens
2. **Review Dependencies** - Check security of any added dependencies
3. **Follow Security Guidelines** - Follow our security best practices
4. **Report Issues** - Report any security concerns immediately

## Known Security Considerations

### Workspace Security

* The workspace is the default working directory, not a hard sandbox
* Tools resolve relative paths against the workspace
* Absolute paths can reach other host locations unless sandboxing is enabled
* Enable sandboxing for additional isolation if needed

### Data Security

* Memory files may contain sensitive information
* SQLite databases should be protected
* Don't commit memory files to public repositories
* Use `.gitignore` to exclude sensitive data

### Agent Security

* Each agent has access to its workspace
* Agents can execute commands if permitted
* Review agent configurations carefully
* Use agent-specific tool restrictions when needed

## Security Updates

We will notify users of security updates through:

* GitHub Security Advisories
* Release notes in CHANGELOG.md
* Twitter announcements (if critical)

## Acknowledgments

We would like to thank the following for their contributions to our security:

* All security researchers who report vulnerabilities
* The OpenClaw community for security guidance
* Contributors who help fix security issues

## Contact

For security-related questions, please contact us through GitHub or email.

---

**Last Updated:** 2026-03-26
