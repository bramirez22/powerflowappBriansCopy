# GitHub Setup Checklist

Use this once after pushing the repo to GitHub.

## 1. Repository Settings

- Visibility: private (unless instructor requires public).
- Default branch: `main`.
- Enable auto-delete head branches after merge.

## 2. Branch Protection (`main`)

Enable a ruleset/branch rule requiring:

- Pull request before merge.
- At least 1 approval.
- Dismiss stale approvals on new commits.
- Require status checks to pass (CI).
- Block force pushes and deletions.

## 3. Labels (recommended)

Create labels:

- `milestone:M0`
- `milestone:M1`
- `milestone:M2`
- `milestone:M3`
- `milestone:M4`
- `milestone:M5`
- `milestone:Final`
- `solver:GS`
- `solver:NR`
- `fault-analysis`
- `ui`
- `validation`
- `docs`

## 4. Milestones in GitHub

Create milestones in GitHub with due weeks:

- M0 (Week 7)
- M1 (Week 8)
- M2 (Week 9)
- M3 (Week 11)
- M4 (Week 12)
- M5 (Week 14)
- Final (Week 15)

## 5. CODEOWNERS

Update `CODEOWNERS` with actual GitHub usernames/team so PR reviews are auto-requested.

## 6. Issue and PR Discipline

- Every PR links an issue.
- Every issue is assigned to a milestone and owner.
- Every merged PR updates relevant checklist(s) in `docs/milestones/`.
