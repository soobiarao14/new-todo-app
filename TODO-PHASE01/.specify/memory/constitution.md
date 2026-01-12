# TODO App Evolution Constitution

<!--
Sync Impact Report:
Version: 1.0.0 (Initial ratification)
Modified Principles: N/A (initial version)
Added Sections: All core sections
Removed Sections: None
Templates Status:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - Requirements align with Phase Governance principles
  ✅ tasks-template.md - Task categorization supports test-first and phase governance
Follow-up TODOs: None
-->

## Core Principles

### I. Specification-Driven Development

All development work MUST originate from approved specifications. No deviation from approved specifications is permitted. Refinement MUST occur only at the specification or planning level, never directly in code. Claude Code MUST be the only entity generating code to ensure consistency and adherence to the specification-driven process.

**Rationale**: Ensures architectural coherence, prevents scope creep, and maintains traceability from requirements to implementation. By centralizing code generation through Claude Code, we eliminate human error and guarantee specification compliance.

### II. Phase Governance

Each phase is strictly scoped by its specification. Features from future phases MUST NEVER appear in earlier phases. Architecture may evolve ONLY through updated specifications and plans, never through ad-hoc implementation changes. Phase I MUST remain simple and isolated from future complexity.

**Rationale**: Prevents premature complexity, maintains clean architectural boundaries, and ensures each phase delivers a stable, testable increment. This enables independent validation and reduces risk of cascading failures.

### III. Technology Constraints

Technology stack is strictly controlled to ensure consistency and compatibility:

- **Backend Language**: Python 3.13+ (REQUIRED)
- **Environment Management**: UV (REQUIRED)
- **Workflow Enforcement**: Spec-Kit Plus (REQUIRED)
- **Code Generation**: Claude Code (EXCLUSIVE - no manual code modification)
- **External Libraries**: Prohibited unless explicitly approved in specifications
- **Future Technologies**: FastAPI, Next.js, databases, agents, etc. are RESERVED for future phases (NOT Phase I)

**Rationale**: Strict technology control reduces onboarding complexity, ensures reproducibility, and prevents dependency conflicts. The beginner-friendly constraint of "no external libraries in Phase I" guarantees the project starts simple and builds complexity incrementally.

### IV. Quality Principles

All code MUST adhere to these non-negotiable quality standards:

- **Clean and Readable Code**: Self-documenting variable names, clear function purposes, consistent formatting
- **Clear Separation of Concerns**: Single responsibility per module, distinct layers for data/logic/presentation
- **Deterministic Behavior**: Same inputs produce same outputs; no hidden state or race conditions
- **Graceful Error Handling**: All error paths handled explicitly; no silent failures; user-friendly error messages
- **Beginner-Friendly Architecture**: Simple patterns, minimal abstraction, clear code flow for learning purposes

**Rationale**: These principles ensure maintainability, debuggability, and accessibility for developers of all skill levels. They form the foundation for a codebase that can evolve without accumulating technical debt.

### V. Test-First Development (NON-NEGOTIABLE)

Test-Driven Development (TDD) is MANDATORY for all implementation work:

1. Tests MUST be written FIRST before any implementation
2. User MUST approve test cases before implementation begins
3. Tests MUST FAIL initially (Red phase)
4. Implementation proceeds ONLY after test failure is confirmed (Green phase)
5. Refactoring occurs ONLY after tests pass (Refactor phase)
6. Red-Green-Refactor cycle is STRICTLY ENFORCED

**Rationale**: TDD guarantees specification compliance, prevents rework, and provides living documentation. Early test approval ensures user intent is captured correctly before development effort is invested.

### VI. Workflow Discipline

Development workflow follows a strict sequence:

1. **Specification Phase**: User requirements captured in spec.md
2. **Planning Phase**: Architecture and design documented in plan.md
3. **Task Generation Phase**: Concrete implementation tasks in tasks.md
4. **Test-First Phase**: Test cases written and approved (Red)
5. **Implementation Phase**: Code written to pass tests (Green)
6. **Refactor Phase**: Code improved while maintaining test passage (Refactor)
7. **Validation Phase**: All acceptance criteria verified

Each phase MUST complete before the next begins. No backtracking or parallel workflow deviations permitted.

**Rationale**: Sequential workflow prevents context switching, reduces errors, and ensures complete thought process at each stage. It also creates clear checkpoints for validation and course correction.

## Development Constraints

### External Dependencies

- Phase I projects MUST NOT include external libraries beyond Python standard library
- Future phases MAY introduce dependencies ONLY after explicit specification approval
- All dependencies MUST be version-pinned for reproducibility
- Dependency rationale MUST be documented in the specification

### Code Ownership

- Claude Code is the EXCLUSIVE code generator
- Human developers MAY write specifications, plans, and tests
- Human developers MUST NOT write implementation code directly
- All code changes MUST flow through the specification → plan → tasks → Claude Code pipeline

### Architectural Evolution

- Architecture changes MUST be proposed at the specification level
- Plan.md MUST reflect architectural decisions with rationale and trade-offs
- Implementation MUST strictly follow the approved plan
- Architectural experiments or explorations are PROHIBITED during implementation

## Governance

### Amendment Process

1. Proposed amendments MUST be documented with:
   - Clear rationale for the change
   - Impact analysis on existing projects and workflows
   - Migration plan for affected codebases
   - Approval from project stakeholders
2. Version numbering follows semantic versioning:
   - MAJOR: Backward-incompatible governance changes or principle removals
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording improvements, non-semantic refinements
3. All amendments MUST trigger updates to dependent templates and documentation
4. Historical versions MUST be preserved for audit trail

### Compliance Verification

- All pull requests MUST include a constitution compliance checklist
- Code reviews MUST verify adherence to all core principles
- Automated checks SHOULD enforce technology constraints where possible
- Violations MUST be documented and justified in the Complexity Tracking section of plan.md

### Enforcement Roles

- **Specifications**: Define WHAT is built and WHY
- **Plans**: Define HOW it is architected
- **Tasks**: Define concrete implementation steps
- **Claude Code**: Executes implementation with guaranteed compliance
- **Human Reviewers**: Validate specifications, plans, and test coverage
- **Automated Tools**: Enforce syntax, formatting, and dependency constraints

### Runtime Development Guidance

For detailed runtime guidance on using Claude Code, Spec-Kit Plus, and the development workflow, refer to `CLAUDE.md` in the repository root.

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
