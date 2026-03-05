# Documentation Traceability Matrix

This document maps the Business Rules (URNs) defined in `specs/urs/` to their corresponding implementation tasks inside the `specs/changes/` directory.

Each feature or logical requirement is associated with a specific task code. Following the Spec-Driven Development (SDD) methodology, each task should reside in its own subdirectory inside `specs/changes/`, containing the respective plan and walkthrough documents.

## Traceability Mapping

| Business Rule (RN) | Assigned Task Code | Target Directory | Specification Files |
|-------------------|--------------------|------------------|---------------------|
| **RN-01** — Access Control | `260305-access-control` | `specs/changes/260305-access-control/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-02** — Orphan Sessions | `260305-orphan-sessions` | `specs/changes/260305-orphan-sessions/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-03** — Human Simulation | `260305-human-simulation` | `specs/changes/260305-human-simulation/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-04** — No Duplicates | `260305-no-duplicates` | `specs/changes/260305-no-duplicates/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-05** — Safe Interruption | `260305-safe-interruption` | `specs/changes/260305-safe-interruption/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-06** — Centralized Messaging | `260305-centralized-messaging` | `specs/changes/260305-centralized-messaging/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-07** — Language Policy | `260305-language-policy` | `specs/changes/260305-language-policy/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-08** — Descriptive Terminology | `260305-descriptive-terminology` | `specs/changes/260305-descriptive-terminology/` | `implementation_plan.md` <br> `walkthrough.md` |
| **All UI RNs** — General Refactor | `260305-general-refactor` | `specs/changes/260305-general-refactor/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-09** — Timezone Awareness | `260305-timezone-awareness` | `specs/changes/260305-timezone-awareness/` | `implementation_plan.md` <br> `walkthrough.md` |
| **RN-10** — Dynamic Shift Timings | `260306-dynamic-shift-timings` | `specs/changes/260306-dynamic-shift-timings/` | `implementation_plan.md` <br> `walkthrough.md` |

## Task Categories Reference
* **TSK-SEC**: Security & Access Control tasks.
* **TSK-SESS**: Session Management tasks.
* **TSK-CORE**: Core Execution & Bot Lifecycle tasks.
* **TSK-UI**: Interface, Messaging, and Terminology tasks.
* **TSK-CFG**: Application Environment & Configuration tasks.
* **TSK-REFACTOR**: Legacy refactoring and large codebase restructuring.

> **Migration Note**: For existing implementations in the root of `specs/` (e.g., `timezone_implementation_plan.md`), these files should be migrated to match this new structure (such as moving `timezone_implementation_plan.md` to `specs/260305-timezone-awareness/implementation_plan.md`) to maintain strict traceability.
