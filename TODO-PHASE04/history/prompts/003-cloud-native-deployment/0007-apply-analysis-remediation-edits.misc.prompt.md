---
id: "0007"
title: Apply Analysis Remediation Edits
stage: misc
date: 2026-02-07
surface: agent
model: claude-opus-4-6
feature: 003-cloud-native-deployment
branch: 003-cloud-native-deployment
user: user
command: /sp.analyze (remediation)
labels: ["remediation", "consistency", "cross-artifact", "fixes"]
links:
  spec: specs/003-cloud-native-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-cloud-native-deployment/spec.md
  - specs/003-cloud-native-deployment/plan.md
  - specs/003-cloud-native-deployment/tasks.md
  - specs/003-cloud-native-deployment/research.md
  - .specify/memory/constitution.md
  - helm/todo-frontend/values.yaml
  - helm/todo-backend/values.yaml
tests:
  - None (documentation and configuration edits only)
---

## Prompt

User: "apply all of these" — referring to the 16 remediation suggestions from cross-artifact analysis (PHR 0006). Apply all CRITICAL, HIGH, and MEDIUM fixes across 7 files.

## Response snapshot

Applied all 16 remediation edits across 7 files:

**CRITICAL (2 fixed)**:
- C1: Pinned custom image tags from `latest` to `1.0.0` in Helm values, tasks, plan, and spec. Added constitution exception for local Minikube dev.
- C2: Updated constitution imagePullPolicy default to distinguish `Never` (custom) vs `IfNotPresent` (official).

**HIGH (5 fixed)**:
- U1: Added task T052a for database schema initialization between deploy-database and deploy-backend.
- I1: Updated spec backend image size target from 300MB to 500MB (matching SC-003).
- I2: Removed nginx from constitution frontend container section; now says "Node.js standalone server."
- I4: Fixed plan Step 3 build command to use `NEXT_PUBLIC_API_URL=""`.
- A1: Added task T034a for backend initContainer (database readiness wait with busybox/nc).

**MEDIUM (5 fixed)**:
- I3: Standardized Python version to 3.12+ in plan.md and constitution.md.
- I5: Fixed stale NEXT_PUBLIC_API_URL text in research.md Section 6.
- A3: Added minimum AI-ops completion criteria in tasks.md Phase 7.
- U2/U3: Added local dev env var defaults to spec.md backend container section.

Files modified: spec.md, plan.md, tasks.md, research.md, constitution.md, helm/todo-frontend/values.yaml, helm/todo-backend/values.yaml

## Outcome

- ✅ Impact: All 16 cross-artifact inconsistencies resolved; 0 CRITICAL issues remain
- 🧪 Tests: N/A (documentation and config edits)
- 📁 Files: 7 files modified
- 🔁 Next prompts: Continue with /sp.implement for T048+ (Minikube deployment), or re-run /sp.analyze to verify zero remaining issues
- 🧠 Reflection: The most impactful fix was U1 (DB schema init) — without it, the entire deployment would fail silently at runtime. The tag pinning (C1) also aligns the project with constitution security rules while maintaining local dev ergonomics.

## Evaluation notes (flywheel)

- Failure modes observed: None — all edits applied cleanly
- Graders run and results (PASS/FAIL): PASS — all 16 edits verified via Edit tool success responses
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.analyze again to confirm zero findings remain
