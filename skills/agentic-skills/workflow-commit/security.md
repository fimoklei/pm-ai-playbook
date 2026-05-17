# Security

## Pre-Commit Checklist

- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitized HTML)
- [ ] CSRF protection enabled
- [ ] Auth/authz verified
- [ ] Rate limiting on all endpoints
- [ ] Error messages don't leak internals

## Secrets

Use environment variables. Never hardcode. Throw on missing required secrets.

## Response Protocol

If security issue found: STOP -> use **security-reviewer** agent -> fix critical issues -> rotate exposed secrets -> review codebase for similar issues.

## Dependencies

- Check last release date and open issues before adding.
- Unmaintained >1 year: flag and discuss alternatives.
- <20 lines logic: implement yourself.
