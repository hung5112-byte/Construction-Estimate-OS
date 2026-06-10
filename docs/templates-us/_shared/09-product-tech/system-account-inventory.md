### PROMPT 10: System Account Inventory

#### Description
An inventory of all system, software, and SaaS accounts the company uses — owner, access rights, review cycle. **DO NOT STORE PASSWORDS** — only track who has access to what, and where. For audit, offboarding, and access review.

#### Information to collect (ask the user before generating)
1. How many systems/SaaS in use?
2. Centralized management (SSO/IAM)?
3. Grant/revoke process at onboarding/offboarding?
4. Access-review frequency? (monthly / quarterly / on change)
5. Any shared accounts / service accounts?
6. Password manager in use? (1Password, Bitwarden, LastPass...)

#### Suggested template
Structure:
- **Part 1** — Overview: # systems, total users, SSO coverage
- **Part 2** — Account inventory: master table — System | URL | Owner | Admin | Users | Auth method | SSO | MFA | Review date
- **Part 3** — Access matrix: User × System → role/permission level
- **Part 4** — Service accounts: non-personal accounts — purpose, owner, rotation schedule
- **Part 5** — Onboarding checklist: systems to provision per role
- **Part 6** — Offboarding checklist: systems to revoke
- **Part 7** — Access-review process: frequency, process, sign-off
- **Appendix**: access-request form, access-review report template

Confirm the structure before generating.

#### File-generation prompt
```
Create a System Account Inventory.

CONTEXT:
- Company: [Name] — # systems: [number] — Headcount: [number]
- SSO: [Yes/No] — Provider: [name]
- Password Manager: [name]
- Access review: [frequency]

FORMAT:
- Summary dashboard: Total systems | SSO-enabled | MFA-enabled | Shared accounts | Last full review
- Master inventory: System | URL | Category | Owner | # Users | Auth | SSO ☐ | MFA ☐ | License type | Cost | Renewal (USD)
- Access matrix: table User × System → Role (Admin/Editor/Viewer/None)
- Service accounts: Account | System | Purpose | Owner | Rotation | Last rotated
- Onboarding per role: Role | Systems to provision | Access level | Provisioned by
- Offboarding checklist: System | Action | Verified by | Date ☐
- Review log: System | Review date | Reviewer | Changes made | Next review

⚠️ SECURITY: do NOT include passwords, API keys, or secrets in this file.

TONE: Inventory, compliance-ready, structured.
LENGTH: 4-6 pages.
```

---
✍️ Author: Brian H. Doan
