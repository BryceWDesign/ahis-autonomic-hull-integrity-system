# Security Policy (AHIS)

AHIS is an engineering proof-of-concept repository. Some content may include scripts, prototyping firmware notes, or tooling that could be misused if treated as production-grade. This policy defines how to report security-relevant issues responsibly.

## Supported scope
Security reports are in-scope if they involve:
- Unsafe defaults or behaviors in any included scripts/tools that could cause unintended system changes (e.g., destructive file operations).
- Vulnerabilities in any included firmware/driver code intended for PoC instrumentation (e.g., insecure update paths, obvious credential leakage, unsafe network exposure).
- Supply-chain risks discovered in dependencies explicitly required by this repo’s PoC workflow (when a dependency is pinned or recommended here).

Out of scope:
- Hypothetical issues in third-party tools not bundled with this repo.
- General “best practices” suggestions without a concrete risk.
- Any request to weaponize the project or provide instructions for harmful use.

## How to report a vulnerability
**Do not open a public GitHub issue** for suspected vulnerabilities.

Use one of the following:
1) **GitHub Private Vulnerability Reporting / Security Advisories**  
   If this repository has private reporting enabled, submit the report through the repo’s **Security** tab.
2) **Direct contact via GitHub**  
   If private reporting is not enabled, contact the maintainer through the maintainer’s GitHub profile.

When reporting, include:
- A clear description of the issue and impact
- Reproduction steps (minimal PoC if possible)
- Affected file paths / commit hash (if known)
- Suggested fix (if you have one)

## Disclosure expectations
- Please allow a reasonable remediation window before public disclosure.
- If the issue affects only non-production PoC scripts, we may document it as a limitation rather than “patching” behavior that is intentionally explicit for engineering transparency.

## No warranties / no bug bounty
This repository is provided “as is.” There is no bug bounty program.
