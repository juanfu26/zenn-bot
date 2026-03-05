# Documentation Traceability Matrix

This document maps the Business Rules (URNs) defined in `specs/urs/` to their corresponding implementation tasks inside the `specs/changes/` directory.

Each feature or logical requirement is associated with a specific task code. Following the Spec-Driven Development (SDD) methodology, each task should reside in its own subdirectory inside `specs/changes/`, containing the respective plan and walkthrough documents.

## Traceability Mapping

| Business Rule (RN) | Assigned Task Code | Target Directory | Specification Files |
|-------------------|--------------------|------------------|---------------------|
| **RN-01** — Access Control | `TSK-SEC-01` | `specs/changes/TSK-SEC-01/` | `TSK-SEC-01_plan.md` <br> `TSK-SEC-01_walkthrough.md` |
| **RN-02** — Orphan Sessions | `TSK-SESS-01` | `specs/changes/TSK-SESS-01/` | `TSK-SESS-01_plan.md` <br> `TSK-SESS-01_walkthrough.md` |
| **RN-03** — Human Simulation | `TSK-CORE-01` | `specs/changes/TSK-CORE-01/` | `TSK-CORE-01_plan.md` <br> `TSK-CORE-01_walkthrough.md` |
| **RN-04** — No Duplicates | `TSK-CORE-02` | `specs/changes/TSK-CORE-02/` | `TSK-CORE-02_plan.md` <br> `TSK-CORE-02_walkthrough.md` |
| **RN-05** — Safe Interruption | `TSK-CORE-03` | `specs/changes/TSK-CORE-03/` | `TSK-CORE-03_plan.md` <br> `TSK-CORE-03_walkthrough.md` |
| **RN-06** — Centralized Messaging | `TSK-UI-01` | `specs/changes/TSK-UI-01/` | `TSK-UI-01_plan.md` <br> `TSK-UI-01_walkthrough.md` |
| **RN-07** — Language Policy | `TSK-UI-02` | `specs/changes/TSK-UI-02/` | `TSK-UI-02_plan.md` <br> `TSK-UI-02_walkthrough.md` |
| **RN-08** — Descriptive Terminology | `TSK-UI-03` | `specs/changes/TSK-UI-03/` | `TSK-UI-03_plan.md` <br> `TSK-UI-03_walkthrough.md` |
| **All UI RNs** — General Refactor | `TSK-REFACTOR-01` | `specs/changes/TSK-REFACTOR-01/` | `TSK-REFACTOR-01_plan.md` <br> `TSK-REFACTOR-01_walkthrough.md` |
| **RN-09** — Timezone Awareness | `TSK-CFG-01` | `specs/changes/TSK-CFG-01/` | `TSK-CFG-01_plan.md` <br> `TSK-CFG-01_walkthrough.md` |

## Task Categories Reference
* **TSK-SEC**: Security & Access Control tasks.
* **TSK-SESS**: Session Management tasks.
* **TSK-CORE**: Core Execution & Bot Lifecycle tasks.
* **TSK-UI**: Interface, Messaging, and Terminology tasks.
* **TSK-CFG**: Application Environment & Configuration tasks.
* **TSK-REFACTOR**: Legacy refactoring and large codebase restructuring.

> **Migration Note**: For existing implementations in the root of `specs/` (e.g., `timezone_implementation_plan.md`), these files should be migrated to match this new structure (such as moving `timezone_implementation_plan.md` to `specs/TSK-CFG-01/TSK-CFG-01_plan.md`) to maintain strict traceability.
